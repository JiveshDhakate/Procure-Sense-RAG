from fastapi import FastAPI
from app import upload_router, query_router, get_logger

# Initialize logger and FastAPI app
logger = get_logger(__name__)
app = FastAPI(
    title="ProcureSense-RAG: Supplier Quotation Analysis API",
    description="Multi-Agent RAG system for supplier offer extraction, evaluation, and summarization.",
    version="1.0.0"
)

logger.info("ProcureSense-RAG API has started")

# Include routers with meaningful prefixes and tags
app.include_router(
    upload_router,
    prefix="/procure-sense-rag",
    tags=["Data Ingestion"]
)

app.include_router(
    query_router,
    prefix="/procure-sense-rag",
    tags=["Supplier Evaluation"]
)

# Health check route
@app.get("/ping", tags=["Health Check"])
def ping():
    return {"status": "ok", "message": "ProcureSense-RAG API is running 🚀"}
