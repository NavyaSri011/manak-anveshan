# pyrefly: ignore [missing-import]
from typing import List

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.database.models import Standard, StandardRelationship
from app.schemas.analysis import (
    RecommendationCard,
    EvidenceItem,
    ExtractedRequirementsResult,
)


CLASSIFICATIONS = [
    "PRIMARY",
    "SUPPORTING",
    "NORMATIVE_REFERENCE",
    "TEST_METHOD",
    "SAFETY",
    "INSTALLATION",
    "TERMINOLOGY",
    "RELATED",
    "POSSIBLY_APPLICABLE",
    "NOT_APPLICABLE",
]


class ApplicabilityEngineService:

    @staticmethod
    def classify_and_build_recommendation(
        db: Session,
        candidate: Standard,
        retrieval_score: float,
        extracted: ExtractedRequirementsResult,
    ) -> RecommendationCard:

        product = extracted.product or {}

        product_name = str(
            product.get("name", "")
        ).lower()

        product_category = str(
            product.get("category", "")
        ).lower()

        application = str(
            extracted.application or ""
        ).lower()

        technical_parameters = (
            extracted.technical_parameters or {}
        )

        title = (candidate.title or "").strip()
        scope = (candidate.scope or "").strip()

        title_lower = title.lower()
        scope_lower = scope.lower()

        title_scope = f"{title_lower} {scope_lower}"

        standard_category = (
            candidate.category or ""
        ).lower()

        standard_classification = (
            candidate.classification or ""
        ).upper()

        classification = "RELATED"

        reasons: List[str] = []
        evidence_items: List[EvidenceItem] = []

        # ---------------------------------------------------------
        # 1. Procurement domain
        # ---------------------------------------------------------

        lighting_context = (
            "lighting" in product_category
            or "street" in product_name
            or "road" in product_name
            or "luminaire" in product_name
            or "led street" in product_name
        )

        water_context = (
            "water" in product_category
            or "water" in product_name
            or "water" in application
        )

        pump_context = (
            "pump" in product_category
            or "pump" in product_name
            or "pump" in application
        )

        electrical_context = (
            "electrical" in product_category
            or "cable" in product_name
            or "motor" in product_name
            or "transformer" in product_name
            or "electrical" in product_name
        )

        # Explicit procurement product contexts. These signals are derived
        # from the tender item, never from the candidate standard title.
        procurement_text = f"{product_name} {product_category} {application}"

        solar_module_context = any(
            term in procurement_text
            for term in [
                "solar photovoltaic module",
                "photovoltaic module",
                "pv module",
                "solar module",
                "photovoltaic panel",
                "solar panel",
                "crystalline-silicon photovoltaic",
                "crystalline silicon photovoltaic",
            ]
        )

        motor_context = any(
            term in procurement_text
            for term in [
                "induction motor",
                "electric motor",
                "three-phase motor",
                "3-phase motor",
                "squirrel-cage motor",
                "squirrel cage motor",
            ]
        )

        transformer_context = any(
            term in procurement_text
            for term in [
                "transformer",
                "distribution transformer",
                "power transformer",
            ]
        )

        cable_context = any(
            term in procurement_text
            for term in [
                "cable",
                "wire",
                "conductor",
                "wire rod",
            ]
        )

        street_light_context = any(
            term in procurement_text.lower()
            for term in [
                "led street light",
                "led street lighting",
                "street light luminaire",
                "street lighting luminaire",
                "road lighting luminaire",
                "outdoor led luminaire",
            ]
        )

        # ---------------------------------------------------------
        # 2. Pump application context
        #
        # These signals are used to reject standards that require
        # a specific application context not present in the tender.
        # ---------------------------------------------------------

        pump_text = (
            f"{product_name} "
            f"{product_category} "
            f"{application} "
            f"{extracted.canonical_query or ''}"
        ).lower()

        solar_context = any(
            term in pump_text
            for term in [
                "solar pump",
                "solar pumping",
                "solar water pumping",
                "solar pv pump",
                "solar photovoltaic pump",
                "photovoltaic water pumping",
                "pv water pumping",
            ]
        )

        marine_context = any(
            term in pump_text
            for term in [
                "marine",
                "ship",
                "shipboard",
                "vessel",
                "offshore",
                "naval",
                "sea water",
                "seawater",
            ]
        )

        agricultural_context = any(
            term in pump_text
            for term in [
                "agricultural",
                "agriculture",
                "irrigation",
                "farm",
                "rural water supply",
                "rural water",
            ]
        )

        municipal_or_industrial_water_context = any(
            term in pump_text
            for term in [
                "municipal",
                "municipal water",
                "industrial water",
                "industrial water supply",
                "water supply",
                "clean water",
                "clear water",
                "potable water",
                "drinking water",
            ]
        )

        # ---------------------------------------------------------
        # 3. Explicit relationship evidence
        # ---------------------------------------------------------

        relationships = (
            db.query(StandardRelationship)
            .filter(
                StandardRelationship.target_standard_id
                == candidate.id
            )
            .all()
        )

        relationship_found = False

        for relationship in relationships:

            relationship_type = (
                relationship.relationship_type or ""
            ).upper()

            if relationship_type in [
                "TEST_METHOD",
                "SAFETY",
                "INSTALLATION",
                "NORMATIVE_REFERENCE",
            ]:

                classification = relationship_type
                relationship_found = True

                reasons.append(
                    "Linked through the standards relationship "
                    "graph as a "
                    f"{relationship_type.lower().replace('_', ' ')}."
                )

                if relationship.evidence:

                    evidence_items.append(
                        EvidenceItem(
                            source="BIS Standard Relationship Graph",
                            type="relationship",
                            reference=str(
                                relationship.evidence
                            ),
                        )
                    )

                break

        # ---------------------------------------------------------
        # 4. Lighting-specific exclusions
        # ---------------------------------------------------------

        lighting_conflicts = [
            "emergency lighting",
            "emergency luminaire",
            "emergency luminaires",
            "handlamp",
            "handlamps",
            "hand lamp",
            "hand lamps",
            "aerodrome lighting",
            "airfield lighting",
            "aircraft lighting",
            "stage lighting",
            "theatre lighting",
            "theater lighting",
            "decorative lighting",
            "indoor lighting",
            "medical lighting",
            "self-ballasted led lamp",
            "self-ballasted led lamps",
            "self ballasted led lamp",
            "self ballasted led lamps",
            "general lighting services",
        ]

        lighting_component_terms = [
            "lighting pole",
            "lighting poles",
            "street lighting pole",
            "street lighting poles",
            "concrete lighting pole",
            "prestressed concrete",
            "precast concrete",
            "pole for street lighting",
        ]

        conflicting_lighting_standard = False

        if lighting_context:

            if any(
                term in title_scope
                for term in lighting_conflicts
            ):
                conflicting_lighting_standard = True

            if any(
                term in title_scope
                for term in lighting_component_terms
            ):
                conflicting_lighting_standard = True

        # ---------------------------------------------------------
        # 5. Solar-PV-module contextual exclusions
        #
        # A solar-module tender must not promote standards whose primary
        # product is a motor, switchgear/controller, transformer, cable,
        # conductor, battery, inverter, or other unrelated equipment.
        # ---------------------------------------------------------

        street_light_context_conflict = False
        street_light_context_reason = None

        if street_light_context:
            unrelated_terms = [
                "transformer", "induction motor", "squirrel cage motor",
                "centrifugal pump", "photovoltaic module", "solar pv module",
                "cable", "wire rod", "switchgear", "contactor"
            ]
            if any(term in title_scope for term in unrelated_terms):
                street_light_context_conflict = True
                street_light_context_reason = (
                    "The candidate standard addresses a different product "
                    "domain and is not directly applicable to the LED "
                    "street-light luminaire."
                )

        solar_module_context_conflict = False
        solar_module_context_reason = None

        if solar_module_context:
            unrelated_solar_product_terms = [
                "motor",
                "motor starter",
                "motor controller",
                "motorstarters",
                "motor starters",
                "switchgear",
                "controlgear",
                "controller",
                "contactor",
                "contactors",
                "transformer",
                "cable",
                "wire rod",
                "wire rods",
                "electrical conductor",
                "conductors",
                "generator",
                "battery",
                "accumulator",
                "inverter",
            ]

            if any(term in title_lower for term in unrelated_solar_product_terms):
                solar_module_context_conflict = True
                solar_module_context_reason = (
                    "The tender is for a solar photovoltaic module, "
                    "but the candidate standard primarily specifies "
                    "a different electrical product or equipment type."
                )

        # ---------------------------------------------------------
        # 6. Pump-specific contextual exclusions
        #
        # A semantic match is not sufficient when the standard title
        # explicitly requires a different application domain.
        # ---------------------------------------------------------

        pump_context_conflict = False
        pump_context_reason = None

        if pump_context:

            # Solar/PV pump standards require solar/PV context.
            if (
                any(
                    term in title_scope
                    for term in [
                        "solar photovoltaic",
                        "solar pv",
                        "photovoltaic water pumping",
                        "pv water pumping",
                        "solar water pumping",
                        "photovoltaic",
                    ]
                )
                and not solar_context
            ):
                pump_context_conflict = True
                pump_context_reason = (
                    "The standard is specific to solar or photovoltaic "
                    "water pumping, but the tender does not specify a "
                    "solar/PV pumping system."
                )

            # Marine pump standards require marine/ship/offshore context.
            elif (
                any(
                    term in title_scope
                    for term in [
                        "marine use",
                        "marine",
                        "ship",
                        "shipboard",
                        "naval",
                        "offshore",
                    ]
                )
                and not marine_context
            ):
                pump_context_conflict = True
                pump_context_reason = (
                    "The standard is specific to marine, shipboard, "
                    "naval, or offshore use, but the tender specifies "
                    "municipal/industrial water-supply service."
                )

            # Agricultural/rural pump standards require that context.
            elif (
                any(
                    term in title_scope
                    for term in [
                        "agricultural",
                        "agriculture",
                        "agricultural and rural",
                        "rural water supply",
                        "irrigation",
                    ]
                )
                and not agricultural_context
            ):
                pump_context_conflict = True
                pump_context_reason = (
                    "The standard is specific to agricultural, irrigation, "
                    "or rural water-supply applications, but that context "
                    "is not stated in the tender."
                )

        # ---------------------------------------------------------
        # 6. Identify governing street-lighting standard
        # ---------------------------------------------------------

        governing_lighting_standard = False

        if lighting_context:

            governing_phrases = [
                "luminaires for road and street lighting",
                "luminaires for road lighting",
                "luminaires for street lighting",
                "road and street lighting luminaires",
            ]

            if any(
                phrase in title_lower
                for phrase in governing_phrases
            ):
                governing_lighting_standard = True

        # ---------------------------------------------------------
        # 7. Identify secondary LED performance standards
        # ---------------------------------------------------------

        secondary_lighting_standard = False

        if lighting_context:

            if (
                "led street lighting" in title_lower
                and not governing_lighting_standard
            ):
                secondary_lighting_standard = True

        # ---------------------------------------------------------
        # 8. Detect test / measurement standards
        # ---------------------------------------------------------

        test_method_standard = False

        test_method_indicators = [
            "methods of tests",
            "method of tests",
            "method of test",
            "methods of test",
            "method of measurement",
            "methods of measurement",
            "test method",
            "test methods",
            "testing method",
            "testing methods",
            "photometry",
        ]

        if (
            standard_classification == "TEST_METHOD"
            or standard_category == "methods of tests"
            or any(
                indicator in title_scope
                for indicator in test_method_indicators
            )
        ):
            test_method_standard = True

        # ---------------------------------------------------------
        # 9. Detect older lighting revision
        # ---------------------------------------------------------

        older_revision = False

        if lighting_context:

            if (
                "first revision" in title_lower
                and (
                    "luminaires for road and street lighting"
                    in title_lower
                    or "luminaires: part 5 particular requirements"
                    in title_lower
                    or "luminaires part 5 particular requirements"
                    in title_lower
                )
            ):

                newer_revision_exists = (
                    db.query(Standard)
                    .filter(
                        Standard.id != candidate.id,
                        Standard.title.ilike(
                            "%Luminaires Part 5%"
                        ),
                        Standard.title.ilike(
                            "%road and street lighting%"
                        ),
                        Standard.title.ilike(
                            "%Second Revision%"
                        ),
                    )
                    .first()
                    is not None
                )

                if newer_revision_exists:
                    older_revision = True

        # ---------------------------------------------------------
        # 10. Pump-specific product specification detection
        # ---------------------------------------------------------

        pump_product_specification = False

        if pump_context:

            pump_product_terms = [
                "centrifugal pump",
                "centrifugal pumps",
                "rotodynamic pump",
                "rotodynamic pumps",
                "horizontal centrifugal pump",
                "horizontal centrifugal pumps",
                "clear, cold water",
                "clear cold water",
            ]

            if (
                standard_category == "product specification"
                and any(
                    term in title_lower
                    for term in pump_product_terms
                )
            ):

                pump_product_specification = True

        # ---------------------------------------------------------
        # 11. Pump supporting general centrifugal-pump standards
        # ---------------------------------------------------------

        pump_general_standard = False

        if pump_context:

            if (
                "centrifugal pumps" in title_lower
                or "centrifugal pump" in title_lower
            ):

                if (
                    "technical specifications" in title_lower
                    or "class ii" in title_lower
                    or "general requirements" in title_lower
                ):
                    pump_general_standard = True

        # ---------------------------------------------------------
        # 12. Classification
        # ---------------------------------------------------------

        if not relationship_found:

            # ---------------------------------------------
            # WRONG LIGHTING SUB-DOMAIN
            # ---------------------------------------------

            if conflicting_lighting_standard:

                classification = "RELATED"

                reasons.append(
                    "Related lighting standard detected, but its "
                    "scope concerns a different lighting application "
                    "or a separate physical component."
                )

            # ---------------------------------------------
            # WRONG PUMP APPLICATION CONTEXT
            # ---------------------------------------------

            elif solar_module_context_conflict:

                classification = "RELATED"

                reasons.append(
                    solar_module_context_reason
                    or
                    "The candidate standard addresses a different electrical "
                    "product than the solar photovoltaic module."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="Procurement Context Applicability Check",
                        type="applicability",
                        reference=(
                            "Candidate was downgraded because its product type "
                            "does not match the solar photovoltaic module "
                            "being procured."
                        ),
                    )
                )

            elif pump_context_conflict:

                classification = "RELATED"

                reasons.append(
                    pump_context_reason
                    or
                    "The standard addresses a pump application "
                    "context that is not stated in the tender."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="Procurement Context Applicability Check",
                        type="applicability",
                        reference=(
                            "Candidate was downgraded because its "
                            "application-specific scope does not "
                            "match the stated procurement context."
                        ),
                    )
                )

            # ---------------------------------------------
            # TEST / MEASUREMENT STANDARD
            # ---------------------------------------------

            elif test_method_standard:

                classification = "TEST_METHOD"

                reasons.append(
                    "Provides standardized testing or measurement "
                    "methods relevant to the procurement item. "
                    "It is not the governing product specification."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="test_method",
                        reference=(
                            "Standard identified as a testing or "
                            "measurement method rather than a "
                            "governing product specification."
                        ),
                    )
                )

            # ---------------------------------------------
            # OLDER REVISION OF GOVERNING LIGHTING STANDARD
            # ---------------------------------------------

            elif older_revision:

                classification = "RELATED"

                reasons.append(
                    "Earlier revision of the governing "
                    "street-lighting standard. The newer revision "
                    "should be used for current procurement "
                    "verification."
                )

            # ---------------------------------------------
            # GOVERNING ROAD/STREET LUMINAIRE STANDARD
            # ---------------------------------------------

            elif governing_lighting_standard:

                classification = "PRIMARY"

                reasons.append(
                    "Governing product specification for luminaires "
                    "used in road and street lighting."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="governing_standard",
                        reference=(
                            "Direct governing-standard match for "
                            "road and street lighting luminaires."
                        ),
                    )
                )

            # ---------------------------------------------
            # SECONDARY LED STREET-LIGHTING PERFORMANCE STANDARD
            # ---------------------------------------------

            elif secondary_lighting_standard:

                classification = "SUPPORTING"

                reasons.append(
                    "LED street-lighting performance requirements "
                    "are relevant to the procurement item, but the "
                    "standard is treated as supporting to the "
                    "governing road/street luminaire specification."
                )

            # ---------------------------------------------
            # DIRECT PRODUCT SPECIFICATION — LED STREET LIGHT
            # ---------------------------------------------

            elif (
                standard_category == "product specification"
                and street_light_context
                and (
                    "street light" in title_lower
                    or "street lighting" in title_lower
                    or "road lighting" in title_lower
                    or "luminaire" in title_lower
                )
                and not any(
                    term in title_lower
                    for term in [
                        "transformer", "motor", "centrifugal pump",
                        "photovoltaic module", "solar pv module",
                        "cable", "wire rod"
                    ]
                )
            ):
                classification = "PRIMARY"
                reasons.append(
                    "Product specification directly identifies the "
                    "procured LED street-light/road-lighting luminaire."
                )
                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="governing_standard",
                        reference="Direct LED street-light luminaire product specification match.",
                    )
                )

            # ---------------------------------------------
            # PUMP PRODUCT SPECIFICATION
            # ---------------------------------------------

            elif pump_product_specification:

                classification = "PRIMARY"

                reasons.append(
                    "Product specification directly identifies "
                    "the centrifugal pump product and is relevant "
                    "to the stated water-supply application."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="governing_standard",
                        reference=(
                            "Direct centrifugal-pump product "
                            "specification match."
                        ),
                    )
                )

            # ---------------------------------------------
            # GENERAL CENTRIFUGAL-PUMP STANDARD
            # ---------------------------------------------

            elif pump_general_standard:

                classification = "SUPPORTING"

                reasons.append(
                    "Provides general technical requirements for "
                    "centrifugal pumps and is treated as supporting "
                    "rather than as the governing product specification."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="supporting_standard",
                        reference=(
                            "General centrifugal-pump technical "
                            "standard identified as supporting."
                        ),
                    )
                )

            # ---------------------------------------------
            # SAFETY
            # ---------------------------------------------

            elif (
                standard_classification == "SAFETY"
                or "safety requirements" in title_scope
                or "safety standard" in standard_category
            ):

                classification = "SAFETY"

                reasons.append(
                    "Addresses safety requirements relevant to "
                    "the procurement item's technical domain."
                )

            # ---------------------------------------------
            # INSTALLATION / CODE OF PRACTICE
            # ---------------------------------------------

            elif (
                "installation" in title_scope
                or "erection" in title_scope
                or "code of practice" in title_scope
            ):

                classification = "INSTALLATION"

                reasons.append(
                    "Provides installation, engineering, erection, "
                    "or field-practice requirements."
                )

            # ---------------------------------------------
            # TERMINOLOGY
            # ---------------------------------------------

            elif (
                standard_category == "terminology"
                or "terminology" in title_scope
                or "vocabulary" in title_scope
            ):

                classification = "TERMINOLOGY"

                reasons.append(
                    "Provides terminology or vocabulary relevant "
                    "to the procurement domain."
                )

            # ---------------------------------------------
            # DIRECT PRODUCT SPECIFICATION — WATER
            # ---------------------------------------------

            elif (
                standard_category == "product specification"
                and water_context
                and (
                    "drinking water" in title_lower
                    or "packaged drinking water" in title_lower
                    or "packaged water" in title_lower
                    or "natural mineral water" in title_lower
                )
            ):

                classification = "PRIMARY"

                reasons.append(
                    "Product specification directly identifies "
                    "the procured water product."
                )

            # ---------------------------------------------
            # DIRECT PRODUCT SPECIFICATION — SOLAR PV MODULE
            # ---------------------------------------------

            elif (
                standard_category == "product specification"
                and solar_module_context
                and (
                    "photovoltaic module" in title_lower
                    or "photovoltaic modules" in title_lower
                    or "pv module" in title_lower
                    or "pv modules" in title_lower
                    or "solar photovoltaic" in title_lower
                )
                and not any(
                    term in title_lower
                    for term in [
                        "pump",
                        "water pumping",
                        "motor",
                        "switchgear",
                        "controlgear",
                        "controller",
                        "contactor",
                        "transformer",
                        "cable",
                        "wire rod",
                    ]
                )
            ):

                classification = "PRIMARY"

                reasons.append(
                    "Product specification directly identifies "
                    "the procured solar photovoltaic module."
                )

                evidence_items.append(
                    EvidenceItem(
                        source="BIS Standard Catalogue",
                        type="governing_standard",
                        reference=(
                            "Direct solar photovoltaic module "
                            "product specification match."
                        ),
                    )
                )

            # ---------------------------------------------
            # DIRECT PRODUCT SPECIFICATION — ELECTRICAL
            # ---------------------------------------------

            elif (
                standard_category == "product specification"
                and electrical_context
                and not solar_module_context
                and (
                    "cable" in title_lower
                    or "wire" in title_lower
                    or "transformer" in title_lower
                    or "motor" in title_lower
                )
            ):

                classification = "PRIMARY"

                reasons.append(
                    "Product specification directly identifies "
                    "the procured electrical product."
                )

            # ---------------------------------------------
            # SYSTEM STANDARDS
            # ---------------------------------------------

            elif standard_category == "system standard":

                classification = "SUPPORTING"

                reasons.append(
                    "Provides system-level requirements relevant "
                    "to the procurement domain."
                )

            # ---------------------------------------------
            # CODE OF PRACTICE
            # ---------------------------------------------

            elif standard_category == "code of practice":

                classification = "SUPPORTING"

                reasons.append(
                    "Provides engineering or field-practice "
                    "requirements related to the procurement."
                )

            # ---------------------------------------------
            # DEFAULT
            # ---------------------------------------------

            else:

                classification = "RELATED"

                reasons.append(
                    "Related standard identified through "
                    "technical-domain relevance."
                )

        # ---------------------------------------------------------
        # 13. Scope evidence
        # ---------------------------------------------------------

        if scope:

            evidence_items.append(
                EvidenceItem(
                    source="Bureau of Indian Standards Scope",
                    type="scope",
                    reference=(
                        f"{candidate.is_number}: "
                        f"{scope[:300]}"
                    ),
                )
            )

        # ---------------------------------------------------------
        # 14. Technical parameter evidence
        # ---------------------------------------------------------

        parameter_matches = []

        for key, value in technical_parameters.items():

            key_text = str(key).lower()
            value_text = str(value).lower()

            if (
                key_text in title_scope
                or value_text in title_scope
            ):

                parameter_matches.append(
                    f"{key}: {value}"
                )

        if parameter_matches:

            reasons.append(
                "Matches tender parameters: "
                + ", ".join(parameter_matches[:3])
                + "."
            )

            evidence_items.append(
                EvidenceItem(
                    source="Procurement Tender Requirement Match",
                    type="technical_match",
                    reference=(
                        "Matched parameters: "
                        + ", ".join(parameter_matches[:5])
                    ),
                )
            )

        # ---------------------------------------------------------
        # 15. Explicit application evidence
        # ---------------------------------------------------------

        if application:

            application_indicators = [
                "water supply",
                "municipal",
                "industrial",
                "clean water",
                "clear water",
                "continuous",
                "agricultural",
                "irrigation",
                "solar",
                "photovoltaic",
                "marine",
            ]

            matched_application_terms = [
                term
                for term in application_indicators
                if term in application
            ]

            if matched_application_terms:

                evidence_items.append(
                    EvidenceItem(
                        source="Extracted Tender Application",
                        type="application",
                        reference=(
                            "Application context detected: "
                            + ", ".join(
                                matched_application_terms
                            )
                        ),
                    )
                )

        # ---------------------------------------------------------
        # 16. Lifecycle
        # ---------------------------------------------------------

        lifecycle_alert = None

        if candidate.status == "SUPERSEDED":

            lifecycle_alert = (
                f"WARNING: {candidate.is_number} is SUPERSEDED. "
                f"It has been replaced by "
                f"{candidate.replaced_by_is or 'a revised edition'}. "
                "Verify the tender specification before procurement."
            )

        # ---------------------------------------------------------
        # 17. Publication information
        # ---------------------------------------------------------

        publication_info = (
            f"Published: "
            f"{candidate.publication_date or 'N/A'}"
        )

        if candidate.revision_date:

            publication_info += (
                f" | Reaffirmed/Revised: "
                f"{candidate.revision_date}"
            )

        # ---------------------------------------------------------
        # 18. Final product-domain safety guard
        #
        # Retrieval/relationship evidence must never turn an unrelated
        # electrical product into a PRIMARY recommendation for a solar
        # photovoltaic module tender.
        # ---------------------------------------------------------

        if solar_module_context and classification == "PRIMARY":
            unrelated_primary_terms = [
                "motor",
                "motor starter",
                "motor controller",
                "motorstarters",
                "motor starters",
                "switchgear",
                "controlgear",
                "controller",
                "contactor",
                "contactors",
                "transformer",
                "cable",
                "wire rod",
                "wire rods",
                "electrical conductor",
                "conductors",
                "generator",
                "battery",
                "accumulator",
                "inverter",
            ]

            is_actual_pv_module_standard = any(
                term in title_lower
                for term in [
                    "photovoltaic module",
                    "photovoltaic modules",
                    "pv module",
                    "pv modules",
                    "solar photovoltaic",
                ]
            )

            if (
                any(term in title_lower for term in unrelated_primary_terms)
                and not is_actual_pv_module_standard
            ):
                classification = "RELATED"
                reasons.append(
                    "Final product-domain safeguard: this standard does not "
                    "specify the procured solar photovoltaic module."
                )

        # ---------------------------------------------------------
        # 19. Recommendation card
        # ---------------------------------------------------------

        return RecommendationCard(
            id=candidate.id,
            is_number=candidate.is_number,
            title=candidate.title,
            scope=candidate.scope,
            status=candidate.status,
            publication_info=publication_info,
            category=candidate.category,
            classification=classification,
            confidence_score=retrieval_score,
            reason=reasons,
            evidence=evidence_items,
            lifecycle_alert=lifecycle_alert,
            certification_info=None,
            source=candidate.source,
            source_url=candidate.source_url,
            source_type=candidate.source_type,
            last_verified=candidate.publication_date,
        )
