# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


# React frontend
FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@app.get("/", include_in_schema=False)
def root():
    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "MANAK ANVESHAN - Indian Standards Intelligence API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


# Serve frontend assets
if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=str(FRONTEND_DIST / "assets")),
        name="assets"
    )


# React Router fallback
@app.get("/{full_path:path}", include_in_schema=False)
def serve_react_app(full_path: str):
    # Never interfere with API routes
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}

    requested_file = FRONTEND_DIST / full_path

    if requested_file.is_file():
        return FileResponse(requested_file)

    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "MANAK ANVESHAN - Indian Standards Intelligence API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
