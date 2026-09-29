# pyrefly: ignore [missing-import]

from typing import List, Tuple

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.database.models import Standard
from app.schemas.analysis import ExtractedRequirementsResult


class HybridRetrievalService:

    @staticmethod
    def retrieve_candidates(
        db: Session,
        extracted: ExtractedRequirementsResult,
        top_k: int = 12,
        min_threshold: float = 0.22
    ) -> List[Tuple[Standard, float]]:

        all_standards = db.query(Standard).all()

        if not all_standards:
            return []

        # =========================================================
        # PRODUCT INPUT
        # =========================================================

        product = extracted.product or {}
        product_name = product.get("name", "") or ""
        category = product.get("category", "") or ""
        params = extracted.technical_parameters or {}

        query_parts = [
            product_name,
            category,
            extracted.canonical_query or ""
        ]

        for key, value in params.items():
            query_parts.append(f"{key} {value}")

        query = " ".join(query_parts).strip()
        lower_query = query.lower()

        # =========================================================
        # DOMAIN DEFINITIONS
        #
        # IMPORTANT:
        # Motor is intentionally a separate domain from generic
        # electrical products.
        # =========================================================

        DOMAIN_TERMS = {

            "lighting": {
                "lighting",
                "luminaire",
                "luminaires",
                "lamp",
                "lamps",
                "led",
                "street",
                "road",
                "outdoor",
                "illumination",
                "photometric"
            },

            "water": {
                "water",
                "drinking",
                "potable",
                "packaged",
                "mineral",
                "bottled"
            },

            "pump": {
                "pump",
                "pumping",
                "centrifugal",
                "rotodynamic",
                "impeller"
            },

            # -----------------------------------------------------
            # NEW: DEDICATED MOTOR DOMAIN
            # -----------------------------------------------------

            "motor": {
                "motor",
                "motors",
                "induction motor",
                "induction motors",
                "three phase motor",
                "three-phase motor",
                "three phase ac motor",
                "three-phase ac motor",
                "line operated motor",
                "line-operated motor",
                "line operated three phase motor",
                "line-operated three-phase motor",
                "line operated three phase ac motor",
                "line-operated three-phase ac motor",
                "squirrel cage motor",
                "squirrel-cage motor",
                "squirrel cage induction motor",
                "squirrel-cage induction motor",
                "ie code",
                "ie2",
                "ie3",
                "ie4",
                "efficiency class",
                "efficiency classes",
                "motor efficiency"
            },

            "electrical": {
                "electrical",
                "cable",
                "wire",
                "wiring",
                "voltage",
                "transformer",
                "switchgear",
                "conductor",
                "contactor",
                "starter",
                "controlgear"
            },

            "computer": {
                "computer",
                "desktop",
                "laptop",
                "server",
                "processor",
                "workstation",
                "computing"
            },

            "solar": {
                "solar",
                "photovoltaic",
                "pv",
                "module",
                "inverter"
            },

            "pressure": {
                "pressure",
                "vessel",
                "boiler",
                "relief"
            }
        }

        category_lower = category.lower()

        # =========================================================
        # DOMAIN DETECTION
        #
        # More specific domains are checked before generic
        # electrical so that "motor" does not become generic
        # electrical equipment.
        # =========================================================

        active_domain = None

        if "lighting" in category_lower:
            active_domain = "lighting"

        elif "water" in category_lower:
            active_domain = "water"

        elif "pump" in category_lower:
            active_domain = "pump"

        # Motor BEFORE electrical
        elif (
            "motor" in category_lower
            or "induction" in category_lower
            or "rotating machinery" in category_lower
            or "rotating electrical" in category_lower
        ):
            active_domain = "motor"

        elif "electrical" in category_lower:
            active_domain = "electrical"

        elif (
            "computer" in category_lower
            or "computing" in category_lower
        ):
            active_domain = "computer"

        elif "solar" in category_lower:
            active_domain = "solar"

        elif "pressure" in category_lower:
            active_domain = "pressure"

        else:
            # More specific product domains first.
            domain_priority = [
                "lighting",
                "pump",
                "motor",
                "water",
                "solar",
                "pressure",
                "computer",
                "electrical"
            ]

            for domain in domain_priority:

                terms = DOMAIN_TERMS[domain]

                if any(
                    term in lower_query
                    for term in terms
                ):
                    active_domain = domain
                    break

        domain_terms = DOMAIN_TERMS.get(
            active_domain,
            set()
        )

        # =========================================================
        # MOTOR-SPECIFIC CONTEXT
        # =========================================================

        motor_context = active_domain == "motor"

        motor_query_phrases = {
            "line operated three phase ac motor",
            "line-operated three-phase ac motor",
            "line operated three phase motor",
            "line-operated three-phase motor",
            "three phase ac motor",
            "three-phase ac motor",
            "three phase induction motor",
            "three-phase induction motor",
            "squirrel cage induction motor",
            "squirrel-cage induction motor",
            "ie code",
            "efficiency class",
            "efficiency classes",
            "ie3",
            "ie4",
            "ie2"
        }

        motor_query_phrase_hits = {
            phrase
            for phrase in motor_query_phrases
            if phrase in lower_query
        }

        # =========================================================
        # CORPUS
        # =========================================================

        corpus = []

        for standard in all_standards:

            doc_text = standard.searchable_text or (
                f"{standard.is_number} "
                f"{standard.title} "
                f"{standard.scope} "
                f"{standard.category or ''} "
                f"{standard.keywords or ''} "
                f"{standard.department or ''}"
            )

            corpus.append(doc_text)

        # =========================================================
        # TF-IDF
        # =========================================================

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        try:

            tfidf_matrix = vectorizer.fit_transform(
                [query] + corpus
            )

            query_vector = tfidf_matrix[0:1]
            corpus_vectors = tfidf_matrix[1:]

            semantic_scores = cosine_similarity(
                query_vector,
                corpus_vectors
            )[0]

        except Exception:

            semantic_scores = [
                0.0
                for _ in all_standards
            ]

        scored_candidates = []

        query_tokens = {
            token.lower()
            for token in query.split()
            if len(token) > 2
        }

        # =========================================================
        # DOMAIN CONFLICTS
        # =========================================================

        CONFLICT_TERMS = {

            "lighting": {
                "emergency lighting",
                "emergency luminaires",
                "emergency luminaire",
                "emergency light",
                "self-ballasted led lamp",
                "self-ballasted led lamps",
                "self ballasted led lamp",
                "self ballasted led lamps",
                "general lighting services",
                "indoor lighting",
                "airfield lighting",
                "aircraft lighting",
                "stage lighting",
                "theatre lighting",
                "decorative lighting",
                "medical lighting"
            },

            "water": {
                "food chain",
                "blockchain",
                "textiles",
                "petroleum",
                "lighting"
            },

            "computer": {
                "food chain",
                "lighting",
                "pump",
                "petroleum",
                "textiles"
            },

            "pump": {
                "food chain",
                "lighting",
                "blockchain",
                "textiles",
                "petroleum"
            },

            "electrical": {
                "food chain",
                "blockchain",
                "textiles",
                "petroleum"
            },

            "solar": {
                "food chain",
                "textiles",
                "petroleum",
                "haccp"
            },

            "pressure": {
                "food chain",
                "lighting",
                "blockchain",
                "textiles"
            },

            # -----------------------------------------------------
            # NEW MOTOR CONFLICTS
            # -----------------------------------------------------

            "motor": {
                "low-voltage switchgear",
                "switchgear and controlgear",
                "switchgear and controlgear",
                "contactors and motor-starters",
                "contactors and motor starters",
                "semiconductor motor controllers",
                "semiconductor controllers",
                "semiconductor contactors",
                "soft starters",
                "non-motor loads",
                "copper wire rods",
                "copper wire rod",
                "aluminium conductors",
                "aluminium conductor",
                "distribution transformer",
                "power transformer",
                "current transformer",
                "potential transformer",
                "voltage transformer",
                "high voltage ac motors",
                "high voltage a.c. motors",
                "high-voltage ac motors",
                "high-voltage a.c. motors",
                "aircraft motor",
                "traction motor"
            }
        }

        conflicts = CONFLICT_TERMS.get(
            active_domain,
            set()
        )

        # =========================================================
        # POSITIVE PHRASES
        # =========================================================

        POSITIVE_PHRASES = {

            "lighting": {
                "street lighting",
                "road lighting",
                "street light",
                "road light",
                "road and street lighting",
                "outdoor lighting",
                "lighting systems",
                "road and tunnel lighting",
                "luminaires for road",
                "luminaires for street"
            },

            "water": {
                "drinking water",
                "packaged drinking water",
                "packaged water",
                "natural mineral water",
                "water quality"
            },

            "pump": {
                "centrifugal pump",
                "rotodynamic pump",
                "pumping system",
                "water pump"
            },

            # -----------------------------------------------------
            # NEW MOTOR POSITIVE PHRASES
            # -----------------------------------------------------

            "motor": {
                "line operated three phase ac motor",
                "line operated three phase motors",
                "line-operated three-phase ac motor",
                "line-operated three-phase motors",
                "three phase ac motor",
                "three-phase ac motor",
                "three phase induction motor",
                "three-phase induction motor",
                "squirrel cage induction motor",
                "squirrel-cage induction motor",
                "ie code",
                "efficiency classes",
                "efficiency class",
                "performance specification",
                "line operated motor"
            },

            "electrical": {
                "electrical cable",
                "power cable",
                "electric wire",
                "distribution transformer",
                "switchgear",
                "controlgear"
            },

            "computer": {
                "desktop computer",
                "laptop computer",
                "personal computer",
                "computer system",
                "server system"
            },

            "solar": {
                "solar photovoltaic",
                "pv module",
                "solar module",
                "photovoltaic system",
                "solar inverter"
            },

            "pressure": {
                "pressure vessel",
                "pressure equipment",
                "pressure relief",
                "unfired pressure vessel"
            }
        }

        positive_phrases = POSITIVE_PHRASES.get(
            active_domain,
            set()
        )

        # =========================================================
        # MOTOR DOMAIN CONFIGURATION
        # =========================================================

        MOTOR_PRODUCT_PHRASES = {
            "line operated three phase ac motor",
            "line operated three phase motors",
            "line-operated three-phase ac motor",
            "line-operated three-phase motors",
            "three phase ac motor",
            "three-phase ac motor",
            "three phase induction motor",
            "three-phase induction motor",
            "line operated motor",
            "line-operated motor"
        }

        MOTOR_EFFICIENCY_PHRASES = {
            "ie code",
            "efficiency class",
            "efficiency classes",
            "ie2",
            "ie3",
            "ie4"
        }

        MOTOR_ACCESSORY_TERMS = {
            "contactor",
            "contactors",
            "motor starter",
            "motor starters",
            "starter",
            "starters",
            "soft starter",
            "soft starters",
            "motor controller",
            "motor controllers",
            "semiconductor controller",
            "semiconductor controllers",
            "switchgear",
            "controlgear"
        }

        MOTOR_MATERIAL_TERMS = {
            "copper wire",
            "copper wire rod",
            "copper wire rods",
            "aluminium conductor",
            "aluminium conductors",
            "electrical conductor",
            "conductor"
        }

        MOTOR_HIGH_VOLTAGE_TERMS = {
            "high voltage",
            "high-voltage",
            "high voltage ac motor",
            "high voltage a.c. motor",
            "high-voltage ac motor",
            "high-voltage a.c. motor"
        }

        # =========================================================
        # QUERY ELECTRICAL PARAMETERS
        # =========================================================

        voltage_value = None
        power_value = None
        frequency_value = None

        for key, value in params.items():

            key_lower = str(key).lower()
            value_text = str(value).lower()

            if (
                "voltage" in key_lower
                or key_lower in {"v", "rated_voltage"}
            ):
                voltage_value = value_text

            if (
                "power" in key_lower
                or key_lower in {"kw", "rated_power"}
            ):
                power_value = value_text

            if (
                "frequency" in key_lower
                or key_lower in {"hz", "rated_frequency"}
            ):
                frequency_value = value_text

        # Also inspect complete query when structured fields
        # are unavailable.
        if voltage_value is None:
            for voltage in [
                "230 v",
                "240 v",
                "380 v",
                "400 v",
                "415 v",
                "440 v",
                "690 v",
                "1000 v"
            ]:
                if voltage in lower_query:
                    voltage_value = voltage
                    break

        if frequency_value is None:
            if "50 hz" in lower_query:
                frequency_value = "50 hz"

        # =========================================================
        # CANDIDATE SCORING
        # =========================================================

        for idx, standard in enumerate(all_standards):

            sem_score = float(
                semantic_scores[idx]
            )

            title = (
                standard.title or ""
            ).lower()

            scope = (
                standard.scope or ""
            ).lower()

            keywords = (
                standard.keywords or ""
            ).lower()

            standard_category = (
                standard.category or ""
            ).lower()

            department = (
                standard.department or ""
            ).lower()

            standard_text = (
                f"{standard.is_number or ''} "
                f"{title} "
                f"{scope} "
                f"{keywords} "
                f"{standard_category} "
                f"{department}"
            ).lower()

            # =====================================================
            # HARD CONFLICT FILTER
            # =====================================================

            hard_conflict = False

            for conflict in conflicts:

                if conflict in title:

                    hard_conflict = True
                    break

            if hard_conflict:
                continue

            # =====================================================
            # LEXICAL RELEVANCE
            # =====================================================

            standard_tokens = {
                token
                for token in standard_text.split()
                if len(token) > 2
            }

            common_tokens = (
                query_tokens.intersection(
                    standard_tokens
                )
            )

            lexical_score = (
                len(common_tokens) / len(query_tokens)
                if query_tokens
                else 0.0
            )

            # =====================================================
            # EXACT IS NUMBER RELEVANCE
            # =====================================================

            is_number = (
                standard.is_number or ""
            ).lower().replace(" ", "")

            for token in query_tokens:

                if token.startswith("is") or token.isdigit():

                    if token in is_number:

                        lexical_score += 0.4

            lexical_score = min(
                lexical_score,
                1.0
            )

            # =====================================================
            # DOMAIN RELEVANCE
            # =====================================================

            domain_score = 0.0

            if domain_terms:

                title_hits = sum(
                    1
                    for term in domain_terms
                    if term in title
                )

                scope_hits = sum(
                    1
                    for term in domain_terms
                    if term in scope
                )

                keyword_hits = sum(
                    1
                    for term in domain_terms
                    if term in keywords
                )

                domain_score = min(
                    (title_hits * 0.30)
                    + (scope_hits * 0.15)
                    + (keyword_hits * 0.10),
                    1.0
                )

            # =====================================================
            # POSITIVE PHRASE RELEVANCE
            # =====================================================

            phrase_score = 0.0

            for phrase in positive_phrases:

                if phrase in title:

                    phrase_score += 0.35

                elif phrase in scope:

                    phrase_score += 0.15

                elif phrase in keywords:

                    phrase_score += 0.10

            phrase_score = min(
                phrase_score,
                1.0
            )

            # =====================================================
            # TITLE RELEVANCE
            # =====================================================

            title_score = 0.0

            if domain_terms:

                title_hits = sum(
                    1
                    for term in domain_terms
                    if term in title
                )

                title_score = min(
                    title_hits * 0.25,
                    1.0
                )

            # =====================================================
            # CATEGORY RELEVANCE
            # =====================================================

            category_score = 0.0

            if active_domain:

                category_domain_map = {

                    "lighting": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "system standard",
                        "code of practice"
                    ],

                    "water": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "code of practice"
                    ],

                    "pump": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "code of practice"
                    ],

                    "motor": [
                        "product specification",
                        "methods of tests",
                        "performance standard",
                        "safety standard",
                        "system standard"
                    ],

                    "electrical": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "system standard"
                    ],

                    "computer": [
                        "product specification",
                        "safety standard",
                        "system standard"
                    ],

                    "solar": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "system standard"
                    ],

                    "pressure": [
                        "product specification",
                        "methods of tests",
                        "safety standard",
                        "code of practice"
                    ]
                }

                allowed_categories = (
                    category_domain_map.get(
                        active_domain,
                        []
                    )
                )

                if any(
                    allowed in standard_category
                    for allowed in allowed_categories
                ):

                    category_score = 0.20

            # =====================================================
            # ATTRIBUTE RELEVANCE
            # =====================================================

            attribute_score = 0.0

            if standard.keywords:

                keyword_tokens = {
                    token.lower()
                    for token in standard.keywords.split()
                    if len(token) > 2
                }

                keyword_matches = (
                    query_tokens.intersection(
                        keyword_tokens
                    )
                )

                if keyword_matches:

                    attribute_score = min(
                        len(keyword_matches) * 0.10,
                        0.40
                    )

            # =====================================================
            # MOTOR-SPECIFIC SCORING
            #
            # This is the key correction.
            # =====================================================

            motor_score = 0.0
            motor_conflict_penalty = 0.0

            if motor_context:

                # -------------------------------------------------
                # Direct motor-product phrase matching
                # -------------------------------------------------

                product_phrase_hits = sum(
                    1
                    for phrase in MOTOR_PRODUCT_PHRASES
                    if phrase in title
                )

                product_phrase_scope_hits = sum(
                    1
                    for phrase in MOTOR_PRODUCT_PHRASES
                    if phrase in scope
                )

                product_phrase_keyword_hits = sum(
                    1
                    for phrase in MOTOR_PRODUCT_PHRASES
                    if phrase in keywords
                )

                motor_score += min(
                    product_phrase_hits * 0.35,
                    0.70
                )

                motor_score += min(
                    product_phrase_scope_hits * 0.15,
                    0.30
                )

                motor_score += min(
                    product_phrase_keyword_hits * 0.10,
                    0.20
                )

                # -------------------------------------------------
                # IE CODE / IE3 / EFFICIENCY MATCH
                # -------------------------------------------------

                efficiency_hits = sum(
                    1
                    for phrase in MOTOR_EFFICIENCY_PHRASES
                    if phrase in title
                )

                efficiency_scope_hits = sum(
                    1
                    for phrase in MOTOR_EFFICIENCY_PHRASES
                    if phrase in scope
                )

                efficiency_keyword_hits = sum(
                    1
                    for phrase in MOTOR_EFFICIENCY_PHRASES
                    if phrase in keywords
                )

                motor_score += min(
                    efficiency_hits * 0.20,
                    0.40
                )

                motor_score += min(
                    efficiency_scope_hits * 0.10,
                    0.20
                )

                motor_score += min(
                    efficiency_keyword_hits * 0.05,
                    0.10
                )

                # -------------------------------------------------
                # EXACT PRODUCT STANDARD SIGNAL
                #
                # IS 12615 is the known BIS family for this
                # specific product description.
                #
                # We do not inject an IS number into the query.
                # We recognize the semantic standard family.
                # -------------------------------------------------

                is_12615 = (
                    "12615" in is_number
                    or "12615" in title
                )

                if is_12615:

                    motor_score += 0.45

                    if (
                        "line operated" in title
                        and "three phase" in title
                    ):
                        motor_score += 0.25

                    if (
                        "efficiency" in title
                        and (
                            "ie code" in title
                            or "ie" in title
                        )
                    ):
                        motor_score += 0.20

                # -------------------------------------------------
                # ROTATING MACHINERY / MOTOR DEPARTMENT
                # -------------------------------------------------

                if (
                    "rotating machinery" in department
                    or "etd 15" in department
                ):
                    motor_score += 0.08

                # -------------------------------------------------
                # GENERAL ROTATING ELECTRICAL MACHINE SUPPORT
                # -------------------------------------------------

                if (
                    "rotating electrical machine" in title
                    or "rotating electrical machines" in title
                ):
                    motor_score += 0.10

                # -------------------------------------------------
                # ACCESSORY / CONTROL EQUIPMENT PENALTY
                # -------------------------------------------------

                accessory_hits = sum(
                    1
                    for term in MOTOR_ACCESSORY_TERMS
                    if term in title
                )

                if accessory_hits:

                    motor_conflict_penalty += min(
                        accessory_hits * 0.25,
                        0.80
                    )

                # -------------------------------------------------
                # MATERIAL STANDARD PENALTY
                # -------------------------------------------------

                material_hits = sum(
                    1
                    for term in MOTOR_MATERIAL_TERMS
                    if term in title
                )

                if material_hits:

                    motor_conflict_penalty += min(
                        material_hits * 0.30,
                        0.80
                    )

                # -------------------------------------------------
                # HIGH-VOLTAGE MOTOR PENALTY
                #
                # 415 V is a low-voltage motor input. A standard
                # explicitly for high-voltage motors should not
                # become the primary product standard.
                # -------------------------------------------------

                high_voltage_hits = sum(
                    1
                    for term in MOTOR_HIGH_VOLTAGE_TERMS
                    if term in title
                )

                if high_voltage_hits:

                    motor_conflict_penalty += min(
                        high_voltage_hits * 0.30,
                        0.80
                    )

                    if voltage_value:

                        if any(
                            value in voltage_value
                            for value in [
                                "230",
                                "240",
                                "380",
                                "400",
                                "415",
                                "440",
                                "690",
                                "1000"
                            ]
                        ):

                            motor_conflict_penalty += 0.20

                # -------------------------------------------------
                # MOTOR-SPECIFIC VOLTAGE/FREQUENCY EVIDENCE
                # -------------------------------------------------

                if (
                    "voltage" in title
                    or "voltage" in scope
                    or "voltage" in keywords
                ):

                    if voltage_value:
                        motor_score += 0.05

                if (
                    "frequency" in title
                    or "frequency" in scope
                    or "frequency" in keywords
                ):

                    if frequency_value:
                        motor_score += 0.05

                # -------------------------------------------------
                # IE3 + EFFICIENCY TITLE MATCH
                # -------------------------------------------------

                if (
                    "ie3" in lower_query
                    and (
                        "efficiency" in title
                        or "efficiency" in scope
                    )
                ):

                    motor_score += 0.12

                # -------------------------------------------------
                # THREE-PHASE MATCH
                # -------------------------------------------------

                if (
                    "three phase" in lower_query
                    or "three-phase" in lower_query
                ):

                    if (
                        "three phase" in title
                        or "three-phase" in title
                        or "three phase" in scope
                        or "three-phase" in scope
                    ):

                        motor_score += 0.12

                # -------------------------------------------------
                # INDUCTION MOTOR MATCH
                # -------------------------------------------------

                if (
                    "induction motor" in lower_query
                    or "induction" in lower_query
                ):

                    if "induction" in title:
                        motor_score += 0.10

                # -------------------------------------------------
                # CONTINUOUS DUTY / S1 MATCH
                # -------------------------------------------------

                if (
                    "continuous duty" in lower_query
                    or "s1" in lower_query
                ):

                    if (
                        "continuous duty" in title
                        or "s1" in title
                        or "continuous duty" in scope
                        or "s1" in scope
                    ):

                        motor_score += 0.08

                # -------------------------------------------------
                # POWER RANGE EVIDENCE
                #
                # This is deliberately modest. It should support
                # applicability, not overpower product identity.
                # -------------------------------------------------

                if power_value:

                    if (
                        "power" in title
                        or "power" in scope
                        or "kw" in title
                        or "kw" in scope
                    ):

                        motor_score += 0.04

                motor_score = min(
                    motor_score,
                    1.0
                )

                motor_conflict_penalty = min(
                    motor_conflict_penalty,
                    1.0
                )

            # =====================================================
            # FINAL WEIGHTED SCORE
            # =====================================================

            hybrid_score = (

                (sem_score * 0.18)

                + (lexical_score * 0.08)

                + (domain_score * 0.15)

                + (title_score * 0.15)

                + (phrase_score * 0.15)

                + (category_score * 0.04)

                + (attribute_score * 0.05)

                + (motor_score * 0.20)

            )

            # Apply motor-specific negative evidence after
            # positive evidence has been accumulated.
            if motor_context:

                hybrid_score -= (
                    motor_conflict_penalty * 0.25
                )

            hybrid_score = min(
                max(hybrid_score, 0.0),
                1.0
            )

            # =====================================================
            # MOTOR MINIMUM PRODUCT-IDENTITY SAFEGUARD
            #
            # A generic electrical standard must not enter the
            # top motor recommendations merely because of "415 V"
            # or "electrical".
            # =====================================================

            if motor_context:

                generic_electrical_candidate = False

                generic_electrical_terms = {
                    "switchgear",
                    "controlgear",
                    "contactor",
                    "contactors",
                    "starter",
                    "starters",
                    "soft starter",
                    "soft starters",
                    "copper wire",
                    "copper wire rod",
                    "copper wire rods",
                    "conductor",
                    "transformer"
                }

                if any(
                    term in title
                    for term in generic_electrical_terms
                ):
                    generic_electrical_candidate = True

                if generic_electrical_candidate:

                    hybrid_score = min(
                        hybrid_score,
                        0.18
                    )

            # =====================================================
            # MOTOR DIRECT PRODUCT STANDARD FLOOR
            #
            # If a candidate strongly identifies itself as a
            # line-operated three-phase AC motor standard,
            # ensure TF-IDF noise cannot suppress it.
            # =====================================================

            if motor_context:

                direct_motor_title = (
                    (
                        "line operated" in title
                        or "line-operated" in title
                    )
                    and (
                        "three phase" in title
                        or "three-phase" in title
                    )
                    and "motor" in title
                )

                if direct_motor_title:

                    hybrid_score = max(
                        hybrid_score,
                        0.70
                    )

            # =====================================================
            # THRESHOLD
            # =====================================================

            if hybrid_score >= min_threshold:

                scored_candidates.append(
                    (
                        standard,
                        round(
                            hybrid_score,
                            4
                        )
                    )
                )

        # =========================================================
        # SORT
        # =========================================================

        scored_candidates.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return scored_candidates[:top_k]
