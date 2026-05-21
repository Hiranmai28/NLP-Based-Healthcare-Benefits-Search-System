# 🏥 NLP-Based Healthcare Benefits Search System
**Author:** Hiranmai Devarasetty

An AI-powered semantic search system to help users understand and compare health insurance benefits across Massachusetts insurance plans.

![AI-Powered](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-NLP-purple)

## 🌟 Live Demo

🔗 **[Try the Live App]((https://nlp-based-healthcare-benefits-search-system.streamlit.app/))**

---

## 📖 Overview

The NLP-Based Healthcare Benefits Search System uses **Natural Language Processing** and **semantic vector search** to help users navigate complex insurance benefit documents. Instead of reading through lengthy PDFs, users can simply ask questions in plain English and get accurate, ranked answers from across 9 Massachusetts insurance plans.

**What you can do:**
- 🔍 Search insurance benefits using natural language questions
- ⚖️ Compare coverage across multiple plans side-by-side
- 💰 Understand costs, copays, and deductibles
- 🎯 Filter results by plan, carrier, or benefit category
- 📋 Browse all 9 Massachusetts insurance plans

---

## ✨ Features

- **Semantic Search** — Understands the *meaning* of your query, not just keywords
- **Multi-Plan Search** — Searches across all 9 MA insurance plans simultaneously
- **Smart Filtering** — Filter by plan name or benefit category
- **Plan Comparison** — Compare how different plans cover the same benefit
- **Auto-Categorization** — Benefits are auto-tagged (dental, vision, prescription, mental health, etc.)
- **Interactive UI** — Clean Streamlit web interface with sample questions

---

## 🛠️ Technology Stack

### AI & Machine Learning
| Technology | Version | Purpose |
|---|---|---|
| **Sentence Transformers** | 2.2.2 | Semantic text embeddings (`all-MiniLM-L6-v2`, 384 dims) |
| **FAISS** | 1.7.4 | Fast vector similarity search (IndexFlatIP) |
| **PyTorch** | 2.1.0 | Deep learning framework underlying transformers |
| **XGBoost** | 2.0.3 | Optional reranking model (scaffolded) |
| **scikit-learn** | 1.3.2 | ML utilities |

### Data Processing
| Technology | Version | Purpose |
|---|---|---|
| **pdfplumber** | 0.10.3 | PDF text extraction |
| **ReportLab** | 4.0.7 | PDF generation for insurance plan documents |
| **NumPy** | 1.24.3 | Embedding array operations |
| **Pandas** | 2.1.4 | Data manipulation |

### Web & API
| Technology | Version | Purpose |
|---|---|---|
| **Streamlit** | 1.29.0 | Interactive web UI |
| **FastAPI** | 0.108.0 | REST API backend (scaffolded) |
| **Uvicorn** | 0.25.0 | ASGI server |

### Utilities
| Technology | Purpose |
|---|---|
| **python-dotenv** | Environment variable management (`.env`) |
| **Pydantic** | Data validation |
| **tqdm** | Progress bars |

---

## 📊 Architecture & Data Flow

```
┌─────────────────────── SETUP PIPELINE (run once) ──────────────────────────┐
│                                                                              │
│  generate_dummy_data.py  →  pdf_extractor.py  →  chunker.py                │
│    (9 MA insurance plans)     (structured JSON)    (~157 benefit chunks)    │
│                                      ↓                                      │
│                          embedding_generator.py                             │
│                     (all-MiniLM-L6-v2 → 384-dim vectors)                   │
│                                      ↓                                      │
│              FAISS Index  +  Chunks Pickle  +  Embeddings  +  Metadata     │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────── QUERY PIPELINE (runtime) ────────────────────────────┐
│                                                                              │
│  User Query  →  Sentence Transformer  →  384-dim Vector                    │
│                                               ↓                             │
│                                     FAISS Cosine Search                     │
│                                               ↓                             │
│                           Top-K Candidates + Similarity Scores              │
│                                               ↓                             │
│                           Optional Plan / Category Filter                   │
│                                               ↓                             │
│                               Ranked Results → Streamlit UI                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Why cosine similarity?** Embeddings are L2-normalized, so FAISS inner product search is mathematically equivalent to cosine similarity — capturing semantic meaning rather than surface-level word overlap.

---

## 🏥 Insurance Plans Included

| Plan | Provider | Type | Monthly Premium |
|---|---|---|---|
| BlueCross HMO Blue New England | Blue Cross Blue Shield MA | HMO | $450 |
| BlueCross PPO Blue | Blue Cross Blue Shield MA | PPO | $550 |
| Tufts Medicare Preferred HMO | Tufts Health Plan | Medicare Advantage | $0 |
| Harvard Pilgrim HMO | Harvard Pilgrim Health Care | HMO | $420 |
| Fallon Health Direct Care HMO | Fallon Health | HMO | $395 |
| Health New England HMO | Health New England | HMO | $380 |
| WellSense Health Plan HMO | WellSense Health Plan | HMO | $340 |
| Mass General Brigham Health Plan HMO | Mass General Brigham | HMO | $490 |
| AllWays Health Partners HMO | AllWays Health Partners | HMO | $410 |

**Total indexed:** ~157 benefit chunks across 14 benefit categories

---

## 📁 Project Structure

```
NLP-Based-Healthcare-Benefits-Search-System/
├── data/
│   ├── Insurance_dataset/      # Generated insurance plan PDFs & JSONs
│   ├── processed/              # Extracted & chunked benefit data
│   │   └── all_chunks.json     # Aggregated chunks for all plans
│   └── index/                  # FAISS index & embeddings (built artifacts)
│       ├── benefits.index
│       ├── chunks.pkl
│       ├── embeddings.npy
│       └── metadata.json
├── src/
│   ├── data_processing/
│   │   ├── generate_dummy_data.py   # Generates 9 MA plan PDFs
│   │   ├── pdf_extractor.py         # Extracts text from PDFs
│   │   └── chunker.py               # Creates searchable chunks
│   ├── models/
│   │   ├── embedding_generator.py   # Builds FAISS vector index
│   │   ├── retriever.py             # Core semantic search engine
│   │   └── reranker.py              # XGBoost reranker (scaffolded)
│   ├── pipelines/
│   │   └── rag_pipeline.py          # RAG pipeline coordinator
│   └── api/
│       └── app.py                   # FastAPI REST endpoints
├── streamlit_app.py            # Main web interface
├── run_pipeline.py             # CLI chatbot interface
├── requirements.txt
├── .env                        # API keys (not committed)
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- 4GB+ RAM
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hiranmai28/NLP-Based-Healthcare-Benefits-Search-System.git
cd NLP-Based-Healthcare-Benefits-Search-System
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the full data pipeline** (one-time setup)
```bash
python src/data_processing/generate_dummy_data.py
python src/data_processing/pdf_extractor.py
python src/data_processing/chunker.py
python src/models/embedding_generator.py
```

5. **Launch the app**
```bash
streamlit run streamlit_app.py
```

Open **http://localhost:8501** in your browser.

---

## 🎯 Usage Examples

### Web Interface
```bash
streamlit run streamlit_app.py
```
Try queries like:
- *"Does my plan cover gym membership?"*
- *"What is the copay for seeing a specialist?"*
- *"Is mental health treatment covered?"*
- *"How much do prescription drugs cost?"*

### Programmatic Usage
```python
from src.models.retriever import BenefitRetriever

retriever = BenefitRetriever()

# Search across all plans
results = retriever.search("Does my plan cover dental?", top_k=5)

# Filter by specific plan
results = retriever.search("gym membership", plan_filter="Harvard Pilgrim HMO")

# Filter by category
results = retriever.search("medication costs", category_filter="prescription")

for result in results:
    print(f"{result['plan_name']}: {result['text']} (score: {result['similarity_score']:.2f})")
```

### Adding Real Insurance PDFs
1. Place your PDF files in `data/Insurance_dataset/`
2. Re-run the pipeline:
```bash
python src/data_processing/pdf_extractor.py
python src/data_processing/chunker.py
python src/models/embedding_generator.py
```

---

## 🔧 Configuration

### Search Parameters
```python
# In src/models/retriever.py
retriever.search(
    query="your question",
    top_k=5,                          # Number of results (default: 5)
    plan_filter="BlueCross HMO",      # Optional: filter by plan
    category_filter="dental"          # Optional: filter by category
)
```

### Benefit Categories
The system auto-classifies benefits into 14 categories:
`general`, `hospital`, `prescription`, `emergency`, `preventive`, `specialist`, `primary_care`, `dental`, `vision`, `mental_health`, `wellness`, `telehealth`, `therapy`, `transportation`

---

## 📈 Performance

| Metric | Value |
|---|---|
| Search latency | < 100ms per query |
| Plans indexed | 9 Massachusetts insurers |
| Total chunks | ~157 benefit chunks |
| Embedding dimensions | 384 |
| Index type | FAISS IndexFlatIP (exact cosine search) |
| Memory usage | ~500MB (models + index) |

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
