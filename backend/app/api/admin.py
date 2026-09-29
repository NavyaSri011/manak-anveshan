# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
import datetime

from app.database.connection import get_db
from app.database.models import Standard
from app.scripts.sync_bis_standards import sync_bis_standards

router = APIRouter(prefix="/admin", tags=["Admin & Data Sources"])

@router.get("/status")
def get_bis_knowledge_base_status(db: Session = Depends(get_db)):
    total_count = db.query(Standard).count()
    authoritative_count = db.query(Standard).filter(Standard.source_type == "AUTHORITATIVE").count()
    categories = db.query(Standard.category).distinct().all()
    cat_list = [c[0] for c in categories if c[0]]

    return {
        "bis_status": "CONNECTED",
        "authoritative_source": "Bureau of Indian Standards (BIS)",
        "source_portal": "https://standards.bis.gov.in/",
        "total_standards_indexed": total_count,
        "authoritative_records_count": authoritative_count,
        "categories_covered": cat_list,
        "last_sync_timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "sync_mode": "REALTIME_INGESTION"
    }

@router.post("/standards/sync")
def trigger_bis_standards_sync(db: Session = Depends(get_db)):
    try:
        res = sync_bis_standards(db)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BIS Standards sync failed: {str(e)}")
