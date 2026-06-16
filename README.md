# 🚀 SalesOrbit

> An agentic B2B sales prospecting system powered by LangGraph, ChromaDB RAG, OCR ingestion, Celery workers, and a Streamlit dashboard — built to automatically research, score, and recommend next actions for sales prospects.

---

## 📌 Overview

SalesOrbit is a **multi-agent AI system** for B2B sales teams. It ingests prospect signals (LinkedIn role, intent data), retrieves relevant context from a vector knowledge base (text files + OCR-scanned business cards), scores each prospect using a rule-based + signal-aware engine, and recommends the best next action — all orchestrated via a **LangGraph state machine**.

The system exposes both a **FastAPI backend** (for event-driven ingestion) and a **Streamlit UI** (for manual pipeline execution and result visualization).

---

## ✨ Features

- 🤖 **Multi-Agent Workflow** — LangGraph state graph with `research` and `scoring` nodes
- 📚 **Dual RAG Pipeline** — Retrieves from both plain text files and OCR-scanned images (business cards)
- 🔍 **ChromaDB Vector Store** — Persistent local vector database with `all-MiniLM-L6-v2` embeddings
- 📷 **OCR Ingestion** — Extracts text from PNG/JPG images via `pytesseract` and indexes into ChromaDB
- ⚡ **Celery Workers** — Async background signal gathering (LinkedIn + intent data)
- 🌐 **FastAPI REST API** — Event ingestion endpoint + prospect result lookup
- 🎛️ **Streamlit Dashboard** — Visual pipeline runner with progress tracking and result tables
- 🐳 **Docker Ready** — Full `docker-compose.yml` with Redis and app services
- 🧪 **Test Suite** — `pytest` tests for API endpoints and graph execution

---

## 🗂️ Project Structure

```
SalesOrbit/
│
├── streamlit_app.py          # Streamlit UI — pipeline runner and results dashboard
├── init_db.py                # Vector store initialization (text + OCR ingestion)
├── requirements.txt          # Python dependencies
├── packages.txt              # System packages (e.g. tesseract-ocr)
├── Dockerfile                # Container definition
├── docker-compose.yml        # Multi-service orchestration (app + Redis)
├── Makefile                  # Dev shortcuts
├── render.yaml               # Render.com deployment config
│
├── agents/
│   ├── graph.py              # LangGraph workflow — research + scoring nodes
│   └── state.py              # ProspectState TypedDict definition
│
├── api/
│   ├── main.py               # FastAPI app — /events/ingest + /prospects/{id}
│   └── models.py             # Pydantic request models
│
├── rag/
│   ├── text_pipeline.py      # ChromaDB text ingestion + retrieval
│   └── ocr_pipeline.py       # Tesseract OCR ingestion + retrieval
│
├── workers/
│   ├── celery_app.py         # Celery app config
│   └── tasks.py              # Signal gathering tasks (LinkedIn, intent)
│
├── knowledge/
│   ├── text/                 # Plain text CRM/prospect files for RAG
│   └── ocr/                  # Business card images for OCR ingestion
│
├── chroma_db/                # Persistent ChromaDB vector store (auto-generated)
│
└── tests/
    ├── conftest.py           # Pytest fixtures
    ├── test_api.py           # FastAPI endpoint tests
    └── test_graph.py         # LangGraph agent tests
```

---

## ⚙️ How It Works

```
Prospect ID + Event Trigger
         │
         ▼
┌─────────────────────────────────┐
│         LangGraph Workflow       │
│                                  │
│  ┌──────────────────────────┐   │
│  │      research_node        │   │
│  │  ┌──────────┐ ┌────────┐ │   │
│  │  │Text RAG  │ │OCR RAG │ │   │  ← ChromaDB retrieval
│  │  │(CRM data)│ │(Biz    │ │   │
│  │  │          │ │ cards) │ │   │
│  │  └──────────┘ └────────┘ │   │
│  └──────────────────────────┘   │
│              │                   │
│              ▼                   │
│  ┌──────────────────────────┐   │
│  │      scoring_node         │   │
│  │  Intent Signal + Role     │   │  ← Rule-based scoring
│  │  Score: 0–100             │   │
│  └──────────────────────────┘   │
└─────────────────┬───────────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │  Score-based Action  │
       ├──────────────────────┤
       │ ≥ 90  → Call Now     │
       │ ≥ 75  → Send Email   │
       │ ≥ 50  → LinkedIn DM  │
       │ < 50  → Review       │
       └──────────────────────┘
```

---

## 🔧 Requirements

### System Requirements

- Python 3.11+
- Redis (for Celery broker) — included via Docker
- Tesseract OCR (`tesseract-ocr` system package)
- 4 GB RAM minimum

### Install System Package (Tesseract)

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

### `requirements.txt`

```txt
fastapi
uvicorn
celery
redis
langgraph
langchain
transformers
torch
accelerate
pydantic
aiofiles
numpy
pytest-asyncio
chromadb
Pillow
pytesseract
streamlit
sentence-transformers
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 📁 Data Setup

### Knowledge Base — Text Files

Place `.txt` files with prospect/CRM data in `knowledge/text/`. Each file is ingested into ChromaDB on first run.

**Example format (`knowledge/text/prospects.txt`):**

```
Prospect ID: p-101

Company: Nexus Systems
Contact: Sarah Miller
Role: Head of Sales Operations

Notes:
- Actively evaluating AI-driven sales automation tools.
- Attended product demo last week.

Budget Information:
- Budget approved for Q2 pilot program. Estimated: $60,000

Intent Signals:
- High urgency. Interested in 60% efficiency improvement.

Recommended Action:
- Immediate follow-up call.
```

### Knowledge Base — OCR Images

Place business card images (`.png`, `.jpg`, `.jpeg`) in `knowledge/ocr/`. Tesseract extracts text and indexes it into ChromaDB under the `ocr` source tag.

### Mock Prospect Data

15 mock prospects are pre-loaded in `workers/tasks.py` with LinkedIn roles and intent signals for immediate demo use.

---

## 🚀 Setup & Running

### Option A — Local (without Docker)

#### Step 1 — Clone or unzip the project

```bash
unzip SalesOrbit-main.zip
cd SalesOrbit
```

#### Step 2 — Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

#### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 4 — Start Redis (required for Celery)

```bash
# With Docker
docker run -d -p 6379:6379 redis

# Or install locally: https://redis.io/docs/getting-started/
```

#### Step 5 — Initialize the vector store

```bash
python init_db.py
```

#### Step 6 — Run the Streamlit UI

```bash
streamlit run streamlit_app.py
```

#### Step 6b — (Optional) Run the FastAPI backend

```bash
uvicorn api.main:app --reload
```

---

### Option B — Docker Compose (recommended)

```bash
docker-compose up --build
```

This starts:
- The Streamlit app on `http://localhost:8501`
- Redis broker for Celery

---

## 💬 Usage

### Streamlit Dashboard

1. Open `http://localhost:8501`
2. Choose **Run All** or **Run Selected** from the sidebar
3. Click **Execute Research Pipeline**
4. View scored results with recommended actions in the results table

### FastAPI Endpoints

**Ingest a prospect event:**
```bash
curl -X POST http://localhost:8000/events/ingest \
  -H "Content-Type: application/json" \
  -d '{"prospect_id": "42", "event_trigger": "demo_request"}'
```

**Get prospect result:**
```bash
curl http://localhost:8000/prospects/42
```

**Sample response:**
```json
{
  "status": "completed",
  "score": 90,
  "rationale": "Scored 90 based on high signals and vp seniority.",
  "next_action": "Call Now"
}
```

---

## 🧩 Key Components

| Component | Library / Tool | Purpose |
|---|---|---|
| Agent Workflow | `langgraph` | State machine with research + scoring nodes |
| Vector Store | `chromadb` | Persistent local embedding database |
| Embeddings | `all-MiniLM-L6-v2` | Sentence-level dense vectors |
| OCR | `pytesseract` + `Pillow` | Business card text extraction |
| Task Queue | `celery` + `redis` | Async signal gathering workers |
| API | `fastapi` + `uvicorn` | REST event ingestion + result lookup |
| UI | `streamlit` | Visual pipeline runner and dashboard |
| Testing | `pytest` + `pytest-asyncio` | API and graph unit tests |

---

## ⚙️ Scoring Logic

| Condition | Points |
|---|---|
| Base score | 50 |
| High intent signal | +30 |
| Medium intent signal | +10 |
| Senior role (VP/CEO/CTO/Director/Head/Founder) | +20 |
| Maximum cap | 100 |

| Score Range | Recommended Action |
|---|---|
| ≥ 90 | 📞 Call Now |
| ≥ 75 | 📧 Send Personalized Email |
| ≥ 50 | 💼 Reach out on LinkedIn |
| < 50 | 🔍 Review & Research |

---

## 🧪 Running Tests

```bash
pytest tests/
```

Tests cover:
- FastAPI `/events/ingest` and `/prospects/{id}` endpoints
- LangGraph research and scoring node execution
- State transitions across the full agent workflow

---

## 🛠️ Troubleshooting

**`tesseract is not installed or not in PATH`**
→ Install Tesseract: `sudo apt install tesseract-ocr` (Linux) or `brew install tesseract` (macOS).

**`redis.exceptions.ConnectionError`**
→ Start Redis: `docker run -d -p 6379:6379 redis` or use `docker-compose up`.

**ChromaDB returns empty results**
→ Run `python init_db.py` to populate the vector store before launching the app.

**Streamlit shows blank results**
→ Ensure `init_db.py` completed successfully and `chroma_db/` folder is populated.

---

## 📄 License

This project is for educational and research purposes.

---

## 🙌 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent orchestration framework
- [ChromaDB](https://www.trychroma.com/) for the local vector store
- [Streamlit](https://streamlit.io/) for the rapid UI
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for image-to-text extraction
