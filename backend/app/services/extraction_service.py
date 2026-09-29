# pyrefly: ignore [missing-import]
import re
import io
from typing import Dict, Any, List
from app.schemas.analysis import ExtractedRequirementsResult, RequirementItem

MULTILINGUAL_TRANSLATIONS = {
    # Hindi
    "सेंट्रीफ्यूगल पंप": "centrifugal pump",
    "पंप": "pump",
    "विद्युत मोटर": "electric motor",
    "इंडक्शन मोटर": "induction motor",
    "मोटर": "motor",
    "तीन-फेज़": "three phase",
    "तीन फेज": "three phase",
    "ट्रान्सफॉर्मर": "transformer",
    "वितरण ट्रांसफॉर्मर": "distribution transformer",
    "सौर पैनल": "solar pv module",
    "सोलर मॉड्यूल": "solar pv module",
    "बैटरी": "battery",
    "वॉल्व": "valve",
    "पाइप": "pipe",
    "पानी की आपूर्ति": "water supply",
    "औद्योगिक": "industrial",
    "निरंतर ड्यूटी": "continuous duty",
    "ऊर्जा दक्षता": "energy efficiency",
    "किलोवाट": "kW",
    "वोल्ट": "V",
    "हर्ट्ज़": "Hz",
    "हर्ट्ज": "Hz",
    "केवीए": "kVA",
    "बार": "bar",
    "मीटर": "meter",

    # Tamil
    "மையவிலக்கு பம்ப்": "centrifugal pump",
    "பம்ப்": "pump",
    "மின்சார மோட்டார்": "electric motor",
    "தூண்டல் மோட்டார்": "induction motor",
    "மூன்று கட்ட": "three phase",
    "மின்மாற்றி": "transformer",
    "விநியோக மின்மாற்றி": "distribution transformer",
    "குழாய்": "pipe",
    "வால்வு": "valve",
    "தொழில்துறை": "industrial",
    "கிலோவாட்": "kW",
    "வோல்ட்": "V",
    "ஹெர்ட்ஸ்": "Hz",

    # Marathi
    "केंद्रापसारी पंप": "centrifugal pump",
    "पंप": "pump",
    "विद्युत मोटर": "electric motor",
    "इंडक्शन मोटर": "induction motor",
    "तीन फेज": "three phase",
    "ट्रान्सफॉर्मर": "transformer",
    "वितरण ट्रान्सफॉर्मर": "distribution transformer",
    "पाईप": "pipe",
    "झडप": "valve",
    "औद्योगिक": "industrial",
    "किलोवॅट": "kW",
    "व्होल्ट": "V",
    "हर्ट्झ": "Hz",

    # Telugu
    "సెంట్రిఫ్యూగల్ పంప్": "centrifugal pump",
    "పంప్": "pump",
    "విద్యుత్ మోటార్": "electric motor",
    "ఇండక్షన్ మోటార్": "induction motor",
    "మూడు దశల": "three phase",
    "ట్రాన్స్‌ఫార్మర్": "transformer",
    "పంపిణీ ట్రాన్స్‌ఫార్మర్": "distribution transformer",
    "పైపు": "pipe",
    "వాల్వ్": "valve",
    "పారిశ్రామిక": "industrial",
    "కిలోవాట్": "kW",
    "వోల్ట్": "V",
    "హెర్ట్జ్": "Hz",
}


PARAM_PATTERNS = {
    "flow_rate": r"\b(\d+(?:\.\d+)?)\s*(m3/hr|m³/h|m3/h|lps|gpm|l/min)\b",
    "head": r"\b(\d+(?:\.\d+)?)\s*(m|meter|meters|metres)\s*(?:head)?\b",
    "power": r"\b(\d+(?:\.\d+)?)\s*(kw|hp|mw)\b",
    "voltage": r"\b(\d+(?:\.\d+)?)\s*(v|kv|volts)\b",
    "efficiency": r"\b(ie[1-4]|eff[1-4]?|\d+%\s*efficiency)\b",
    "capacity": r"\b(\d+(?:\.\d+)?)\s*(kva|mva|ah)\b",
    "pressure": r"\b(\d+(?:\.\d+)?)\s*(bar|kg/cm2|pn\d+)\b"
}


def extract_text_from_file_bytes(file_bytes: bytes, filename: str) -> str:
    filename_lower = filename.lower()
    text = ""

    if filename_lower.endswith(".pdf"):
        try:
            # pyrefly: ignore [missing-import]
            import pypdf  # type: ignore
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            print(f"pypdf extraction warning: {e}")

        if not text.strip():
            try:
                text = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                pass

    elif filename_lower.endswith(".docx"):
        try:
            # pyrefly: ignore [missing-import]
            import docx  # type: ignore
            doc = docx.Document(io.BytesIO(file_bytes))
            for p in doc.paragraphs:
                text += p.text + "\n"
        except Exception as e:
            print(f"docx extraction warning: {e}")
    else:
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = file_bytes.decode("latin-1", errors="ignore")

    return text.strip()


class RequirementExtractionService:

    @staticmethod
    def _normalize_multilingual_text(text: str) -> str:
        """Normalize common Indian-language technical terms to BIS-oriented English terms."""
        normalized = text or ""

        for source_term, english_term in sorted(
            MULTILINGUAL_TRANSLATIONS.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            normalized = normalized.replace(
                source_term,
                f" {english_term} ",
            )

        return re.sub(r"\s+", " ", normalized).strip()

    @staticmethod
    def _extract_key_values_from_text(text: str) -> Dict[str, str]:
        extracted = {}
        if not text:
            return extracted

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line_clean = re.sub(r'^[*\-•\d+\.]+\s*', '', line)
            match = re.match(
                r'^([A-Za-z0-9_\s\-\/]{2,35})\s*[:=]\s*(.+)$', line_clean)
            if match:
                raw_key, raw_val = match.group(
                    1).strip(), match.group(2).strip()
                low_k = raw_key.lower()
                if any(skip in low_k for skip in ["http", "https", "page", "date", "tel", "email", "fax", "ref", "tender_no", "tender_id"]):
                    continue
                norm_key = re.sub(r'[\s\-]+', '_', low_k)
                if norm_key and raw_val:
                    extracted[norm_key] = raw_val
        return extracted

    @staticmethod
    def _extract_from_prose(text: str) -> Dict[str, str]:
        """Generic prose extraction — detects technical parameters present in text regardless of product."""
        extracted = {}
        if not text:
            return extracted

        # Generic patterns applicable to any product
        PROSE_PATTERNS = [
            ("quantity",
             r'\b(?:procurement\s+of|quantity[:\s]*|qty[:\s]*)\s*(\d+)\b'),
            ("processor",
             r'\b(intel\s+core\s+i[3579][^,\.;\n]*|amd\s+ryzen\s+\d+[^,\.;\n]*)\b'),
            ("ram", r'\b(\d+\s*gb(?:\s+ram|\s+ddr[345]?))\b'),
            ("storage", r'\b(\d+\s*(?:gb|tb)\s*(?:ssd|hdd|nvme|storage))\b'),
            ("display",
             r'\b(\d+(?:\.\d+)?[\s-]*(?:inch|\"|in)\s*[^,\.;\n]*(?:monitor|display|led|lcd)[^,\.;\n]*)\b'),
            ("graphics",
             r'\b(integrated\s+graphics|dedicated\s+graphics|nvidia[^,\.;\n]*|amd\s+radeon[^,\.;\n]*)\b'),
            ("networking",
             r'\b((?:gigabit\s+ethernet|ethernet|wi-fi|wifi)[^,\.;\n]*)\b'),
            ("accessories", r'\b(keyboard\s+and\s+mouse|mouse\s+and\s+keyboard)\b'),
            ("application", r'\bused\s+for\s+([^,\.;\n]+)'),
            ("environment", r'\bin\s+an?\s+([^,\.;\n]*environment)'),
            ("temperature", r'\b(\d+(?:\.\d+)?\s*(?:°C|deg\s*C|degrees?\s*C(?:elsius)?))\b'),
            ("weight", r'\b(\d+(?:\.\d+)?\s*(?:kg|ton|tonne|gram)s?)\b'),
            ("dimension", r'\b(\d+\s*(?:x|×)\s*\d+(?:\s*(?:x|×)\s*\d+)?\s*(?:mm|cm|m|inch))\b'),
            ("material",
             r'\b((?:stainless\s+steel|cast\s+iron|mild\s+steel|copper|bronze|aluminium|aluminum|hdpe|upvc|frp|grp|ss\s*304|ss\s*316)[^,\.;\n]*)\b'),
            ("ip_rating", r'\b(IP\s*[0-9]{2})\b'),
            ("certification_ref",
             r'\b(IS\s+\d+(?:\s*\(\s*Part\s*\d+\s*\))?(?:\s*:\s*\d{4})?)\b'),
            ("colour_temperature", r'\b(\d{4}\s*K\b)'),
            ("luminous_flux", r'\b(\d+\s*(?:lm|lumens?))\b'),
            ("wattage", r'\b(\d+(?:\.\d+)?\s*(?:W|watt)s?)\b'),
            ("speed", r'\b(\d+\s*(?:rpm|RPM))\b'),
            ("frequency", r'\b(\d+\s*(?:Hz|hz))\b'),
            ("volume", r'\b(\d+(?:\.\d+)?\s*(?:litres?|liters?|ml|m3|m³))\b'),
        ]

        for key, pattern in PROSE_PATTERNS:
            m = re.search(pattern, text, re.I)
            if m:
                extracted[key] = m.group(1).strip()

        return extracted

    @staticmethod
    def extract_from_request(
        product_title: str,
        product_description: str = "",
        technical_specification: Dict[str, Any] = None,
        language: str = "en",
        document_text: str = ""
    ) -> ExtractedRequirementsResult:

        tech_spec = dict(technical_specification or {})

        combined_text = (
            f"{product_title} "
            f"{product_description} "
            f"{document_text} "
            + " ".join(
                f"{k}: {v}"
                for k, v in tech_spec.items()
            )
        ).strip()

        normalized_text = (
            RequirementExtractionService
            ._normalize_multilingual_text(combined_text)
        )

        # Use normalized text for detection while preserving the
        # original title in the returned product object.
        lower_text = normalized_text.lower()
        product_name = (
            product_title.strip()
            if product_title
            else "Industrial Product"
        )

        # Infer category dynamically from normalized content; preserve
        # the user's original product title.
        category = "General Engineering & Industrial Products"

        # Category inference rules — product_name is NOT overwritten; user's title is preserved
        CATEGORY_RULES = [
            (["pressure vessel", "unfired pressure", "reactor", "boiler",
             "16 bar"], "Pressure Vessels & Process Equipment"),
            (["street light", "street lighting", "luminaire", "led lamp",
             "highway lighting"], "Lighting & Electrical Systems"),
            (["storage tank", "water tank", "ss304",
             "ss316"], "Tanks & Storage Systems"),
            (["centrifuge", "laboratory centrifuge"],
             "Laboratory & Medical Testing"),
            (["cable", "wire", "wiring", "xlpe", "pvc insulated"],
             "Electrical Cables & Wiring"),
            (["desktop", "computer", "processor", "intel core", "laptop",
             "pc", "workstation", "server"], "IT & Computing Infrastructure"),
            (["pump", "centrifugal", "rotodynamic", "पंप"], "Pumps & Fluid Handling"),
            (["motor", "induction motor", "squirrel cage", "मोटर"],
             "Electrical Motors & Drives"),
            (["transformer", "distribution transformer",
             "ट्रान्सफॉर्मर"], "Electrical Power Systems"),
            (["solar", "pv module", "photovoltaic", "सौर"], "Solar Energy Systems"),
            (["pipe", "hdpe", "पाइप"], "Pipes, Valves & Fittings"),
            (["valve", "gate valve", "check valve",
             "वॉल्व"], "Pipes, Valves & Fittings"),
            (["drinking water", "packaged drinking", "packaged water",
             "mineral water", "potable water"], "Water & Environment"),
        ]

        for terms, cat in CATEGORY_RULES:
            if any(re.search(rf"\b{re.escape(term)}\b", lower_text) for term in terms):
                category = cat
                break

        # 1. Parse structured key-values from document_text and product_description
        parsed_key_values = RequirementExtractionService._extract_key_values_from_text(
            f"{product_description}\n{document_text}")

        # 2. Parse prose specifications from natural language text
        parsed_prose = RequirementExtractionService._extract_from_prose(
            f"{product_title}\n{product_description}\n{document_text}")

        # Merge key-values: tech_spec passed explicitly takes precedence, then key-values, then prose
        params = {**parsed_prose, **parsed_key_values, **tech_spec}

        # 2. Add regex matched parameters if not present
        for param_key, pattern in PARAM_PATTERNS.items():
            if param_key not in params:
                match = re.search(pattern, lower_text, re.IGNORECASE)
                if match:
                    params[param_key] = match.group(0)

        # Application & Environment detection
        if "application" in params:
            application = str(params["application"]).strip()
        else:
            application = ""

            application_patterns = [
                r"\bused\s+for\s+([^,.;\n]+)",
                r"\bfor\s+([^,.;\n]+?)\s+(?:application|use|service)",
                r"\bsuitable\s+for\s+([^,.;\n]+)",
                r"\bfor\s+([^,.;\n]+)",
                r"\bapplication\s+(?:is|:)\s*([^,.;\n]+)",
            ]

            for pattern in application_patterns:
                match = re.search(
                    pattern,
                    lower_text,
                    re.IGNORECASE,
                )
                if match:
                    application = match.group(1).strip()
                    break

            if not application:
                application = (
                    f"general {category.lower()} application"
                )

        if "environment" in params:
            environment = {
                "installation": str(params["environment"]),
                "location": "Facility / Office"
            }
        else:
            environment = {
                "installation": "Field / Industrial installation",
                "location": "Facility"
            }

        materials = []
        if "cast iron" in lower_text:
            materials.append("Cast Iron (CI)")
        if "stainless steel" in lower_text or "ss 304" in lower_text or "ss 316" in lower_text:
            materials.append("Stainless Steel (SS)")
        if "bronze" in lower_text or "copper alloy" in lower_text:
            materials.append("Bronze / Copper Alloy")

        performance = []
        if "ie3" in lower_text or "ie4" in lower_text or "energy efficient" in lower_text:
            performance.append("IE3/IE4 Premium Efficiency Rating")
        if "high head" in lower_text:
            performance.append("High Head Operating Range")
        if "ssd" in lower_text or "nvme" in lower_text:
            performance.append("High-Speed Solid State Drive Storage")
        if "mono perc" in lower_text or "bifacial" in lower_text:
            performance.append("High-Efficiency Photovoltaic Cell Technology")
        if "ip66" in lower_text or "ip67" in lower_text or "ip68" in lower_text:
            performance.append("High Ingress Protection (IP66+) Rating")

        # Build safety list dynamically from category and detected parameters
        safety = ["Earthing & Protective Bonding"]
        if any(t in lower_text for t in ["electrical", "motor", "computer", "power", "voltage", "led", "cable"]):
            safety.append("Electrical Insulation & Short Circuit Protection")
        if any(t in lower_text for t in ["pressure", "vessel", "pump", "tank", "valve", "pipe"]):
            safety.append("Mechanical Integrity & Pressure Relief Protection")
        if any(t in lower_text for t in ["solar", "photovoltaic", "pv"]):
            safety.append(
                "Fire Safety & Anti-Islanding Protection (Grid-Tied Systems)")
        if any(t in lower_text for t in ["outdoor", "street", "road", "highway", "field"]):
            safety.append(
                "Weather & Ingress Protection for Outdoor Installation")
        if any(t in lower_text for t in ["computer", "desktop", "laptop", "server", "it"]):
            safety.append(
                "Bureau of Indian Standards (BIS) CRS Registration Compliance")
        if any(t in lower_text for t in ["medical", "laboratory", "clinical", "hospital"]):
            safety.append("Medical Device Safety & Regulatory Clearance")
        if "overload" not in lower_text:
            safety.append("Overload & Thermal Protection")

        PRODUCT_FAMILY_TERMS = {
            "transformer": [
                "transformer",
                "distribution transformer",
                "power transformer",
                "oil immersed transformer",
            ],
            "motor": [
                "motor",
                "induction motor",
                "three phase induction motor",
                "squirrel cage motor",
            ],
            "pump": [
                "pump",
                "centrifugal pump",
                "rotodynamic pump",
                "water pump",
            ],
            "cable": [
                "cable",
                "electric cable",
                "power cable",
                "pvc insulated cable",
                "xlpe cable",
            ],
            "compressor": [
                "compressor",
                "air compressor",
                "screw compressor",
                "rotary screw compressor",
            ],
            "refrigerator": [
                "refrigerator",
                "household refrigerator",
                "domestic refrigerator",
                "frost free refrigerator",
            ],
            "lighting": [
                "street lighting",
                "road lighting",
                "luminaire",
                "led luminaire",
                "street light",
            ],
        }

        product_family = ""

        for family, terms in PRODUCT_FAMILY_TERMS.items():
            if any(term in lower_text for term in terms):
                product_family = family
                break

        canonical_parts = [
            product_name,
            product_family,
            category,
            application,
        ]

        canonical_parts.extend(
            str(v)
            for v in params.values()
        )

        canonical_query = " ".join(
            part
            for part in canonical_parts
            if part
        )

        return ExtractedRequirementsResult(
            product={"name": product_name, "category": category},
            application=application,
            environment=environment,
            technical_parameters=params,
            materials=materials,
            performance=performance,
            safety=safety,
            canonical_query=canonical_query
        )

    @staticmethod
    def convert_to_requirement_items(tech_spec: Dict[str, Any]) -> List[RequirementItem]:
        items = []
        for k, v in tech_spec.items():
            val_str = str(v)
            unit = ""
            unit_match = re.search(r"([a-zA-Z3%/]+)$", val_str)
            if unit_match:
                unit = unit_match.group(1)
            items.append(
                RequirementItem(
                    category="technical_parameters",
                    attribute=k,
                    value=val_str,
                    unit=unit,
                    source_text=f"{k}: {val_str}"
                )
            )
        return items
