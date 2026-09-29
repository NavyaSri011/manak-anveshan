from typing import List, Dict, Any
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.database.models import Standard, Amendment


class LifecycleService:

    @staticmethod
    def audit_lifecycle_and_alerts(
        db: Session,
        query_text: str,
        recommendation_cards: List[Any]
    ) -> List[Dict[str, Any]]:

        alerts = []
        lower_query = query_text.lower()

        # 1. Detect if tender explicitly references a SUPERSEDED standard by IS number
        superseded_standards = db.query(Standard).filter(Standard.status == "SUPERSEDED").all()
        for sup in superseded_standards:
            sup_num_clean = sup.is_number.split(":")[0].lower()  # e.g. "is 325"
            if sup_num_clean in lower_query or sup.is_number.lower() in lower_query:
                replacement_note = (
                    f"Replace {sup.is_number} with {sup.replaced_by_is}"
                    if sup.replaced_by_is
                    else f"Remove the superseded reference to {sup.is_number} and consult the current revision."
                )
                alerts.append({
                    "is_number": sup.is_number,
                    "type": "SUPERSEDED_TENDER_REFERENCE",
                    "severity": "HIGH",
                    "title": f"Outdated Tender Reference Detected: {sup.is_number}",
                    "message": (
                        f"This tender refers to {sup.is_number} which has been officially SUPERSEDED"
                        f" by {sup.replaced_by_is or 'a newer revised standard'}."
                        f" Verify applicability before finalising the tender specification."
                    ),
                    "replacement": sup.replaced_by_is,
                    "action_required": replacement_note
                })

        # 2. Report active amendments for any recommended standard
        for card in recommendation_cards:
            std = db.query(Standard).filter(Standard.id == card.id).first()
            if std and std.amendments:
                latest_am = std.amendments[-1]
                alerts.append({
                    "is_number": std.is_number,
                    "type": "AMENDMENT_ALERT",
                    "severity": "INFO",
                    "title": f"Active Amendment #{latest_am.amendment_number} for {std.is_number}",
                    "message": (
                        f"Amendment #{latest_am.amendment_number} issued on"
                        f" {latest_am.date or 'N/A'}: {latest_am.description}"
                    ),
                    "source": latest_am.source
                })

        return alerts
