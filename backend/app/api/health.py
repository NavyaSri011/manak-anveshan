# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.core.config import settings
from app.services.llm_service import LLMService

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0-SIH2026",
        "llm_provider": settings.LLM_PROVIDER,
        "llm_configured": LLMService.is_configured(),
        "database_url_type": "SQLite" if "sqlite" in settings.DATABASE_URL else "PostgreSQL"
    }
