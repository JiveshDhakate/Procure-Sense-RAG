"""
Two Pydantic models:
    Offer - for structured supplier offer info
    UploadRequest - what the user sends to /upload
"""

from pydantic import BaseModel
from typing import Optional,List

class UploadRequest(BaseModel):
    """
    Sent to /upload
    Contains the full raw quotation as plain text.
    """
    text: str

class Offer(BaseModel):
    """This is the structured format that the LLM will extract"""
    supplier: str
    item: str
    product_id: Optional[str] = None
    unit_price : Optional[float]= None
    min_quantity: Optional[int] = None
    delivery_days: Optional[int] = None
    payment_terms: Optional[str] = None
    risk_note: Optional[str] = None
    raw_text: str