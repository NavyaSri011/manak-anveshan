# MANAK ANVESHAN
### Indian Standards Intelligence for Procurement (SIH 2026 Prototype)

MANAK ANVESHAN is an AI-powered decision-support system designed for public procurement officials, tender evaluation committees, and technical auditors to automatically match procurement specifications with authoritative Bureau of Indian Standards (BIS), verify Quality Control Orders (QCO), flag superseded standard references (e.g. IS 325), and generate procurement-ready compliance reports.

---

## 🚀 Key Features & Capabilities

1. **Document Parsing & Requirement Normalization**: Converts raw tender text, technical specification JSON/key-values, or uploaded documents into canonical requirements.
2. **Multilingual Query Processing**: Supports English, Hindi (हिन्दी), Tamil (தமிழ்), and Marathi (मराठी).
3. **Hybrid Retrieval Engine**: Combines lexical (BM25), TF-IDF semantic embeddings, metadata/ICS matching, and attribute matching.
4. **Applicability Classification Engine**: Classifies standards into `PRIMARY`, `SUPPORTING`, `NORMATIVE_REFERENCE`, `TEST_METHOD`, `SAFETY`, `INSTALLATION`, and `RELATED`.
5. **Version & Lifecycle Intelligence**: Detects outdated/superseded standards (e.g. flagging IS 325 replaced by IS 12615) with explicit procurement alerts.
6. **Mandatory QCO Regulatory Engine**: Deterministic rules engine checking BIS Product Certification (ISI Mark), CRS, and Quality Control Orders.
7. **Missing Requirement Detection**: Identifies specification gaps (e.g. missing fluid operating temperature or material grade).
8. **Standards Relationship Graph**: Interactive React Flow visualizer for Product → Primary Standard → Test / Safety / Installation / Normative / QCO links.
9. **Mock GeM Procurement Portal**: Realistic enterprise procurement interface demonstrating live embedded backend API integration (`POST /api/v1/standards/analyze`).
10. **Procurement Report Generator**: Printable PDF/DOCX layout, executive summary, JSON export, and signature block.
11. **Evaluation Module**: Comparative benchmark metrics (Precision@K, Recall@K, MRR, NDCG, F1, 0% Hallucination Rate).

---

## 🛠️ Project Structure

```text
project/
├── frontend/             # React + Vite + Tailwind CSS + React Flow frontend
│   ├── src/
│   │   ├── components/   # Header, Footer, StandardCard, WhyRecommendedModal, RequirementEditor
│   │   ├── pages/        # Dashboard, NewAnalysis, AnalysisResults, StandardsExplorer, StandardsGraph, TenderHistory, MockPortal, Reports, SettingsAbout
│   │   └── services/     # Axios API client
│   └── vite.config.js
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── api/          # FastAPI routers (/health, /standards, /analyses, /evaluation)
│   │   ├── core/         # Settings & environment configuration
│   │   ├── database/     # SQLAlchemy connection, SQLite/Postgres models, seed data
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   └── services/     # Modular extraction, hybrid retrieval, applicability, lifecycle, QCO, graph & evaluation services
│   ├── run.py            # Uvicorn server launcher
│   └── requirements.txt
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## ⚡ Quick Start (Local Setup)

### 1. Run Backend Server
```bash
cd backend
pip install -r requirements.txt
python run.py
```
The API backend will start on `http://127.0.0.1:8000` and automatically seed the database with Indian Standards. API documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Run Frontend Development Server
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## ⚖️ SIH 2026 Prototype Notice
This software is a decision-support prototype submitted for SIH 2026. It is designed to assist human procurement committees and does not claim official affiliation with the Bureau of Indian Standards (BIS) or Government of India.
