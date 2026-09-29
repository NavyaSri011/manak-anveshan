from typing import List, Dict, Any
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.database.models import CertificationRule, Standard
from app.schemas.analysis import EvidenceItem

class CertificationEngineService:

    @staticmethod
    def get_certification_status(
        db: Session,
        standard: Standard
    ) -> Dict[str, Any]:
        
        rule = db.query(CertificationRule).filter(
            CertificationRule.standard_id == standard.id
        ).first()

        if not rule:
            return {
                "status": "Verify",
                "scheme": "VERIFICATION REQUIRED",
                "mandatory": False,
                "conditions": "No authoritative evidence of a Quality Control Order (QCO) identified. Verification required.",
                "source": "BIS Official Public Register"
            }

        return {
            "status": "Applicable" if rule.mandatory else "Verify",
            "scheme": rule.scheme,
            "mandatory": rule.mandatory,
            "conditions": rule.conditions,
            "source": rule.source
        }

    @staticmethod
    def attach_certification_evidence(
        db: Session,
        cards: List[Any]
    ) -> List[Dict[str, Any]]:
        
        summary = []
        for card in cards:
            std = db.query(Standard).filter(Standard.id == card.id).first()
            if std:
                cert_info = CertificationEngineService.get_certification_status(db, std)
                card.certification_info = cert_info
                
                if cert_info["status"] == "Applicable":
                    card.evidence.append(EvidenceItem(
                        source=cert_info["source"],
                        type="qco_gazette",
                        reference=f"{cert_info['scheme']} - {cert_info['conditions']}"
                    ))
                    summary.append({
                        "is_number": std.is_number,
                        "product": std.title,
                        "scheme": cert_info["scheme"],
                        "status": cert_info["status"],
                        "conditions": cert_info["conditions"],
                        "source": cert_info["source"]
                    })
        return summary
