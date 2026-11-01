# 🩺 CuraPulse AI — Grounded Clinical Knowledge & Diagnosis Assistant

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain%200.3-emerald.svg)](https://www.langchain.com/)
[![LLM](https://img.shields.io/badge/LLM-Google%20Gemini%202.5%20Pro-4285F4.svg)](https://ai.google.dev/)
[![Vector Store](https://img.shields.io/badge/VectorDB-ChromaDB%20%7C%20Pinecone-orange.svg)](https://www.trychroma.com/)
[![UI](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**CuraPulse AI** is an advanced Retrieval-Augmented Generation (RAG) healthcare assistant designed to provide accurate, verified, and grounded medical information. Built on top of *The Gale Encyclopedia of Medicine*, CuraPulse AI synthesizes clinical knowledge across 1,700+ medical disorders, treatments, and procedures to provide reliable patient guidance with strict medical citations.

---

## 🌟 Key Features

* **Strict Clinical Grounding**: Responses are strictly synthesized from authoritative medical literature with page-level source citations.
* **Hybrid Vector Architecture**: Supports zero-cost, offline **ChromaDB** out-of-the-box, with optional cloud-scale **Pinecone** integration.
* **Conversational Context Memory**: Maintains multi-turn context with question reformulations (`create_history_aware_retriever`).
* **Interactive Clinical UI**: Modern Streamlit interface featuring token streaming, customizable retrieval parameters ($k$), and emergency safety alerts.
* **Clinical Safety Guardrails**: Detects critical symptom descriptions and proactively alerts users to contact emergency services (911/112).
* **Zero-Cost Embeddings**: Employs `sentence-transformers/all-MiniLM-L6-v2` locally on CPU with zero inference costs or external embedding API limits.

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION PIPELINE                     │
│  [Medical_book.pdf] ──► [Chunker (1000 chars)] ──► [all-MiniLM] │
│                                                          │      │
│                                                          ▼      │
│                     [ChromaDB / Pinecone Store] ◄────────┘      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CONVERSATIONAL RAG WORKFLOW                   │
│                                                                 │
│   [User Query] ──► [Contextualizer + Chat History]              │
│                           │                                     │
│                           ▼                                     │
│                 [Semantic Vector Search]                        │
│                           │                                     │
│                           ▼                                     │
│             [Top-K Clinical Context + Metadata]                 │
│                           │                                     │
│                           ▼                                     │
│         [Strict System Prompt] + [Google Gemini LLM]            │
│                           │                                     │
│                           ▼                                     │
│         [Streaming Answer] + [📚 Source Citations]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
CuraPulse-AI/
├── .env.example              # Environment variable template
├── .gitignore                # Production gitignore rules
├── app.py                    # Streamlit conversational web assistant
├── data/
│   └── Medical_book.pdf      # The Gale Encyclopedia of Medicine (16MB)
├── ingest.py                 # Automated PDF loader & vector indexer
├── requirements.txt          # Python project dependencies
├── setup.py                  # Package configuration & author metadata
├── src/
│   ├── __init__.py
│   ├── helper.py             # Document loading, cleaning, chunking & embeddings
│   └── prompt.py             # Clinical system prompts & safety guidelines
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python**: 3.10 or higher
* **Git**: Installed on your machine
* **Google Gemini API Key**: Free key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 2. Clone and Setup Environment

```bash
git clone https://github.com/Aryan-123-app/CuraPulse-AI.git
cd CuraPulse-AI

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```ini
GEMINI_API_KEY=AIzaSy...your_gemini_api_key_here
VECTOR_STORE_TYPE=chroma

# Optional: Only needed if using cloud Pinecone
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX_NAME=curapulse-medical
```

### 4. Ingest Medical Literature

Run the automated ingestion pipeline to index the medical book:

```bash
# Option A: Local ChromaDB (Recommended - runs offline with zero setup)
python ingest.py --store chroma

# Fast test run (ingest first 50 pages for instant testing)
python ingest.py --store chroma --limit 50

# Option B: Pinecone Cloud (If you have a Pinecone account)
python ingest.py --store pinecone
```

### 5. Launch the Web Assistant

```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 💡 Usage Example

1. **Ask a Clinical Question**:
   > *"What causes an Abdominal Aortic Aneurysm, and what diagnostic procedures are typically recommended?"*

2. **CuraPulse AI Response**:
   * **Clinical Summary**: Explains the dilation of the abdominal aorta and common vascular causes.
   * **Diagnosis**: Details how abdominal ultrasound and CT scans are utilized.
   * **Verified Citations**: Expand the `📚 Verified Clinical Citations` box to inspect the exact pages from *The Gale Encyclopedia of Medicine* referenced by the model.

---

## 🛡️ Medical Disclaimer

> **IMPORTANT**: CuraPulse AI is intended solely for informational and educational reference. It does not offer clinical diagnoses, personalized medical treatment plans, or emergency services. Always consult a licensed medical provider for diagnostic evaluation. In a medical emergency, immediately contact local emergency services (**911 / 112**).

---

## 👨‍💻 Author

**Aryan Patade**
* GitHub: [@Aryan-123-app](https://github.com/Aryan-123-app)
* Email: [aryanpatade8@gmail.com](mailto:aryanpatade8@gmail.com)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
