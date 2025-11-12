from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import json

from app import RetrieverAgent, EvaluatorAgent, SummarizerAgent, get_logger
from app.models.models import Offer

logger = get_logger(__name__)
router = APIRouter()

# ----------- Agents -----------
retriever = RetrieverAgent()
evaluator = EvaluatorAgent()
summarizer = SummarizerAgent()

# ----------- Request & Response Schemas -----------

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class EvaluatedOffer(BaseModel):
    supplier: str
    item: str
    unit_price: float
    delivery_days: int
    risk_assessment: str


class CustomQueryResponse(BaseModel):
    recommendation: Optional[str]
    reasoning: Optional[str]
    offers_evaluated: List[EvaluatedOffer]


# ----------- Helper Function -----------

def extract_risk_assessment(note: Optional[str]) -> str:
    """Map supplier note text to a structured risk assessment label."""
    note_lower = (note or "").lower()
    if "high risk" in note_lower or "quality issues" in note_lower:
        return "High Risk (Major quality issues last year, be cautious)"
    elif "low risk" in note_lower or "reliable" in note_lower or "95%" in note_lower:
        return "Low Risk (Reliable supplier, consistent on-time delivery)"
    elif "moderate" in note_lower:
        return "Moderate Risk (Occasional issues or delays)"
    else:
        return "Unknown Risk (Insufficient data)"


# ----------- Main Endpoint -----------

@router.post("/evaluate-offers", response_model=CustomQueryResponse, summary="Search, Evaluate and Summarize offers")
def query_offers(req: QueryRequest):
    """Multi-agent RAG pipeline: Retriever → Evaluator → Summarizer"""

    # Step 1: Retrieve top-k offers
    retrieved_offers = retriever.search(req.query, k=req.top_k)
    offer_dicts = [offer.model_dump() for offer in retrieved_offers]

    if not offer_dicts:
        logger.warning("⚠️ No offers retrieved. Returning 'No Offer'.")
        return CustomQueryResponse(
            recommendation="No Offer",
            reasoning="No supplier offers were retrieved for the given query.",
            offers_evaluated=[]
        )

    # Evaluate offers using LLM-based EvaluatorAgent
    best_offer = evaluator.evaluate(req.query, offer_dicts)

    #  Summarize using SummarizerAgent (only summarizing best_offer)
    if best_offer:
        best_offer_copy = best_offer.copy()
        evaluation_reason = best_offer_copy.pop("evaluation_reason", "")
        summary_text = summarizer.summarize(
            query=req.query,
            best_offer=json.dumps(best_offer_copy, indent=2)
        )
    else:
        summary_text = None
        evaluation_reason = "No supplier found matching the required product specifications."

    # Format all offers for response
    offers_evaluated = [
        EvaluatedOffer(
            supplier=o.get("supplier", "Unknown"),
            item=f"{o.get('item', 'N/A')} ({o.get('product_id', 'N/A')})",
            unit_price=o.get("unit_price", 0.0),
            delivery_days=o.get("delivery_days", 0),
            risk_assessment=extract_risk_assessment(o.get("risk_note"))
        ) for o in offer_dicts
    ]

    # Return final structured response
    return CustomQueryResponse(
        recommendation=best_offer.get("supplier") if best_offer else "No Offer",
        reasoning=summary_text or evaluation_reason,
        offers_evaluated=offers_evaluated
    )
