import uuid
import time
import re
from typing import List
from langchain_openai import OpenAIEmbeddings
from chromadb import PersistentClient
from app.models.models import Offer
from app import get_logger

logger = get_logger(__name__)


class RetrieverAgent:
    def __init__(self, persist_dir: str = "./chroma_db"):
        """Initializes persistent ChromaDB store and OpenAI embeddings."""
        try:
            logger.info(f"Initializing RetrieverAgent with persistence at: {persist_dir}")
            self.client = PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection("supplier_offers")
            self.embedder = OpenAIEmbeddings(model="text-embedding-3-small")
            logger.info("RetrieverAgent successfully initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize RetrieverAgent: {e}", exc_info=True)
            raise

    def _offer_to_text(self, offer: Offer) -> str:
        """Converts an Offer object into descriptive text for embeddings."""
        return (
            f"Supplier: {offer.supplier}. "
            f"Item: {offer.item}. "
            f"Product ID: {offer.product_id}. "
            f"Unit price: {offer.unit_price}. "
            f"Minimum quantity: {offer.min_quantity}. "
            f"Delivery time: {offer.delivery_days} days. "
            f"Payment terms: {offer.payment_terms}. "
            f"Risk note: {offer.risk_note or 'No risk notes provided'}."
        )

    def _detect_intents(self, query: str) -> list[str]:
        """
        Identify all relevant intents in the query.
        Returns a list of intents such as ['price', 'delivery', 'risk'].
        """
        q = query.lower()
        intents = []

        if any(word in q for word in ["price", "cheapest", "cost", "under", "budget"]):
            intents.append("price")

        if any(word in q for word in ["delivery", "fast", "quick", "urgent", "asap"]):
            intents.append("delivery")

        if any(word in q for word in ["risk", "reliable", "dependable", "trust", "quality"]):
            intents.append("risk")

        if any(word in q for word in ["bulk", "large order", "quantity"]):
            intents.append("bulk")
        # Default fallback
        if not intents:
            intents.append("general")
        return intents


    def add_offers(self, offers: List[Offer]) -> None:
        """Adds supplier offers into the Chroma vector store."""
        if not offers:
            logger.warning("No offers provided for addition to vector store.")
            return

        logger.info(f"Adding {len(offers)} offers to vector store...")
        start_time = time.time()

        try:
            ids = [str(uuid.uuid4()) for _ in offers]
            docs = [self._offer_to_text(o) for o in offers]
            metas = [o.model_dump(exclude_none=True) for o in offers]
            embeddings = self.embedder.embed_documents(docs)

            self.collection.add(
                ids=ids,
                documents=docs,
                embeddings=embeddings,
                metadatas=metas
            )
            elapsed = time.time() - start_time
            logger.info(f"Added {len(offers)} offers to ChromaDB in {elapsed:.2f}s.")
        except Exception as e:
            logger.error(f"Error adding offers: {e}", exc_info=True)
            raise

    def search(self, query: str, k: int = 5) -> List[Offer]:
        """
        Performs intent-aware semantic retrieval:
        1. Detects size (e.g., '10 mm') and multiple query intents (price, delivery, risk, etc.).
        2. Performs vector search using OpenAI embeddings.
        3. Applies keyword filtering for product, size, and intent relevance.
        """
        logger.info(f"🔍 Searching for query: '{query}' (top {k})")
        start_time = time.time()

        try:
            query_lower = query.lower()
            mm_match = re.search(r"(\d+)\s*mm", query_lower)
            query_mm = mm_match.group(1) if mm_match else None
            intents = self._detect_intents(query)
            product_keywords = ["bolt", "fastener", "steel", "alloy", "component"]

            # ---  Embed query ---
            query_embedding = self.embedder.embed_query(query)

            # --- Perform semantic search ---
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k * 2  # fetch more to allow filtering
            )

            retrieved_offers = [Offer(**meta) for meta in results.get("metadatas", [[]])[0]]

            # ---  Filter for relevance ---
            filtered_offers = []
            for offer in retrieved_offers:
                text = (offer.item or "").lower()

                # Product relevance
                if not any(p in text for p in product_keywords):
                    continue

                # Size matching (if query mentions mm)
                if query_mm:
                    size_match = re.search(r"(\d+)\s*mm", text)
                    if not size_match or size_match.group(1) != query_mm:
                        continue

                # Intent-based soft filtering (accept if ANY intent matches)
                if intents and intents != ["general"]:
                    matched = False
                    for intent in intents:
                        if (
                            (intent == "delivery" and re.search(r"delivery|days|ship|arrive", text))
                            or (intent == "price" and re.search(r"price|unit|cost|\$", text))
                            or (intent == "risk" and re.search(r"risk|reliable|quality|defect", text))
                            or (intent == "bulk" and re.search(r"bulk|large|quantity|min", text))
                        ):
                            matched = True
                            break
                    if not matched:
                        continue  # skip if none of the detected intents matched

                filtered_offers.append(offer)

            # --- Fallback & Logging ---
            final_results = filtered_offers[:k] if filtered_offers else retrieved_offers[:k]

            elapsed = time.time() - start_time
            logger.info(
                f"Retrieved {len(final_results)} relevant offers "
                f"(intents: {', '.join(intents)}) in {elapsed:.2f}s."
            )

            if not final_results:
                logger.warning("No relevant offers found for this query.")

            return final_results

        except Exception as e:
            logger.error(f"Error during vector search: {e}", exc_info=True)
            raise

