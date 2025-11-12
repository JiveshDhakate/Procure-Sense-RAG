from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from app import get_logger
import time

logger = get_logger(__name__)

class SummarizerAgent:
    def __init__(self):
        """
        SummarizerAgent
        Generates concise, factual summaries of evaluator decisions.
        Aligned with EvaluatorAgent priorities — never re-ranks or re-evaluates offers.
        """
        logger.info("SummarizerAgent initialized.")

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a senior procurement analyst summarizing the results of a supplier evaluation.\n"
                "Your task is to clearly explain the EvaluatorAgent’s decision without changing or reinterpreting it.\n"
                "Never invent suppliers, details, or reasoning that are not present in the evaluator’s decision.\n"
                "If the evaluator concluded 'No Offer', explain that no supplier met the required specifications.\n"
                "Otherwise, summarize why the chosen supplier was selected, referencing the reasoning provided.\n"
                "Keep the tone factual, concise, and professional."
            ),
            (
                "human",
                "User Query:\n{query}\n\n"
                "Evaluator Decision:\n{best_offer}\n\n"
                "Write a short, formal summary that restates the evaluator’s decision in plain language.\n"
                "Do not add new reasoning or compare with other suppliers. Just summarize the evaluator’s justification."
            )
        ])

        # Compose LCEL chain
        self.chain = (
            self.prompt
            | ChatOpenAI(model="gpt-4o-mini", temperature=0)
            | StrOutputParser()
        )

    def summarize(self, query: str, best_offer: str) -> str:
        """
        Summarizes evaluator results in natural language.
        Mirrors EvaluatorAgent's strict decision logic — zero hallucination tolerance.
        """
        logger.info("Starting summarization process.")
        start_time = time.time()

        try:
            # Guardrail: No valid supplier selected
            if not best_offer or '"supplier": "No Offer"' in best_offer:
                logger.warning("Summarizer detected 'No Offer'. Returning default summary.")
                return (
                    "No supplier matched the required product specifications or size. "
                    "Therefore, no recommendation can be made from the evaluated offers."
                )

            # Generate concise factual summary
            summary = self.chain.invoke({
                "query": query,
                "best_offer": best_offer
            })

            elapsed = time.time() - start_time
            logger.info(f" Summarization completed in {elapsed:.2f}s.")
            logger.debug(f" Generated Summary (first 250 chars): {summary[:250]}")

            return summary.strip()

        except Exception as e:
            logger.error(f" Summarization failed: {e}", exc_info=True)
            return "An error occurred during summarization."
