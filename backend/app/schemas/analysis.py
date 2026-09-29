from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RequirementItem(BaseModel):
    category: Optional[str] = "technical_parameters"
    attribute: str
    value: str
    unit: Optional[str] = ""
    source_text: Optional[str] = ""

class RequirementExtractionRequest(BaseModel):
    product_title: str
    product_description: Optional[str] = ""
    technical_specification: Optional[Dict[str, Any]] = {}
    language: Optional[str] = "en"
    document_text: Optional[str] = ""

class ExtractedRequirementsResult(BaseModel):
    product: Dict[str, str]
    application: Optional[str] = ""
    environment: Dict[str, str] = {}
    technical_parameters: Dict[str, Any] = {}
    materials: List[str] = []
    performance: List[str] = []
    safety: List[str] = []
    canonical_query: str = ""

class TenderAnalysisRequest(BaseModel):
    request_id: Optional[str] = "TENDER-001"
    product_title: Optional[str] = "Industrial Centrifugal Pump"
    product_description: Optional[str] = ""
    technical_specification: Optional[Dict[str, Any]] = {}
    extracted_requirements: Optional[List[RequirementItem]] = None
    language: Optional[str] = "en"
    document_text: Optional[str] = None

class EvidenceItem(BaseModel):
    source: str
    type: str # scope, technical_match, relationship, qco_gazette, amendment
    reference: str

class RecommendationCard(BaseModel):
    id: str
    is_number: str
    title: str
    scope: str
    status: str
    publication_info: str
    category: str
    classification: str # PRIMARY, SUPPORTING, NORMATIVE_REFERENCE, TEST_METHOD, SAFETY, INSTALLATION, TERMINOLOGY, RELATED
    confidence_score: float # 0 to 1
    reason: List[str]
    evidence: List[EvidenceItem]
    lifecycle_alert: Optional[str] = None
    certification_info: Optional[Dict[str, Any]] = None
    source: Optional[str] = "Bureau of Indian Standards (BIS)"
    source_url: Optional[str] = "https://standards.bis.gov.in/"
    source_type: Optional[str] = "AUTHORITATIVE"
    last_verified: Optional[str] = None

class MissingRequirementAlert(BaseModel):
    attribute: str
    importance: str # HIGH, MEDIUM, LOW
    impact: str
    message: str

class StandardsGraphNode(BaseModel):
    id: str
    type: str # product, primary, test, safety, installation, normative, certification
    label: str
    status: Optional[str] = "ACTIVE"
    category: Optional[str] = ""

class StandardsGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    animated: Optional[bool] = False

class StandardsGraphData(BaseModel):
    nodes: List[StandardsGraphNode]
    edges: List[StandardsGraphEdge]

class TenderAnalysisResponse(BaseModel):
    analysis_id: str
    request_id: str
    product_title: str
    language: str
    created_at: str
    canonical_requirements: ExtractedRequirementsResult
    primary_standards: List[RecommendationCard]
    supporting_standards: List[RecommendationCard]
    normative_references: List[RecommendationCard]
    test_methods: List[RecommendationCard]
    safety_standards: List[RecommendationCard]
    installation_standards: List[RecommendationCard]
    related_standards: List[RecommendationCard]
    version_alerts: List[Dict[str, Any]]
    certification_summary: List[Dict[str, Any]]
    missing_requirements: List[MissingRequirementAlert]
    graph_data: StandardsGraphData
    summary_counts: Dict[str, int]
