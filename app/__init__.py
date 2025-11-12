"""
App package initializer.
Exposes core utilities, agent classes, and API routers.
"""

# Core Utilities
from .core import get_logger

# Agent Classes
from .agents import (
    RetrieverAgent,
    EvaluatorAgent,
    ExtractorAgent,
    SummarizerAgent,
)

# API Routers
from .routes.query import router as query_router
from .routes.upload import router as upload_router


__all__ = [
    "get_logger",
    "RetrieverAgent",
    "EvaluatorAgent",
    "ExtractorAgent",
    "SummarizerAgent",
    "query_router",
    "upload_router",
]