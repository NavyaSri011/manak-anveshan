from pydantic import BaseModel, Field
from typing import List, Optional

class AmendmentSchema(BaseModel):
    id: str
    amendment_number: int
    date: Optional[str] = None
    description: str
    source: str

    class Config:
        from_attributes = True

class RelationshipSchema(BaseModel):
    id: str
    source_standard_id: str
    target_standard_id: str
    relationship_type: str
    evidence: Optional[str] = None
    target_is_number: Optional[str] = None
    target_title: Optional[str] = None

    class Config:
        from_attributes = True

class CertificationRuleSchema(BaseModel):
    id: str
    product: str
    scheme: str
    mandatory: bool
    conditions: Optional[str] = None
    source: str

    class Config:
        from_attributes = True

class StandardSchema(BaseModel):
    id: str
    is_number: str
    title: str
    scope: str
    status: str
    publication_date: Optional[str] = None
    revision_date: Optional[str] = None
    ics_codes: Optional[str] = None
    category: str
    source: str
    source_type: str
    replaced_by_is: Optional[str] = None
    amendments: List[AmendmentSchema] = []
    certification_rules: List[CertificationRuleSchema] = []

    class Config:
        from_attributes = True

class ValidateStandardRequest(BaseModel):
    is_number: str

class ValidateStandardResponse(BaseModel):
    is_number: str
    valid: bool
    status: str
    replaced_by: Optional[str] = None
    warning_message: Optional[str] = None
    standard: Optional[StandardSchema] = None
