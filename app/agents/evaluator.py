from typing import List, Dict, Optional
import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser
from app import get_logger

logger = get_logger(__name__)

PROMPT_TEMPLATE_STRING = """
You are a procurement analyst. Your job is to select the single best supplier from the PRE-FILTERED list below and explain your choice.

The list has ALREADY been filtered for product size and critical risks (if the user's query mentioned them).

---

### 1. Analyze User Intent
Read the user query to understand their main priorities:
- "price", "cheapest", "under": `unit_price`
- "delivery", "fast", "urgent": `delivery_days`
- "risk", "reliable", "quality": `risk_assessment`
- "payment", "credit", "terms": `payment_terms`

---

### 2. Rank Offers
Select the best offer by applying this **strict priority chain** to the entire list:

1.  **Lower `risk_assessment`** (Low > Moderate > High > Unknown)
2.  **Lower `unit_price`**
3.  **Lower `delivery_days`**
4.  **Better `payment_terms`** (Net 60 > Net 45 > Net 30)
5.  **Lower `min_quantity`**

---

### 3. Justify Your Choice
Your reasoning is the most important part.
- State clearly why the winner was chosen based on the priority chain.
- Use the User Query intents to "color" your explanation.
- **Example:** If the winner is low-risk but expensive, and the user wanted "cheap", you must explain: "Supplier X was chosen for its 'Low Risk' status, which is our top priority. Although Supplier Y was cheaper, it was rejected due to its 'Moderate Risk' assessment."

---

### 4. Output Format
Return ONLY a valid JSON object. Do not include any other text.

{format_instructions}

---

### User Query:
{query}

### Pre-Filtered Supplier Offers (JSON list):
{offers}
"""

class EvaluatorAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        logger.info(f"EvaluatorAgent initialized with model: {model_name}")

        self.response_schemas = [
            ResponseSchema(name="supplier", description="Best supplier name or 'No Offer'"),
            ResponseSchema(name="reason", description="Short reason for the final selection"),
            ResponseSchema(name="score_explanation", description="Summary of how top offers compare"),
            ResponseSchema(name="priority_breakdown", description="Breakdown of key decision priorities")
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_STRING)
    
    def _filter_by_size(self, query: str, offers: List[Dict]) -> List[Dict]:
        """Filters offers based on exact mm size in the query."""
        mm_match = re.search(r"(\d+)\s*mm", query.lower())
        if not mm_match:
            return offers  # No size specified, return all
        
        required_mm = mm_match.group(1)
        pattern = re.compile(rf"\b{re.escape(required_mm)}\s*mm\b", re.IGNORECASE)
        pattern_no_space = re.compile(rf"\b{re.escape(required_mm)}mm\b", re.IGNORECASE)

        filtered = [
            o for o in offers 
            if pattern.search(o.get("item", "")) or pattern_no_space.search(o.get("item", ""))
        ]
        logger.debug(f"Size filter ({required_mm}mm): {len(filtered)}/{len(offers)} offers remain.")
        return filtered

    def _query_implies_reliability(self, query: str) -> bool:
        """Checks if the query implies a high-stakes, risk-averse purchase."""
        q = query.lower()
        reliability_keywords = ["large order", "large quantity", "critical", "important", "engineering", "lowest risk", "reliable"]
        if any(k in q for k in reliability_keywords):
            return True
        
        # Check for large quantity numbers
        qty_match = re.search(r"(?:over|more than|greater than|>=|)\s*([\d,]+)\s*(?:units|pcs|pieces|items)?", q)
        if qty_match:
            try:
                qty = int(qty_match.group(1).replace(",", ""))
                if qty >= 1000:
                    return True
            except ValueError:
                pass
        return False

    def _is_high_risk(self, offer: Dict) -> bool:
        """Checks if an offer is flagged as high risk in any relevant notes field."""
        risk_text = " ".join([
            str(offer.get("risk_assessment") or ""),
            str(offer.get("risk_note") or ""),
            str(offer.get("notes") or ""),
            str(offer.get("supplier_comments") or "")
        ]).lower()
        return any(kw in risk_text for kw in ["high risk", "quality issues", "major quality", "production delays"])

    def evaluate(self, query: str, offers: List[Dict]) -> Optional[Dict]:
        if not offers:
            logger.warning("No offers provided for evaluation.")
            return None

        logger.info(f"Evaluating {len(offers)} offers for query: '{query}'")
        
        #  Filter by size
        filtered_offers = self._filter_by_size(query, offers)
        if not filtered_offers:
            logger.warning("No size-matching offers found.")
            return {
                "supplier": "No Offer",
                "evaluation_reason": "No supplier found matching the required product size.",
                "score_explanation": f"Query specified a size not found in offers.",
                "priority_breakdown": "Product size match"
            }

        # Filter by risk if query is critical
        if self._query_implies_reliability(query):
            logger.info("🔒 Query implies reliability. Applying strict risk filter.")
            reliable_offers = [o for o in filtered_offers if not self._is_high_risk(o)]
            
            if not reliable_offers:
                logger.warning("All size-matching offers were disqualified due to high risk.")
                return {
                    "supplier": "No Offer",
                    "evaluation_reason": "All matching suppliers were disqualified due to high risk for a critical order.",
                    "score_explanation": "All suppliers matching the size constraint were found to be high risk.",
                    "priority_breakdown": "Risk assessment was the highest priority."
                }
            
            # Use only the reliable offers for the LLM
            offers_to_evaluate = reliable_offers
            logger.info(f"Risk filter applied: {len(offers_to_evaluate)}/{len(filtered_offers)} offers remaining.")
        else:
            offers_to_evaluate = filtered_offers 
        try:
            offers_text = json.dumps(offers_to_evaluate, indent=2)
        
            formatted_prompt = self.prompt_template.format(
                query=query,
                offers=offers_text,
                format_instructions=self.format_instructions
            )
            messages = formatted_prompt.to_messages()
            result = self.llm(messages)
            parsed = self.output_parser.parse(result.content)

            supplier = parsed.get("supplier", "No Offer").strip()
            logger.info(f"Evaluator selected supplier: {supplier}")

            # Find the original offer object to return
            best = next((o for o in offers_to_evaluate if supplier.lower() in o.get("supplier", "").lower()), None)
            
            if not best or supplier.lower() == "no offer":
                # Handle case where LLM returns "No Offer"
                return {
                    "supplier": "No Offer",
                    "evaluation_reason": parsed.get("reason", "No suitable supplier found after evaluation."),
                    "score_explanation": parsed.get("score_explanation", ""),
                    "priority_breakdown": parsed.get("priority_breakdown", "")
                }
            
            # Add LLM reasoning to the chosen offer
            best.update({
                "evaluation_reason": parsed.get("reason", ""),
                "score_explanation": parsed.get("score_explanation", ""),
                "priority_breakdown": parsed.get("priority_breakdown", "")
            })
            return best

        except Exception as e:
            logger.error(f"Evaluation error: {e}", exc_info=True)
            # Fallback in case of LLM error
            return offers_to_evaluate[0] if offers_to_evaluate else None