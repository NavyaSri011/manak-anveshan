from app.database.models import Standard, Amendment, StandardRelationship, CertificationRule, generate_uuid
from sqlalchemy.orm import Session

def seed_database(db: Session):
    # Check if database is already populated
    if db.query(Standard).count() > 0:
        return

    # 1. STANDARDS
    standards_data = [
        {
            "id": "std-1520",
            "is_number": "IS 1520:1980",
            "title": "Horizontal Centrifugal Pumps for Clear, Cold, Fresh Water",
            "scope": "Specifies technical requirements, design criteria, hydraulic performance limits, materials, and testing protocols for horizontal centrifugal pumps handling clear, cold, fresh water for agricultural, industrial, and municipal water supply applications.",
            "status": "ACTIVE",
            "publication_date": "1980-05-15",
            "revision_date": "2018-11-20",
            "ics_codes": "23.080",
            "category": "Pumps & Fluid Handling",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-5120",
            "is_number": "IS 5120:1977",
            "title": "Technical Requirements for Rotodynamic Special Purpose Pumps",
            "scope": "Covers general technical requirements for rotodynamic pumps including centrifugal, mixed flow, and axial flow pumps used for industrial processes, chemical plants, sewage, and special service conditions.",
            "status": "ACTIVE",
            "publication_date": "1977-10-10",
            "revision_date": "2020-02-14",
            "ics_codes": "23.080",
            "category": "Pumps & Fluid Handling",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-9137",
            "is_number": "IS 9137:1978",
            "title": "Code for Acceptance Tests for Centrifugal, Mixed Flow and Axial Pumps - Class C",
            "scope": "Specifies test procedures, measurement tolerances, instrumentation requirements, and acceptance standards for Class C performance testing of centrifugal, mixed flow, and axial pumps.",
            "status": "ACTIVE",
            "publication_date": "1978-08-30",
            "revision_date": "2019-04-12",
            "ics_codes": "23.080",
            "category": "Pumps & Fluid Handling",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-11346",
            "is_number": "IS 11346:2002",
            "title": "Code of Practice for Selection, Installation and Maintenance of Centrifugal Pumps",
            "scope": "Provides guidelines and mandatory practices for suction layout, foundation design, alignment, piping connections, electrical wiring, startup procedure, and preventative maintenance of centrifugal pump sets.",
            "status": "ACTIVE",
            "publication_date": "2002-04-15",
            "revision_date": "2021-07-08",
            "ics_codes": "23.080",
            "category": "Pumps & Fluid Handling",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-325",
            "is_number": "IS 325:1996",
            "title": "Three-Phase Induction Motors - Specification",
            "scope": "Covers performance, dimensions, insulation class, and thermal test specifications for general purpose 3-phase squirrel cage induction electric motors.",
            "status": "SUPERSEDED",
            "publication_date": "1996-01-01",
            "revision_date": "2018-01-01",
            "ics_codes": "29.160.30",
            "category": "Electrical Motors & Drives",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL",
            "replaced_by_is": "IS 12615:2018"
        },
        {
            "id": "std-12615",
            "is_number": "IS 12615:2018",
            "title": "Energy Efficient Three Phase Squirrel Cage Induction Motors (IE2, IE3, IE4)",
            "scope": "Specifies energy efficiency classes (IE2, IE3, IE4), performance parameters, loss determination methods, and compulsory labeling for 3-phase squirrel cage induction motors from 0.12 kW to 1000 kW.",
            "status": "ACTIVE",
            "publication_date": "2018-03-25",
            "revision_date": "2023-09-10",
            "ics_codes": "29.160.30",
            "category": "Electrical Motors & Drives",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-1180",
            "is_number": "IS 1180 (Part 1):2014",
            "title": "Outdoor Type Oil Immersed Distribution Transformers Up to 2500 kVA, 33 kV",
            "scope": "Specifies standard losses, ratings, temperature rise limits, short-circuit withstand capacity, and safety fittings for outdoor oil-immersed distribution transformers up to 2500 kVA.",
            "status": "ACTIVE",
            "publication_date": "2014-06-12",
            "revision_date": "2022-11-05",
            "ics_codes": "29.180",
            "category": "Electrical Power Systems",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-732",
            "is_number": "IS 732:2019",
            "title": "Code of Practice for Electrical Wiring Installations",
            "scope": "Defines fundamental safety, design, conductor sizing, grounding/earthing, surge protection, and inspection specifications for electrical wiring installations in residential, commercial, and industrial facilities.",
            "status": "ACTIVE",
            "publication_date": "2019-02-18",
            "revision_date": "2024-01-15",
            "ics_codes": "91.140.50",
            "category": "Electrical Safety & Wiring",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-14286",
            "is_number": "IS 14286 (Part 1):2019 / IEC 61215-1",
            "title": "Terrestrial Photovoltaic (PV) Modules - Design Qualification and Type Approval",
            "scope": "Specifies test sequences, thermal cycling, humidity freeze, mechanical load, and electrical performance requirements for terrestrial crystalline silicon and thin-film solar PV modules.",
            "status": "ACTIVE",
            "publication_date": "2019-08-10",
            "revision_date": "2023-05-18",
            "ics_codes": "27.160",
            "category": "Solar Energy Systems",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-16270",
            "is_number": "IS 16270:2014",
            "title": "Secondary Cells and Batteries for Solar Photovoltaic Application",
            "scope": "Covers performance criteria, discharge capacity, safety vents, charge efficiency, and life testing for lead-acid and lithium batteries used in off-grid and grid-interactive solar PV installations.",
            "status": "ACTIVE",
            "publication_date": "2014-11-20",
            "revision_date": "2021-12-01",
            "ics_codes": "29.220.20",
            "category": "Solar Energy Systems",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-778",
            "is_number": "IS 778:1984",
            "title": "Copper Alloy Gate, Globe and Check Valves for Water Works",
            "scope": "Specifies manufacturing tolerances, pressure-temperature ratings, hydrostatic testing, and material composition for bronze/copper alloy gate, globe, and non-return check valves.",
            "status": "ACTIVE",
            "publication_date": "1984-04-10",
            "revision_date": "2020-08-15",
            "ics_codes": "23.060.01",
            "category": "Pipes, Valves & Fittings",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-4984",
            "is_number": "IS 4984:2016",
            "title": "High Density Polyethylene (HDPE) Pipes for Water Supply - Specification",
            "scope": "Specifies raw material grades (PE 63, PE 80, PE 100), dimensions, hydrostatic strength, oxidation induction time, and pressure classes for HDPE pipes used in water supply and distribution.",
            "status": "ACTIVE",
            "publication_date": "2016-07-22",
            "revision_date": "2023-10-30",
            "ics_codes": "23.040.20",
            "category": "Pipes, Valves & Fittings",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        },
        {
            "id": "std-10500",
            "is_number": "IS 10500:2012",
            "title": "Drinking Water Specifications",
            "scope": "Prescribes organoleptic, physical, chemical, toxic, and bacteriological requirements and permissible limits for drinking water suitable for human consumption.",
            "status": "ACTIVE",
            "publication_date": "2012-06-01",
            "revision_date": "2021-03-12",
            "ics_codes": "13.060.20",
            "category": "Water & Environment",
            "source": "Bureau of Indian Standards (BIS)",
            "source_type": "OFFICIAL"
        }
    ]

    for item in standards_data:
        db.add(Standard(**item))
    db.commit()

    # 2. AMENDMENTS
    amendments_data = [
        {
            "standard_id": "std-1520",
            "amendment_number": 1,
            "date": "2012-03-15",
            "description": "Updated hydraulic efficiency calculation factors and impeller balancing tolerances under Clause 4.2.",
            "source": "BIS Gazette Notification 2012/AM-1"
        },
        {
            "standard_id": "std-1520",
            "amendment_number": 2,
            "date": "2018-11-20",
            "description": "Incorporated mandatory compliance with IS 12615 IE3 energy efficiency rating for coupled electric drive motors.",
            "source": "BIS Gazette Notification 2018/AM-2"
        },
        {
            "standard_id": "std-12615",
            "amendment_number": 1,
            "date": "2021-05-10",
            "description": "Mandated minimum IE3 efficiency class for all 3-phase induction motors from 0.75 kW up to 375 kW under Quality Control Order (QCO).",
            "source": "Ministry of Heavy Industries Order S.O. 1820(E)"
        },
        {
            "standard_id": "std-1180",
            "amendment_number": 1,
            "date": "2016-09-01",
            "description": "Mandated maximum total losses at 50% and 100% loading for Star 1, Star 2, and Star 3 efficiency ratings.",
            "source": "Bureau of Energy Efficiency (BEE) / BIS Gazette"
        },
        {
            "standard_id": "std-14286",
            "amendment_number": 1,
            "date": "2022-02-14",
            "description": "Added safety requirement for ALMM (Approved List of Models and Manufacturers) registration and BIS compulsory registration scheme (CRS).",
            "source": "MNRE Gazette Notification 2022"
        }
    ]

    for am in amendments_data:
        db.add(Amendment(**am))
    db.commit()

    # 3. STANDARD RELATIONSHIPS
    relationships_data = [
        # IS 1520 relationships
        {
            "source_standard_id": "std-1520",
            "target_standard_id": "std-9137",
            "relationship_type": "TEST_METHOD",
            "evidence": "Clause 8.1 of IS 1520 specifies that hydraulic acceptance testing of pumps shall strictly follow test procedures outlined in IS 9137 Class C."
        },
        {
            "source_standard_id": "std-1520",
            "target_standard_id": "std-11346",
            "relationship_type": "INSTALLATION",
            "evidence": "Clause 12.4 of IS 1520 mandates that site installation, suction alignment, and foundation grounding shall comply with IS 11346."
        },
        {
            "source_standard_id": "std-1520",
            "target_standard_id": "std-12615",
            "relationship_type": "NORMATIVE_REFERENCE",
            "evidence": "Clause 5.2 specifies that coupled 3-phase electric motors must conform to IS 12615 for energy efficiency."
        },
        {
            "source_standard_id": "std-1520",
            "target_standard_id": "std-778",
            "relationship_type": "RELATED",
            "evidence": "Suction and delivery valves used with IS 1520 centrifugal pump sets shall conform to IS 778 copper alloy gate and check valves."
        },

        # IS 325 -> IS 12615
        {
            "source_standard_id": "std-325",
            "target_standard_id": "std-12615",
            "relationship_type": "SUPERSEDES",
            "evidence": "IS 12615:2018 officially supersedes IS 325:1996 for line-operated 3-phase squirrel cage induction motors to mandate higher energy efficiency standards."
        },

        # IS 5120 relationships
        {
            "source_standard_id": "std-5120",
            "target_standard_id": "std-9137",
            "relationship_type": "TEST_METHOD",
            "evidence": "IS 5120 rotodynamic special purpose pump specifications require hydro testing and performance acceptance per IS 9137."
        },

        # IS 12615 safety & wiring
        {
            "source_standard_id": "std-12615",
            "target_standard_id": "std-732",
            "relationship_type": "SAFETY",
            "evidence": "Electrical connection, terminal box IP protection, and earthing of motors shall comply with IS 732 wiring safety code."
        },

        # Solar PV relationships
        {
            "source_standard_id": "std-14286",
            "target_standard_id": "std-16270",
            "relationship_type": "NORMATIVE_REFERENCE",
            "evidence": "Solar PV system deployments utilizing battery storage under IS 14286 require battery storage units conforming to IS 16270."
        },
        {
            "source_standard_id": "std-14286",
            "target_standard_id": "std-732",
            "relationship_type": "SAFETY",
            "evidence": "DC wiring and AC grid interconnection safety must comply with IS 732 earthing and surge protection rules."
        }
    ]

    for rel in relationships_data:
        db.add(StandardRelationship(**rel))
    db.commit()

    # 4. CERTIFICATION RULES (Deterministic / Gazette orders)
    certification_data = [
        {
            "product": "Centrifugal Pumps for Clear, Cold Water",
            "scheme": "BIS Product Certification (ISI Mark)",
            "standard_id": "std-1520",
            "mandatory": True,
            "conditions": "Mandatory ISI marking required for public procurement under Ministry of Commerce & Industry Quality Control Order (QCO).",
            "source": "Gazette Order S.O. 2481(E) - Electrical & Mechanical Equipment QCO"
        },
        {
            "product": "Energy Efficient 3-Phase Induction Motors",
            "scheme": "Mandatory QCO + BIS Certification (ISI Mark)",
            "standard_id": "std-12615",
            "mandatory": True,
            "conditions": "All 3-phase induction motors from 0.75 kW to 375 kW sold or imported in India must bear ISI mark under IS 12615 with minimum IE3 rating.",
            "source": "Ministry of Heavy Industries Quality Control Order 2021"
        },
        {
            "product": "Outdoor Oil Immersed Distribution Transformers",
            "scheme": "BIS Product Certification + BEE Star Labeling",
            "standard_id": "std-1180",
            "mandatory": True,
            "conditions": "Mandatory BIS certification and Bureau of Energy Efficiency (BEE) Star rating label mandatory prior to grid connection.",
            "source": "Central Electricity Authority (CEA) Technical Standards Regulations"
        },
        {
            "product": "Crystalline Silicon Terrestrial Photovoltaic (PV) Modules",
            "scheme": "BIS Compulsory Registration Scheme (CRS) + ALMM",
            "standard_id": "std-14286",
            "mandatory": True,
            "conditions": "Mandatory BIS CRS registration and inclusion in MNRE Approved List of Models and Manufacturers (ALMM).",
            "source": "Solar Photovoltaics, Systems, Devices and Components Goods QCO 2018"
        },
        {
            "product": "HDPE Pipes for Water Supply",
            "scheme": "BIS Product Certification (ISI Mark)",
            "standard_id": "std-4984",
            "mandatory": True,
            "conditions": "Mandatory BIS license required for government municipal and rural water supply schemes (Jal Jeevan Mission).",
            "source": "Department of Drinking Water & Sanitation Guidelines"
        }
    ]

    for cert in certification_data:
        db.add(CertificationRule(**cert))
    db.commit()

    print("[MANAK ANVESHAN] Database seeded successfully with Indian Standards demo knowledge base.")
