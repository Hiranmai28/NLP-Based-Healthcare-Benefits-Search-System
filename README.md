# 🏥 NLP-Based Healthcare Benefits Search System
- Hiranmai Devarasetty
An AI-powered semantic search system to help users understand and compare health insurance benefits across different plans.

![Healthcare Search System](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)

## 🌟 Live Demo

🔗 **[Try the Live App](https://your-app-name.streamlit.app)** _(Add your URL after deployment)_

## 📖 Overview

NLP-Based Healthcare Benefits Search System is an intelligent system that uses Natural Language Processing (NLP) and semantic search to help users:
- 🔍 Search insurance benefits using natural language
- ⚖️ Compare coverage across multiple plans
- 💰 Understand costs and copays
- 🎯 Find specific benefits quickly

## ✨ Features

### Core Capabilities
- **Semantic Search**: Ask questions naturally, get relevant answers
- **Multi-Plan Search**: Search across all insurance plans simultaneously
- **Smart Filtering**: Filter by plan, category, or benefit type
- **Plan Comparison**: Side-by-side benefit comparisons
- **Category Classification**: Auto-categorizes benefits (dental, vision, prescription, etc.)

### Technical Features
- **AI-Powered Embeddings**: Uses Sentence-BERT for semantic understanding
- **Vector Search**: FAISS for lightning-fast similarity search
- **RAG Architecture**: Retrieval-Augmented Generation pattern
- **Modern UI**: Beautiful Streamlit web interface

## 🛠️ Technology Stack

### AI & Machine Learning
- **Sentence Transformers** (2.2.2) - Text embeddings
- **FAISS** - Vector similarity search
- **PyTorch** - Deep learning framework

### Backend
- **Python 3.11**
- **pdfplumber** - PDF text extraction
- **NumPy & Pandas** - Data processing

### Frontend
- **Streamlit** - Web interface
- **Custom CSS** - Enhanced styling

## 📊 Architecture
```
User Query
    ↓
Sentence-BERT Embedding
    ↓
FAISS Vector Search
    ↓
Top-K Retrieval
    ↓
Result Ranking
    ↓
Display Results
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- 4GB+ RAM
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hiranmai28/NLP-Based-Healthcare-Benefits-Search-System.git
cd NLP-Based Healthcare Benefits Search System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Generate dummy data**
```bash
python src/data_processing/generate_dummy_data.py
```

5. **Extract and process PDFs**
```bash
python src/data_processing/pdf_extractor.py
python src/data_processing/chunker.py
```

6. **Build search index**
```bash
python src/models/embedding_generator.py
```

7. **Run the app**
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure
```
NLP-Based Healthcare Benefits Search System/
├── data/
│   ├── dummy_dataset/      # Generated insurance PDFs
│   ├── processed/          # Extracted & chunked data
│   └── index/              # FAISS index & embeddings
├── src/
│   ├── data_processing/
│   │   ├── generate_dummy_data.py
│   │   ├── pdf_extractor.py
│   │   └── chunker.py
│   └── models/
│       ├── embedding_generator.py
│       └── retriever.py
├── streamlit_app.py        # Web interface
├── requirements.txt
└── README.md
```

## 🎯 Usage Examples

### Web Interface (Streamlit)
```bash
streamlit run streamlit_app.py
```

### Command Line Chatbot
```bash
python chatbot.py
```

### Programmatic Usage
```python
from src.models.retriever import BenefitRetriever

# Initialize retriever
retriever = BenefitRetriever()

# Search for benefits
results = retriever.search("Does my plan cover gym membership?", top_k=5)

# Display results
for result in results:
    print(f"{result['plan_name']}: {result['text']}")
```

## 📊 Sample Data

The project includes 3 dummy insurance plans:
- **BlueCross HMO Blue New England** - HMO plan with $450/month premium
- **BlueCross PPO Blue** - PPO plan with $550/month premium  
- **Tufts Medicare Preferred HMO** - Medicare Advantage with $0 premium

Total benefits indexed: **~50-60 benefits** across all plans

## 🔧 Configuration

### Adjusting Search Parameters

Edit `src/models/retriever.py`:
```python
# Change number of results
results = retriever.search(query, top_k=10)  # Default: 5

# Filter by plan
results = retriever.search(query, plan_filter="BlueCross HMO")

# Filter by category
results = retriever.search(query, category_filter="dental")
```

### Using Real Insurance PDFs

1. Place PDF files in `data/dummy_dataset/`
2. Run extraction pipeline:
```bash
python src/data_processing/pdf_extractor.py
python src/data_processing/chunker.py
python src/models/embedding_generator.py
```

## 🧪 Testing

Run test queries:
```bash
python src/models/retriever.py
```

Test the chatbot:
```bash
python chatbot.py
# Type: Does my plan cover dental?
```

## 📈 Performance

- **Search Speed**: <100ms per query
- **Index Size**: ~52 chunks (expandable to 1000s)
- **Accuracy**: Semantic similarity matching
- **Memory**: ~500MB for models + index

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request



