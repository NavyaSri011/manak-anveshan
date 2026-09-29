# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.database.connection import get_db
from app.database.models import Tender, Requirement, Recommendation, Standard
from app.schemas.analysis import (
    RequirementExtractionRequest, ExtractedRequirementsResult,
    TenderAnalysisRequest, TenderAnalysisResponse, RecommendationCard,
    MissingRequirementAlert
)
from app.services.extraction_service import RequirementExtractionService, extract_text_from_file_bytes
from app.services.retrieval_service import HybridRetrievalService
from app.services.applicability_service import ApplicabilityEngineService
from app.services.lifecycle_service import LifecycleService
from app.services.certification_service import CertificationEngineService
from app.services.missing_req_service import MissingRequirementService
from app.services.graph_service import GraphVisualizationService

router = APIRouter(prefix="", tags=["Analyses"])


@router.post("/extract-requirements", response_model=ExtractedRequirementsResult)
def extract_requirements(payload: RequirementExtractionRequest):
    return RequirementExtractionService.extract_from_request(
        product_title=payload.product_title,
        product_description=payload.product_description or "",
        technical_specification=payload.technical_specification or {},
        language=payload.language or "en",
        document_text=payload.document_text or ""
    )


@router.post("/extract-document", response_model=ExtractedRequirementsResult)
async def extract_document(
    file: UploadFile = File(...),
    product_title: Optional[str] = Form(None),
    language: Optional[str] = Form("en")
):
    try:
        content = await file.read()
        extracted_text = extract_text_from_file_bytes(
            content, file.filename or "document.pdf")
        title = product_title if (
            product_title and product_title.strip()) else file.filename

        return RequirementExtractionService.extract_from_request(
            product_title=title,
            product_description=f"Extracted document: {file.filename}",
            technical_specification={},
            language=language or "en",
            document_text=extracted_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to process document '{file.filename}': {str(e)}")


def _generate_analysis_response(payload: TenderAnalysisRequest, db: Session, save_to_db: bool = True) -> TenderAnalysisResponse:
    # 1. Requirement Extraction
    extracted = RequirementExtractionService.extract_from_request(
        product_title=payload.product_title or "Equipment Tender",
        product_description=payload.product_description or "",
        technical_specification=payload.technical_specification or {},
        language=payload.language or "en",
        document_text=payload.document_text or ""
    )

    # 2. Hybrid Retrieval
    retrieved_candidates = HybridRetrievalService.retrieve_candidates(
        db, extracted, top_k=12)

    # 3. Applicability Classification & Recommendation Cards
    primary_cards: List[RecommendationCard] = []
    supporting_cards: List[RecommendationCard] = []
    normative_cards: List[RecommendationCard] = []
    test_cards: List[RecommendationCard] = []
    safety_cards: List[RecommendationCard] = []
    installation_cards: List[RecommendationCard] = []
    related_cards: List[RecommendationCard] = []

    all_cards: List[RecommendationCard] = []

    for std, score in retrieved_candidates:
        card = ApplicabilityEngineService.classify_and_build_recommendation(
            db, std, score, extracted)
        all_cards.append(card)

        if card.classification == "PRIMARY":
            primary_cards.append(card)
        elif card.classification == "SUPPORTING":
            supporting_cards.append(card)
        elif card.classification == "NORMATIVE_REFERENCE":
            normative_cards.append(card)
        elif card.classification == "TEST_METHOD":
            test_cards.append(card)
        elif card.classification == "SAFETY":
            safety_cards.append(card)
        elif card.classification == "INSTALLATION":
            installation_cards.append(card)
        else:
            related_cards.append(card)

    # IMPORTANT:
    # Do not force the highest-ranked candidate to PRIMARY.
    # PRIMARY must come only from the applicability engine when
    # product/scope evidence supports that classification.

    # 4. Certification Engine
    cert_summary = CertificationEngineService.attach_certification_evidence(
        db, all_cards)

    # 5. Lifecycle Intelligence
    full_text = f"{payload.product_title} {payload.product_description} {payload.document_text}"
    version_alerts = LifecycleService.audit_lifecycle_and_alerts(
        db, full_text, all_cards)

    # 6. Missing Requirements Gap Detection
    missing_reqs = MissingRequirementService.detect_missing_requirements(
        extracted)

    # 7. Relationship Graph Construction
    graph_data = GraphVisualizationService.build_graph_data(
        product_title=extracted.product.get(
            "name", payload.product_title or "Tender Item"),
        primary=primary_cards,
        supporting=supporting_cards,
        normative=normative_cards,
        test=test_cards,
        safety=safety_cards,
        installation=installation_cards,
        certification_summary=cert_summary
    )

    analysis_id = str(uuid.uuid4())
    req_id = payload.request_id or f"TENDER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    created_at = datetime.utcnow()

    if save_to_db:
        # 8. Save Analysis record to DB
        tender = Tender(
            id=analysis_id,
            request_id=req_id,
            product_title=payload.product_title or "Procurement Specification",
            product_description=payload.product_description,
            language=payload.language or "en",
            raw_spec=payload.technical_specification,
            created_at=created_at
        )
        db.add(tender)
        db.commit()

        for k, v in extracted.technical_parameters.items():
            req = Requirement(
                tender_id=analysis_id,
                category="technical_parameters",
                attribute=k,
                value=str(v),
                source_text=f"{k}: {v}"
            )
            db.add(req)

        for card in all_cards:
            rec = Recommendation(
                tender_id=analysis_id,
                standard_id=card.id,
                classification=card.classification,
                retrieval_score=card.confidence_score,
                applicability_score=card.confidence_score,
                reasoning=card.reason,
                evidence=[e.model_dump() for e in card.evidence]
            )
            db.add(rec)
        db.commit()

    summary_counts = {
        "primary": len(primary_cards),
        "supporting": len(supporting_cards),
        "normative": len(normative_cards),
        "test": len(test_cards),
        "safety": len(safety_cards),
        "installation": len(installation_cards),
        "related": len(related_cards),
        "total_analyzed": len(all_cards)
    }

    return TenderAnalysisResponse(
        analysis_id=analysis_id,
        request_id=req_id,
        product_title=payload.product_title or "Equipment Tender",
        language=payload.language or "en",
        created_at=created_at.strftime("%Y-%m-%d %H:%M:%S"),
        canonical_requirements=extracted,
        primary_standards=primary_cards,
        supporting_standards=supporting_cards,
        normative_references=normative_cards,
        test_methods=test_cards,
        safety_standards=safety_cards,
        installation_standards=installation_cards,
        related_standards=related_cards,
        version_alerts=version_alerts,
        certification_summary=cert_summary,
        missing_requirements=missing_reqs,
        graph_data=graph_data,
        summary_counts=summary_counts
    )


@router.post("/standards/analyze", response_model=TenderAnalysisResponse)
def analyze_tender_standards(payload: TenderAnalysisRequest, db: Session = Depends(get_db)):
    return _generate_analysis_response(payload, db, save_to_db=True)


@router.get("/analyses")
def list_analyses(db: Session = Depends(get_db)):
    tenders = db.query(Tender).order_by(Tender.created_at.desc()).all()
    results = []
    for t in tenders:
        results.append({
            "id": t.id,
            "request_id": t.request_id,
            "product_title": t.product_title,
            "language": t.language,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "COMPLETED",
            "requirement_count": len(t.requirements),
            "recommendation_count": len(t.recommendations)
        })
    return results


@router.get("/analyses/{analysis_id}")
def get_analysis_detail(analysis_id: str, db: Session = Depends(get_db)):
    tender = db.query(Tender).filter(Tender.id == analysis_id).first()
    if not tender:
        raise HTTPException(
            status_code=404, detail="Analysis record not found")

    fake_payload = TenderAnalysisRequest(
        request_id=tender.request_id,
        product_title=tender.product_title,
        product_description=tender.product_description,
        technical_specification=tender.raw_spec or {},
        language=tender.language
    )

    resp = _generate_analysis_response(fake_payload, db, save_to_db=False)
    resp.analysis_id = tender.id
    resp.created_at = tender.created_at.strftime("%Y-%m-%d %H:%M:%S")
    return resp
