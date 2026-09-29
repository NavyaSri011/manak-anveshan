# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.database.connection import engine, Base, SessionLocal
from app.database.seed_data import seed_database

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="MANAK ANVESHAN - AI-Powered Indian Standards Intelligence for Procurement (SIH 2026 Prototype)"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "message": "MANAK ANVESHAN - Indian Standards Intelligence API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
