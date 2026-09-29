from typing import List, Dict

from app.schemas.analysis import (
    MissingRequirementAlert,
    ExtractedRequirementsResult,
)


# Domain-specific expected parameters for gap detection.
#
# These are procurement completeness checks.
# They do NOT prescribe a numeric value unless that value is
# explicitly supported by an authoritative standard/rule elsewhere
# in the system.
DOMAIN_EXPECTED_PARAMS: Dict[str, List[Dict[str, str]]] = {

    "Pressure Vessels & Process Equipment": [
        {
            "attribute": "design_pressure",
            "importance": "HIGH",
            "impact": (
                "Determines pressure class, shell thickness, and "
                "applicable pressure-vessel standard requirements."
            ),
            "message": (
                "Design pressure (bar / kg/cm²) not specified. "
                "Required for pressure-vessel technical classification."
            ),
        },
        {
            "attribute": "operating_temperature",
            "importance": "HIGH",
            "impact": (
                "Affects material selection and design requirements "
                "for pressure-containing equipment."
            ),
            "message": (
                "Operating temperature not specified. "
                "Required for material and design verification."
            ),
        },
        {
            "attribute": "material_of_construction",
            "importance": "MEDIUM",
            "impact": (
                "Material selection affects corrosion allowance, "
                "fabrication, and service compatibility."
            ),
            "message": (
                "Vessel shell material not specified."
            ),
        },
        {
            "attribute": "ndt_requirements",
            "importance": "MEDIUM",
            "impact": (
                "Non-destructive examination requirements affect "
                "fabrication and weld-quality verification."
            ),
            "message": (
                "NDT extent or method not specified."
            ),
        },
    ],

    "Pumps & Fluid Handling": [
        {
            "attribute": "operating_temperature",
            "importance": "HIGH",
            "impact": (
                "Fluid temperature affects pump material, sealing, "
                "and operating conditions."
            ),
            "message": (
                "Fluid operating temperature not specified."
            ),
        },
        {
            "attribute": "fluid_characteristics",
            "importance": "HIGH",
            "impact": (
                "Fluid properties affect pump selection, materials, "
                "sealing, and hydraulic performance."
            ),
            "message": (
                "Fluid characteristics such as viscosity and "
                "solid content are not specified."
            ),
        },
        {
            "attribute": "material_of_construction",
            "importance": "MEDIUM",
            "impact": (
                "Casing and impeller material affects corrosion "
                "resistance and service compatibility."
            ),
            "message": (
                "Pump material grade is not explicitly specified."
            ),
        },
        {
            "attribute": "casing_working_pressure",
            "importance": "MEDIUM",
            "impact": (
                "Maximum casing pressure is required for mechanical "
                "integrity and pressure verification."
            ),
            "message": (
                "Maximum casing working pressure is not specified."
            ),
        },
    ],

    "Electrical Motors & Drives": [
        {
            "attribute": "efficiency_class",
            "importance": "HIGH",
            "impact": (
                "Motor efficiency classification affects energy "
                "performance and applicable regulatory requirements."
            ),
            "message": (
                "Energy efficiency class is not specified."
            ),
        },
        {
            "attribute": "enclosure_ip_rating",
            "importance": "MEDIUM",
            "impact": (
                "Ingress protection affects suitability for the "
                "specified installation environment."
            ),
            "message": (
                "Motor enclosure IP rating is not specified."
            ),
        },
        {
            "attribute": "insulation_class",
            "importance": "MEDIUM",
            "impact": (
                "Insulation classification affects thermal endurance "
                "and motor service life."
            ),
            "message": (
                "Motor insulation class is not specified."
            ),
        },
    ],

    "Solar Energy Systems": [
        {
            "attribute": "almm_enlistment",
            "importance": "HIGH",
            "impact": (
                "Applicable government procurement requirements may "
                "require verification of manufacturer/model eligibility."
            ),
            "message": (
                "Applicable manufacturer/model eligibility or "
                "ALMM status is not specified."
            ),
        },
        {
            "attribute": "system_voltage",
            "importance": "MEDIUM",
            "impact": (
                "Maximum system voltage affects system configuration "
                "and equipment selection."
            ),
            "message": (
                "Maximum system voltage is not specified."
            ),
        },
    ],

    "Electrical Cables & Wiring": [
        {
            "attribute": "voltage_rating",
            "importance": "HIGH",
            "impact": (
                "Working voltage determines applicable cable "
                "construction and standard requirements."
            ),
            "message": (
                "Working voltage rating is not specified."
            ),
        },
        {
            "attribute": "conductor_material",
            "importance": "MEDIUM",
            "impact": (
                "Conductor material affects electrical and mechanical "
                "characteristics and applicable product requirements."
            ),
            "message": (
                "Conductor material is not specified."
            ),
        },
        {
            "attribute": "insulation_type",
            "importance": "MEDIUM",
            "impact": (
                "Insulation construction affects operating conditions "
                "and applicable cable requirements."
            ),
            "message": (
                "Insulation type is not specified."
            ),
        },
    ],

    "Lighting & Electrical Systems": [
        {
            "attribute": "ip_rating",
            "importance": "HIGH",
            "impact": (
                "Ingress protection is an important procurement "
                "parameter for outdoor lighting equipment."
            ),
            "message": (
                "IP rating is not specified for the outdoor "
                "lighting equipment."
            ),
        },
        {
            "attribute": "colour_rendering_index",
            "importance": "MEDIUM",
            "impact": (
                "Colour Rendering Index is a relevant photometric "
                "parameter for evaluating lighting performance."
            ),
            "message": (
                "Colour Rendering Index (CRI) is not specified."
            ),
        },
        {
            "attribute": "colour_temperature",
            "importance": "MEDIUM",
            "impact": (
                "Correlated Colour Temperature is a relevant "
                "photometric parameter for lighting selection."
            ),
            "message": (
                "Correlated Colour Temperature (CCT) is not specified."
            ),
        },
    ],

    "IT & Computing Infrastructure": [
        {
            "attribute": "energy_efficiency",
            "importance": "HIGH",
            "impact": (
                "Energy-efficiency requirements may affect "
                "government procurement compliance."
            ),
            "message": (
                "Applicable energy-efficiency requirement or "
                "rating is not specified."
            ),
        },
        {
            "attribute": "warranty_period",
            "importance": "MEDIUM",
            "impact": (
                "Warranty requirements define supplier support "
                "and post-procurement coverage."
            ),
            "message": (
                "Warranty period and support coverage are not "
                "explicitly specified."
            ),
        },
        {
            "attribute": "operating_system",
            "importance": "MEDIUM",
            "impact": (
                "Operating-system requirements affect software "
                "compatibility and licensing."
            ),
            "message": (
                "Operating system requirement is not specified."
            ),
        },
    ],

    "Tanks & Storage Systems": [
        {
            "attribute": "capacity",
            "importance": "HIGH",
            "impact": (
                "Tank capacity determines sizing and applicable "
                "design requirements."
            ),
            "message": (
                "Storage tank capacity is not specified."
            ),
        },
        {
            "attribute": "material_grade",
            "importance": "HIGH",
            "impact": (
                "Material selection affects corrosion resistance, "
                "service compatibility, and product suitability."
            ),
            "message": (
                "Tank material grade is not specified."
            ),
        },
        {
            "attribute": "installation_type",
            "importance": "MEDIUM",
            "impact": (
                "Installation configuration affects structural, "
                "access, and installation requirements."
            ),
            "message": (
                "Tank installation type is not specified."
            ),
        },
    ],

    "Laboratory & Medical Testing": [
        {
            "attribute": "rotor_speed",
            "importance": "HIGH",
            "impact": (
                "Maximum rotor speed is important for equipment "
                "performance and safety verification."
            ),
            "message": (
                "Maximum centrifuge rotor speed is not specified."
            ),
        },
        {
            "attribute": "capacity_per_run",
            "importance": "MEDIUM",
            "impact": (
                "Run capacity affects throughput and equipment "
                "selection."
            ),
            "message": (
                "Centrifuge tube capacity per run is not specified."
            ),
        },
        {
            "attribute": "safety_certification",
            "importance": "HIGH",
            "impact": (
                "Applicable medical or laboratory safety requirements "
                "must be verified for the intended use."
            ),
            "message": (
                "Applicable safety certification or approval status "
                "is not specified."
            ),
        },
    ],

    "Pipes, Valves & Fittings": [
        {
            "attribute": "pressure_rating",
            "importance": "HIGH",
            "impact": (
                "Nominal pressure rating determines the applicable "
                "pipe or valve pressure class."
            ),
            "message": (
                "Nominal pressure rating is not specified."
            ),
        },
        {
            "attribute": "material_grade",
            "importance": "HIGH",
            "impact": (
                "Material selection affects corrosion resistance "
                "and fluid compatibility."
            ),
            "message": (
                "Pipe or valve material grade is not specified."
            ),
        },
        {
            "attribute": "end_connections",
            "importance": "MEDIUM",
            "impact": (
                "Connection type must be compatible with mating "
                "equipment and installation requirements."
            ),
            "message": (
                "End connection type is not specified."
            ),
        },
    ],
}


# Generic checks applied when domain-specific rules are unavailable.
#
# These checks are procurement-completeness checks rather than
# product-specific technical prescriptions.
GENERIC_EXPECTED_PARAMS = [
    {
        "attribute": "quantity",
        "importance": "MEDIUM",
        "impact": (
            "Procurement quantity affects lot testing, inspection, "
            "and sampling considerations."
        ),
        "message": (
            "Procurement quantity not specified."
        ),
    },
    {
        "attribute": "applicable_standards",
        "importance": "HIGH",
        "impact": (
            "Explicit IS references in a tender reduce ambiguity "
            "during compliance verification."
        ),
        "message": (
            "Applicable Indian Standards (IS numbers) are not "
            "explicitly mentioned in the tender specification."
        ),
    },
]


class MissingRequirementService:

    @staticmethod
    def detect_missing_requirements(
        extracted: ExtractedRequirementsResult,
    ) -> List[MissingRequirementAlert]:

        missing: List[MissingRequirementAlert] = []

        product = extracted.product or {}

        category = str(
            product.get("category", "")
        ).strip()

        technical_parameters = (
            extracted.technical_parameters or {}
        )

        provided_keys = [
            str(key).lower().strip()
            for key in technical_parameters.keys()
        ]

        # ---------------------------------------------------------
        # Domain-specific rules
        # ---------------------------------------------------------

        expected_rules = DOMAIN_EXPECTED_PARAMS.get(
            category,
            []
        )

        # ---------------------------------------------------------
        # Generic procurement checks
        # ---------------------------------------------------------

        all_rules = (
            expected_rules
            + GENERIC_EXPECTED_PARAMS
        )

        # ---------------------------------------------------------
        # Detect missing attributes
        # ---------------------------------------------------------

        for rule in all_rules:

            rule_attr = (
                rule["attribute"]
                .lower()
                .strip()
            )

            found = any(
                rule_attr in key
                or key in rule_attr
                for key in provided_keys
            )

            if not found:

                missing.append(
                    MissingRequirementAlert(
                        attribute=(
                            rule["attribute"]
                            .replace("_", " ")
                            .title()
                        ),
                        importance=rule["importance"],
                        impact=rule["impact"],
                        message=rule["message"],
                    )
                )

        return missing
