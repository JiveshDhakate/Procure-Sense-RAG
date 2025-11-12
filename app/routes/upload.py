import logging
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import ExtractorAgent, RetrieverAgent


# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
extractor = ExtractorAgent()
retriever = RetrieverAgent()

class UploadRequest(BaseModel):
    text: str

class UploadResponse(BaseModel):
    message: str
    offers_added: int

@router.post(
    "/ingest-offers",
    response_model=UploadResponse,
    summary="Extract structured supplier offers and add them to the vector database"
)
def upload_text(data: UploadRequest):
    try:
        logger.info("Received upload request")

        # Extract structured offers
        offers = extractor.extract_offers(data.text)
        if not offers:
            logger.warning("No offers could be extracted from the text")
            raise ValueError("No offers could be extracted.")

        logger.info(f"Extracted {len(offers)} offer(s)")

        # Add to vector store
        retriever.add_offers(offers)
        logger.info("Offers successfully added to vector store")

        return UploadResponse(
            message="Offers successfully extracted and stored.",
            offers_added=len(offers)
        )

    except Exception as e:
        logger.error("Error during upload processing")
        traceback.print_exc()  # Full stack trace to console
        logger.error(f"Exception detail: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
