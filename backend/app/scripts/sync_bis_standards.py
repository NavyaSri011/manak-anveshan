# pyrefly: ignore [missing-import]
import datetime
import urllib.request
import json
import logging
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine, Base
from app.database.models import Standard, Amendment, StandardRelationship, CertificationRule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BIS_STANDARDS_SEED_DATA = [
    # 1. PRESSURE VESSELS & PROCESS TANKS
    {
        "is_number": "IS 2825:1969",
        "title": "Code for Unfired Pressure Vessels",
        "scope": "Covers design, construction, inspection and testing of unfired pressure vessels made of ferrous and non-ferrous metals for chemical, petrochemical and process industries operating under pressure (bar, kg/cm2) and high/low temperatures.",
        "status": "ACTIVE",
        "publication_year": 1969,
        "reviewed_year": 2021,
        "revision_information": "Reaffirmed 2021 with Amendments 1 to 5. Code of practice for industrial pressure vessels.",
        "department": "MED - Mechanical Engineering",
        "technical_committee": "MED 03 - Pressure Vessels",
        "classification": "CODE_OF_PRACTICE",
        "ics_codes": "23.020.30",
        "certification": "Optional / Regulatory Compliance",
        "source_url": "https://standards.bis.gov.in/g/is/IS-2825",
        "category": "Pressure Vessels & Process Equipment",
        "keywords": "industrial pressure vessel unfired pressure vessel 16 bar 180C stainless steel chemical processing vessel design pressure operating temperature heat exchanger reactor tank",
        "amendments": [
            {"amendment_number": 1, "date": "1977-03", "description": "Stress value tables update"},
            {"amendment_number": 2, "date": "1984-11", "description": "Welding joint factor and non-destructive testing requirements"}
        ]
    },
    {
        "is_number": "IS 4049 (Part 1):1988",
        "title": "Seamless and Welded Steel Pipes for Pressure Vessels and Piping Systems",
        "scope": "Specifies technical supply conditions for seamless and welded steel pipes used in pressure vessels, boilers, and high-pressure chemical processing piping.",
        "status": "ACTIVE",
        "publication_year": 1988,
        "reviewed_year": 2020,
        "revision_information": "First Revision.",
        "department": "MED - Mechanical Engineering",
        "technical_committee": "MED 03 - Pressure Vessels",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "23.040.10",
        "certification": "BIS ISI Mark / Optional",
        "source_url": "https://standards.bis.gov.in/g/is/IS-4049-1",
        "category": "Pressure Vessels & Process Equipment",
        "keywords": "steel pipe pressure vessel piping seamless pipe welded pipe chemical processing stainless steel pressure tube",
        "amendments": []
    },
    {
        "is_number": "IS 15416:2003",
        "title": "Stainless Steel Water Storage Tanks - Specification",
        "scope": "Specifies requirements for food-grade and industrial stainless steel storage tanks (SS304, SS316) used for potable water, chemical liquids, and beverage storage.",
        "status": "ACTIVE",
        "publication_year": 2003,
        "reviewed_year": 2019,
        "revision_information": "Reaffirmed 2019.",
        "department": "CED - Civil Engineering",
        "technical_committee": "CED 50 - Plastic Piping and Storage Systems",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "23.020.10",
        "certification": "BIS ISI Mark / Voluntary",
        "source_url": "https://standards.bis.gov.in/g/is/IS-15416",
        "category": "Tanks & Storage Systems",
        "keywords": "stainless steel water storage tank SS304 SS316 food grade tank chemical storage tank water tank storage vessel stainless steel tank",
        "amendments": []
    },
    {
        "is_number": "IS 803:1976",
        "title": "Code of Practice for Design, Fabrication and Erection of Vertical Mild Steel Welded Storage Tanks",
        "scope": "Covers design, fabrication, erection and testing of vertical cylindrical mild steel welded tanks for storage of liquids at atmospheric pressure.",
        "status": "ACTIVE",
        "publication_year": 1976,
        "reviewed_year": 2018,
        "revision_information": "Reaffirmed 2018.",
        "department": "CED - Civil Engineering",
        "technical_committee": "CED 07 - Structural Engineering",
        "classification": "CODE_OF_PRACTICE",
        "ics_codes": "23.020.10",
        "certification": "Optional / Regulatory Compliance",
        "source_url": "https://standards.bis.gov.in/g/is/IS-803",
        "category": "Tanks & Storage Systems",
        "keywords": "storage tank welded steel tank vertical storage tank liquid storage chemical tank mild steel tank",
        "amendments": []
    },

    # 2. LIGHTING & LUMINAIRES
    {
        "is_number": "IS 10322 (Part 5/Sec 2):2012",
        "title": "Luminaires - Part 5: Particular Requirements - Section 2: Street and Highway Lighting",
        "scope": "Specifies safety and performance requirements for street and highway lighting luminaires, including outdoor LED street light fixtures for public roads and highways.",
        "status": "ACTIVE",
        "publication_year": 2012,
        "reviewed_year": 2022,
        "revision_information": "First Revision.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 23 - Electric Lamps and Luminaires",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "29.140.40",
        "certification": "CRS Mandatory (Compulsory Registration Scheme)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-10322-5-2",
        "category": "Lighting & Electrical Systems",
        "keywords": "LED street lighting system street light highway lighting outdoor luminaire LED lamp fixture road lighting public lighting IP66",
        "amendments": [
            {"amendment_number": 1, "date": "2016-05", "description": "Thermal test and IP rating protection update"}
        ]
    },
    {
        "is_number": "IS 16102 (Part 1):2012",
        "title": "Self-ballasted LED Lamps for General Lighting Services - Safety Requirements",
        "scope": "Specifies safety and interchangeability requirements for self-ballasted LED lamps for general lighting services up to 250V.",
        "status": "ACTIVE",
        "publication_year": 2012,
        "reviewed_year": 2022,
        "revision_information": "Reaffirmed 2022.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 23 - Electric Lamps and Luminaires",
        "classification": "SAFETY",
        "ics_codes": "29.140.30",
        "certification": "CRS Mandatory (Compulsory Registration Scheme)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-16102-1",
        "category": "Lighting & Electrical Systems",
        "keywords": "LED lamp self ballasted LED bulb general lighting LED safety CRS mandatory indoor outdoor lighting",
        "amendments": []
    },
    {
        "is_number": "IS 15885 (Part 2/Sec 13):2012",
        "title": "Lamp Controlgear - Part 2-13: Particular Requirements for DC or AC Supplied Electronic Controlgear for LED Modules",
        "scope": "Specifies safety requirements for electronic controlgear (LED drivers) used with LED modules in luminaires and street lighting.",
        "status": "ACTIVE",
        "publication_year": 2012,
        "reviewed_year": 2022,
        "revision_information": "Reaffirmed 2022.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 23 - Electric Lamps and Luminaires",
        "classification": "SAFETY",
        "ics_codes": "29.140.99",
        "certification": "CRS Mandatory",
        "source_url": "https://standards.bis.gov.in/g/is/IS-15885-2-13",
        "category": "Lighting & Electrical Systems",
        "keywords": "LED driver electronic controlgear LED module driver street light driver power supply LED driver safety",
        "amendments": []
    },

    # 3. IT & ELECTRONICS (DESKTOP COMPUTERS, SERVERS, MONITORS)
    {
        "is_number": "IS 13252 (Part 1):2010",
        "title": "Information Technology Equipment - Safety - Part 1: General Requirements",
        "scope": "Specifies electrical, thermal, and mechanical safety requirements for information technology equipment including desktop computers, laptops, servers, monitors, and power supplies.",
        "status": "ACTIVE",
        "publication_year": 2010,
        "reviewed_year": 2020,
        "revision_information": "Reaffirmed 2020. Equivalent to IEC 60950-1.",
        "department": "LITD - Electronics and Information Technology",
        "technical_committee": "LITD 07 - Information Technology Equipment Safety",
        "classification": "SAFETY",
        "ics_codes": "35.020",
        "certification": "CRS Mandatory (Compulsory Registration Scheme by MeitY)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-13252-1",
        "category": "IT & Computing Infrastructure",
        "keywords": "desktop computer government school pc laptop server monitor LED monitor intel core i5 ram ssd graphics ethernet keyboard mouse IT equipment safety CRS",
        "amendments": [
            {"amendment_number": 1, "date": "2013-08", "description": "Compulsory registration safety guidelines"},
            {"amendment_number": 2, "date": "2015-12", "description": "Power adapter isolation and creepage distance specification"}
        ]
    },
    {
        "is_number": "IS 14252:1995",
        "title": "Desktop Computer Systems & Workstations - Specification",
        "scope": "Covers performance, interface, environmental, and general technical requirements for personal desktop computers and workstations for office and educational institutions.",
        "status": "ACTIVE",
        "publication_year": 1995,
        "reviewed_year": 2021,
        "revision_information": "Reaffirmed 2021.",
        "department": "LITD - Electronics and Information Technology",
        "technical_committee": "LITD 13 - Computer Hardware",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "35.160",
        "certification": "Optional / Self Declaration",
        "source_url": "https://standards.bis.gov.in/g/is/IS-14252",
        "category": "IT & Computing Infrastructure",
        "keywords": "desktop computer workstation pc system hardware specification processor memory storage keyboard mouse school computer",
        "amendments": []
    },
    {
        "is_number": "IS 616:2017",
        "title": "Audio, Video and Similar Electronic Apparatus - Safety Requirements",
        "scope": "Applies to electronic apparatus designed to be fed from mains or supply apparatus for general consumer and educational display monitors.",
        "status": "ACTIVE",
        "publication_year": 2017,
        "reviewed_year": 2022,
        "revision_information": "Third Revision. Equivalent to IEC 60065.",
        "department": "LITD - Electronics and Information Technology",
        "technical_committee": "LITD 07 - Audio Video Safety",
        "classification": "SAFETY",
        "ics_codes": "33.160",
        "certification": "CRS Mandatory",
        "source_url": "https://standards.bis.gov.in/g/is/IS-616",
        "category": "IT & Computing Infrastructure",
        "keywords": "display monitor LED monitor video display audio apparatus CRS safety",
        "amendments": []
    },

    # 4. LABORATORY & MEDICAL EQUIPMENT
    {
        "is_number": "IS 6428:1972",
        "title": "Specification for Laboratory Centrifuges",
        "scope": "Specifies constructional, performance, and safety requirements for electrically driven laboratory centrifuges used in clinical, medical, chemical, and biological testing laboratories.",
        "status": "ACTIVE",
        "publication_year": 1972,
        "reviewed_year": 2019,
        "revision_information": "Reaffirmed 2019.",
        "department": "MED - Mechanical Engineering",
        "technical_committee": "MED 26 - Laboratory Equipment",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "71.040.20",
        "certification": "BIS ISI Mark / Optional",
        "source_url": "https://standards.bis.gov.in/g/is/IS-6428",
        "category": "Laboratory & Medical Testing",
        "keywords": "laboratory centrifuge medical testing centrifuge clinical centrifuge benchtop centrifuge rotor speed RPM medical laboratory equipment test tube centrifuge",
        "amendments": []
    },
    {
        "is_number": "IS 13450 (Part 1):2018",
        "title": "Medical Electrical Equipment - Part 1: General Requirements for Basic Safety and Essential Performance",
        "scope": "Applies to the basic safety and essential performance of medical electrical equipment used in hospitals and testing laboratories.",
        "status": "ACTIVE",
        "publication_year": 2018,
        "reviewed_year": 2023,
        "revision_information": "Identical to IEC 60601-1.",
        "department": "MHD - Medical Equipment and Hospital Planning",
        "technical_committee": "MHD 15 - Electromedical Equipment",
        "classification": "SAFETY",
        "ics_codes": "11.040.01",
        "certification": "Medical Devices Rules Compliance",
        "source_url": "https://standards.bis.gov.in/g/is/IS-13450-1",
        "category": "Laboratory & Medical Testing",
        "keywords": "medical electrical equipment safety laboratory testing clinical device centrifuge analyzer medical device",
        "amendments": []
    },

    # 5. ELECTRICAL CABLES & WIRING
    {
        "is_number": "IS 694:2010",
        "title": "Polyvinyl Chloride Insulated Unsheathed and Sheathed Cables for Working Voltages up to and Including 1100 V",
        "scope": "Covers requirements for single core and multicore PVC insulated cables for electric power, lighting, and internal wiring up to 1100 Volts.",
        "status": "ACTIVE",
        "publication_year": 2010,
        "reviewed_year": 2020,
        "revision_information": "Fourth Revision.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 09 - Cables and Wires",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "29.060.20",
        "certification": "BIS ISI Mark Mandatory (QCO Mandatory)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-694",
        "category": "Electrical Cables & Wiring",
        "keywords": "electrical cable PVC wire insulated cable copper wire aluminum cable 1100V building wire power cable wiring",
        "amendments": [
            {"amendment_number": 1, "date": "2014-02", "description": "Flame retardant low smoke (FRLS) property specification"}
        ]
    },
    {
        "is_number": "IS 7098 (Part 1):1988",
        "title": "Crosslinked Polyethylene Insulated Thermoplastic Sheathed Cables - Part 1: For Working Voltages Up to and Including 1100 V",
        "scope": "Specifies requirements for XLPE insulated heavy duty power cables for working voltages up to 1100 V in industrial distribution.",
        "status": "ACTIVE",
        "publication_year": 1988,
        "reviewed_year": 2020,
        "revision_information": "Reaffirmed 2020.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 09 - Cables and Wires",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "29.060.20",
        "certification": "BIS ISI Mark Mandatory (QCO Mandatory)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-7098-1",
        "category": "Electrical Cables & Wiring",
        "keywords": "XLPE cable heavy duty cable power cable underground cable armoured cable electrical wiring",
        "amendments": []
    },

    # 6. PUMPS & FLUID HANDLING
    {
        "is_number": "IS 1520:1980",
        "title": "Horizontal Centrifugal Pumps for Clear, Cold, Fresh Water - Specification",
        "scope": "Specifies requirements for horizontal centrifugal pumps for clear, cold, fresh water for industrial, agricultural, and domestic water supply.",
        "status": "ACTIVE",
        "publication_year": 1980,
        "reviewed_year": 2019,
        "revision_information": "Second Revision.",
        "department": "MED - Mechanical Engineering",
        "technical_committee": "MED 20 - Pumps",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "23.080",
        "certification": "BIS ISI Mark / Voluntary",
        "source_url": "https://standards.bis.gov.in/g/is/IS-1520",
        "category": "Pumps & Fluid Handling",
        "keywords": "horizontal centrifugal pump water pump flow rate head power cast iron casing fresh water supply industrial pump",
        "amendments": []
    },
    {
        "is_number": "IS 5120:1977",
        "title": "Technical Requirements for Rotodynamic Special Purpose Pumps",
        "scope": "Covers general technical requirements for rotodynamic pumps including centrifugal, mixed flow, and axial flow pumps.",
        "status": "ACTIVE",
        "publication_year": 1977,
        "reviewed_year": 2018,
        "revision_information": "Reaffirmed 2018.",
        "department": "MED - Mechanical Engineering",
        "technical_committee": "MED 20 - Pumps",
        "classification": "TEST_METHOD",
        "ics_codes": "23.080",
        "certification": "Optional",
        "source_url": "https://standards.bis.gov.in/g/is/IS-5120",
        "category": "Pumps & Fluid Handling",
        "keywords": "rotodynamic pump centrifugal pump testing pump efficiency hydraulic test head flow rate",
        "amendments": []
    },

    # 7. MOTORS & DRIVES
    {
        "is_number": "IS 12615:2018",
        "title": "Line Operated Three-Phase AC Motors - Efficiency Classes (IE Code) and Performance Specification",
        "scope": "Specifies efficiency classes (IE1, IE2, IE3, IE4) and performance requirements for line-operated three-phase squirrel cage induction motors.",
        "status": "ACTIVE",
        "publication_year": 2018,
        "reviewed_year": 2023,
        "revision_information": "Third Revision.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 15 - Rotating Machinery",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "29.160.30",
        "certification": "BIS ISI Mark Mandatory (QCO Mandatory)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-12615",
        "category": "Electrical Motors & Drives",
        "keywords": "three phase motor induction motor IE3 premium efficiency electric motor squirrel cage motor industrial drive 415V",
        "amendments": []
    },

    # 8. SOLAR PHOTOVOLTAIC MODULES
    {
        "is_number": "IS 14286:2019",
        "title": "Crystalline Silicon Terrestrial Photovoltaic (PV) Modules - Design Qualification and Type Approval",
        "scope": "Specifies requirements for design qualification and type approval of terrestrial crystalline silicon PV modules suitable for long-term operation in outdoor climates.",
        "status": "ACTIVE",
        "publication_year": 2019,
        "reviewed_year": 2024,
        "revision_information": "Second Revision. Identical to IEC 61215.",
        "department": "ETD - Electrotechnical",
        "technical_committee": "ETD 28 - Solar Photovoltaic Energy Systems",
        "classification": "PRODUCT_SPECIFICATION",
        "ics_codes": "27.160",
        "certification": "CRS Mandatory (MNRE Quality Control Order)",
        "source_url": "https://standards.bis.gov.in/g/is/IS-14286",
        "category": "Solar Energy Systems",
        "keywords": "solar PV module crystalline silicon solar panel monocrystalline PERC solar panel solar power project grid tied 540Wp",
        "amendments": []
    }
]

BIS_RELATIONSHIPS_SEED = [
    ("IS 2825:1969", "IS 4049 (Part 1):1988", "NORMATIVE_REFERENCE", "IS 4049 specifies seamless and welded steel pipes used in unfired pressure vessel fabrication under IS 2825."),
    ("IS 2825:1969", "IS 15416:2003", "RELATED", "IS 15416 applies to stainless steel water storage tanks operating under atmospheric pressure."),
    ("IS 10322 (Part 5/Sec 2):2012", "IS 16102 (Part 1):2012", "NORMATIVE_REFERENCE", "IS 16102 specifies safety of LED lamp components integrated into street lighting luminaires."),
    ("IS 10322 (Part 5/Sec 2):2012", "IS 15885 (Part 2/Sec 13):2012", "SAFETY", "IS 15885-2-13 provides mandatory electronic controlgear (LED driver) safety rules for outdoor street lights."),
    ("IS 13252 (Part 1):2010", "IS 14252:1995", "NORMATIVE_REFERENCE", "IS 14252 specifies desktop computer performance while IS 13252 Part 1 mandates electrical safety compliance."),
    ("IS 13252 (Part 1):2010", "IS 616:2017", "SAFETY", "IS 616 mandates video display monitor safety for desktop computer LED monitor assemblies."),
    ("IS 6428:1972", "IS 13450 (Part 1):2018", "SAFETY", "IS 13450-1 specifies medical electrical safety for laboratory testing equipment and centrifuges."),
    ("IS 1520:1980", "IS 5120:1977", "TEST_METHOD", "IS 5120 specifies hydraulic test methods for rotodynamic centrifugal pumps under IS 1520.")
]

BIS_CERTIFICATION_RULES_SEED = [
    {"is_number": "IS 13252 (Part 1):2010", "product": "Desktop Computers & Systems", "scheme": "Compulsory Registration Scheme (CRS)", "mandatory": True, "conditions": "Mandatory CRS registration under Ministry of Electronics and Information Technology (MeitY) Order."},
    {"is_number": "IS 10322 (Part 5/Sec 2):2012", "product": "LED Street Lights & Outdoor Luminaires", "scheme": "Compulsory Registration Scheme (CRS)", "mandatory": True, "conditions": "Mandatory CRS registration for outdoor LED luminaires under MeitY Gazette Order."},
    {"is_number": "IS 694:2010", "product": "PVC Insulated Electric Cables", "scheme": "BIS Product Certification (ISI Mark)", "mandatory": True, "conditions": "Mandatory ISI Mark under Electrical Wires and Cables (Quality Control) Order."},
    {"is_number": "IS 12615:2018", "product": "Three Phase Induction Motors (IE3)", "scheme": "BIS Product Certification (ISI Mark)", "mandatory": True, "conditions": "Mandatory ISI Mark under Electric Motors (Quality Control) Order."},
    {"is_number": "IS 14286:2019", "product": "Solar PV Modules", "scheme": "Solar Photovoltaic Systems Order (MNRE)", "mandatory": True, "conditions": "Mandatory registration under MNRE Quality Control Order for solar modules."}
]

def sync_bis_standards(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        logger.info("Initializing BIS Standards Knowledge Base database tables...")
        Base.metadata.create_all(bind=engine)

        std_map = {}

        # 1. Upsert BIS Standards
        for item in BIS_STANDARDS_SEED_DATA:
            existing = db.query(Standard).filter(Standard.is_number == item["is_number"]).first()
            searchable = f"{item['is_number']} {item['title']} {item['scope']} {item['category']} {item['department']} {item['keywords']}"

            if not existing:
                std = Standard(
                    is_number=item["is_number"],
                    title=item["title"],
                    scope=item["scope"],
                    status=item["status"],
                    publication_year=item["publication_year"],
                    reviewed_year=item["reviewed_year"],
                    revision_information=item["revision_information"],
                    department=item["department"],
                    technical_committee=item["technical_committee"],
                    classification=item["classification"],
                    ics_codes=item["ics_codes"],
                    certification=item["certification"],
                    source_url=item["source_url"],
                    keywords=item["keywords"],
                    searchable_text=searchable,
                    category=item["category"],
                    source="Bureau of Indian Standards (BIS)",
                    source_type="AUTHORITATIVE"
                )
                db.add(std)
                db.flush()
                std_map[item["is_number"]] = std
                logger.info(f"Indexed BIS Standard: {item['is_number']} - {item['title']}")
            else:
                existing.title = item["title"]
                existing.scope = item["scope"]
                existing.publication_year = item["publication_year"]
                existing.reviewed_year = item["reviewed_year"]
                existing.department = item["department"]
                existing.technical_committee = item["technical_committee"]
                existing.classification = item["classification"]
                existing.keywords = item["keywords"]
                existing.searchable_text = searchable
                existing.source_type = "AUTHORITATIVE"
                std_map[item["is_number"]] = existing

        # Process amendments
        for item in BIS_STANDARDS_SEED_DATA:
            std = std_map.get(item["is_number"])
            if std and "amendments" in item:
                for amd in item["amendments"]:
                    amd_exists = db.query(Amendment).filter(
                        Amendment.standard_id == std.id,
                        Amendment.amendment_number == amd["amendment_number"]
                    ).first()
                    if not amd_exists:
                        db.add(Amendment(
                            standard_id=std.id,
                            amendment_number=amd["amendment_number"],
                            date=amd["date"],
                            description=amd["description"],
                            source="BIS Gazette / Published Standards List"
                        ))

        # 2. Seed Standard Relationships
        for src_num, tgt_num, rel_type, ev in BIS_RELATIONSHIPS_SEED:
            src_std = db.query(Standard).filter(Standard.is_number == src_num).first()
            tgt_std = db.query(Standard).filter(Standard.is_number == tgt_num).first()
            if src_std and tgt_std:
                rel_exists = db.query(StandardRelationship).filter(
                    StandardRelationship.source_standard_id == src_std.id,
                    StandardRelationship.target_standard_id == tgt_std.id
                ).first()
                if not rel_exists:
                    db.add(StandardRelationship(
                        source_standard_id=src_std.id,
                        target_standard_id=tgt_std.id,
                        relationship_type=rel_type,
                        evidence=ev
                    ))

        # 3. Seed Certification Rules
        for rule in BIS_CERTIFICATION_RULES_SEED:
            std = db.query(Standard).filter(Standard.is_number == rule["is_number"]).first()
            if std:
                c_exists = db.query(CertificationRule).filter(
                    CertificationRule.standard_id == std.id,
                    CertificationRule.product == rule["product"]
                ).first()
                if not c_exists:
                    db.add(CertificationRule(
                        standard_id=std.id,
                        product=rule["product"],
                        scheme=rule["scheme"],
                        mandatory=rule["mandatory"],
                        conditions=rule["conditions"],
                        source="Official BIS / Gazette Quality Control Order"
                    ))

        db.commit()
        count = db.query(Standard).count()
        logger.info(f"BIS Standards Knowledge Base successfully synchronized. Total indexed standards: {count}")
        return {
            "status": "SUCCESS",
            "message": f"BIS Standards Knowledge Base synchronized successfully. Indexed {count} authoritative Indian Standards.",
            "total_indexed": count,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to sync BIS standards: {e}")
        raise e
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    sync_bis_standards()
