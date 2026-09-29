# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, Query
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.database.models import Standard, Amendment, StandardRelationship
from app.schemas.standards import StandardSchema, ValidateStandardRequest, ValidateStandardResponse, RelationshipSchema

router = APIRouter(prefix="/standards", tags=["Standards"])


@router.get("/count")
def standards_count(db: Session = Depends(get_db)):
    return {"count": db.query(Standard).count()}


@router.get("", response_model=List[StandardSchema])
def list_standards(
    search: Optional[str] = Query(
        None, description="Search term for IS number, title, scope"),
    category: Optional[str] = Query(None, description="Category filter"),
    db: Session = Depends(get_db)
):
    query = db.query(Standard)
    if category:
        query = query.filter(Standard.category == category)
    if search:
        s_term = f"%{search}%"
        query = query.filter(
            (Standard.is_number.ilike(s_term)) |
            (Standard.title.ilike(s_term)) |
            (Standard.scope.ilike(s_term))
        )
    return query.all()


@router.get("/{standard_id}")
def get_standard_detail(standard_id: str, db: Session = Depends(get_db)):
    std = db.query(Standard).filter(Standard.id == standard_id).first()
    if not std:
        # try search by is_number
        std = db.query(Standard).filter(
            Standard.is_number.ilike(f"%{standard_id}%")).first()
    if not std:
        raise HTTPException(status_code=404, detail="Standard not found")

    # Fetch relationships
    relationships = []
    rel_rows = db.query(StandardRelationship).filter(
        StandardRelationship.source_standard_id == std.id).all()
    for rel in rel_rows:
        target = db.query(Standard).filter(
            Standard.id == rel.target_standard_id).first()
        relationships.append({
            "id": rel.id,
            "relationship_type": rel.relationship_type,
            "evidence": rel.evidence,
            "target_is_number": target.is_number if target else "Unknown",
            "target_title": target.title if target else "Unknown"
        })

    return {
        "standard": StandardSchema.model_validate(std),
        "relationships": relationships
    }


@router.post("/validate", response_model=ValidateStandardResponse)
def validate_standard(payload: ValidateStandardRequest, db: Session = Depends(get_db)):
    is_num = payload.is_number.strip().upper()
    std = db.query(Standard).filter(
        Standard.is_number.ilike(f"%{is_num}%")).first()

    if not std:
        return ValidateStandardResponse(
            is_number=is_num,
            valid=False,
            status="NOT_FOUND",
            warning_message=f"Standard '{is_num}' was not found in the Indian Standards Knowledge Base.",
            standard=None
        )

    warning = None
    if std.status == "SUPERSEDED":
        warning = f"ALERT: {std.is_number} is SUPERSEDED by {std.replaced_by_is or 'a revised standard'}. Do not specify in new tenders."

    return ValidateStandardResponse(
        is_number=std.is_number,
        valid=(std.status == "ACTIVE"),
        status=std.status,
        replaced_by=std.replaced_by_is,
        warning_message=warning,
        standard=StandardSchema.model_validate(std)
    )
