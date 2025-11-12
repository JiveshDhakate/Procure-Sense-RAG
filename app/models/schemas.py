from pydantic import BaseModel

class UploadRequest(BaseModel):
    text: str

class UploadResponse(BaseModel):
    message: str
    offers_added: int
