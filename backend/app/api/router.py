# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.api import health, standards, analyses, evaluation, admin

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(standards.router)
api_router.include_router(analyses.router)
api_router.include_router(evaluation.router)
api_router.include_router(admin.router)

