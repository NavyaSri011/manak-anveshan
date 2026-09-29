# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, Float, JSON
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class Standard(Base):
    __tablename__ = "standards"

    id = Column(String, primary_key=True, default=generate_uuid)
    is_number = Column(String, unique=True, index=True, nullable=False) # e.g. "IS 1520:1980"
    title = Column(String, nullable=False)
    scope = Column(Text, nullable=False)
    status = Column(String, default="ACTIVE") # ACTIVE, REVISED, SUPERSEDED, WITHDRAWN, UNDER_REVIEW
    publication_date = Column(String, nullable=True)
    revision_date = Column(String, nullable=True)
    publication_year = Column(Integer, nullable=True)
    reviewed_year = Column(Integer, nullable=True)
    revision_information = Column(Text, nullable=True)
    department = Column(String, nullable=True) # e.g., "ETD - Electrotechnical", "MED - Mechanical"
    technical_committee = Column(String, nullable=True) # e.g., "ETD 35", "MED 03"
    classification = Column(String, nullable=True) # e.g., "PRODUCT_SPECIFICATION", "TEST_METHOD"
    certification = Column(String, nullable=True) # e.g., "BIS ISI Mark", "CRS Mandatory", "Optional"
    source_url = Column(String, default="https://standards.bis.gov.in/")
    keywords = Column(Text, nullable=True) # Searchable domain terms / synonyms
    searchable_text = Column(Text, nullable=True) # Full text for search indexing
    ics_codes = Column(String, nullable=True) # e.g. "23.080"
    category = Column(String, index=True)
    source = Column(String, default="Bureau of Indian Standards (BIS)")
    source_type = Column(String, default="AUTHORITATIVE") # AUTHORITATIVE
    replaced_by_is = Column(String, nullable=True)

    amendments = relationship("Amendment", back_populates="standard", cascade="all, delete-orphan")
    outgoing_relationships = relationship("StandardRelationship", foreign_keys="StandardRelationship.source_standard_id", back_populates="source_standard")
    incoming_relationships = relationship("StandardRelationship", foreign_keys="StandardRelationship.target_standard_id", back_populates="target_standard")
    certification_rules = relationship("CertificationRule", back_populates="standard")

class Amendment(Base):
    __tablename__ = "amendments"

    id = Column(String, primary_key=True, default=generate_uuid)
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    amendment_number = Column(Integer, nullable=False)
    date = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    source = Column(String, default="BIS Gazette / Amendment Bulletin")

    standard = relationship("Standard", back_populates="amendments")

class StandardRelationship(Base):
    __tablename__ = "standard_relationships"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    target_standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    relationship_type = Column(String, nullable=False) # NORMATIVE_REFERENCE, TEST_METHOD, SAFETY, INSTALLATION, TERMINOLOGY, RELATED, SUPERSEDES, AMENDED_BY
    evidence = Column(Text, nullable=True)

    source_standard = relationship("Standard", foreign_keys=[source_standard_id], back_populates="outgoing_relationships")
    target_standard = relationship("Standard", foreign_keys=[target_standard_id], back_populates="incoming_relationships")

class CertificationRule(Base):
    __tablename__ = "certification_rules"

    id = Column(String, primary_key=True, default=generate_uuid)
    product = Column(String, nullable=False)
    scheme = Column(String, nullable=False) # BIS Product Certification (ISI Mark), CRS, QCO, etc.
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    mandatory = Column(Boolean, default=True)
    conditions = Column(Text, nullable=True)
    source = Column(String, default="Ministry Order / Gazette Notification")

    standard = relationship("Standard", back_populates="certification_rules")

class Tender(Base):
    __tablename__ = "tenders"

    id = Column(String, primary_key=True, default=generate_uuid)
    request_id = Column(String, index=True, nullable=True) # e.g. TENDER-2026-001
    product_title = Column(String, nullable=False)
    product_description = Column(Text, nullable=True)
    language = Column(String, default="en")
    document_name = Column(String, nullable=True)
    raw_spec = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    requirements = relationship("Requirement", back_populates="tender", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="tender", cascade="all, delete-orphan")

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(String, primary_key=True, default=generate_uuid)
    tender_id = Column(String, ForeignKey("tenders.id"), nullable=False)
    category = Column(String, nullable=True) # technical_parameters, materials, performance, safety, environment
    attribute = Column(String, nullable=False) # e.g., flow_rate, head, power, efficiency
    value = Column(String, nullable=False) # e.g., 100, 50, 75
    unit = Column(String, nullable=True) # e.g., m3/hr, m, kW
    source_text = Column(Text, nullable=True)

    tender = relationship("Tender", back_populates="requirements")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=generate_uuid)
    tender_id = Column(String, ForeignKey("tenders.id"), nullable=False)
    requirement_id = Column(String, ForeignKey("requirements.id"), nullable=True)
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    classification = Column(String, nullable=False) # PRIMARY, SUPPORTING, NORMATIVE_REFERENCE, TEST_METHOD, SAFETY, INSTALLATION, TERMINOLOGY, RELATED
    retrieval_score = Column(Float, default=0.0)
    applicability_score = Column(Float, default=0.0)
    reasoning = Column(JSON, nullable=True) # List of strings
    evidence = Column(JSON, nullable=True) # List of evidence dicts

    tender = relationship("Tender", back_populates="recommendations")
    standard = relationship("Standard")
