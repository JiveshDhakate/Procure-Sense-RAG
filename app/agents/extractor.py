"""
ExtractorAgent
    The ExtractorAgent is the first component in our system.
    Its job is to take messy, unstructured quotation text like:
    “QuickFix is offering 10mm steel bolts (Product ID: SB-10) at $0.75 per unit… Delivery: 10 business days...”
"""
import json
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from app.models.models import Offer
from app import get_logger

logger = get_logger(__name__)

load_dotenv()
SYSTEM_PROMPT = """
You are an information extraction assistant for supplier quotations.
Extract a JSON list of offers from the following raw text.

Each offer must include:
- supplier (string)
- item (string)
- product_id (string or null)
- unit_price (number or null)
- min_quantity (integer or null)
- delivery_days (integer or null)
- payment_terms (string or null)
- risk_note (string or null)
- raw_text (original quoted snippet)

Return ONLY a valid JSON list of offers.
No extra text. No commentary.
"""

class ExtractorAgent:
    def __init__(self):
        logger.info("ExtractorAgent initialized.")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)

    def extract_offers(self, text: str) -> List[Offer]:
        logger.info("Starting offer extraction using LLM.")
        try:
            # Build chat messages
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
            logger.debug("Prepared system and user messages for OpenAI API.")

            # Call OpenAI Chat API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0
            )
            logger.info("Received response from OpenAI model.")

            # Extract returned JSON string from LLM response
            json_text = response.choices[0].message.content.strip()

            # Clean Markdown fences (```json ... ```)
            if json_text.startswith("```"):
                logger.debug("Cleaning Markdown formatting from LLM output.")
                json_text = json_text.strip("`")
                json_text = json_text.replace("json", "", 1).strip()
                json_text = json_text.replace("```", "").strip()

            # Log raw output for debugging (comment out if too verbose)
            logger.debug(f"Raw LLM output: {json_text[:300]}...")

            # Convert string to list of Offer objects
            offer_list = json.loads(json_text)
            logger.info(f"Parsed {len(offer_list)} offers successfully.")

            offers = [Offer(**data) for data in offer_list]
            logger.info("Offer objects created successfully.")
            return offers

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON output from LLM: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error during offer extraction: {e}", exc_info=True)
            raise
