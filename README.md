<div align="center">

<br />

<img src="https://img.shields.io/badge/RAG-Document_Q&A-0d74e7?style=for-the-badge&labelColor=24292d" alt="RAG Document Q&A" />

<br /><br />

# AI Research Assistant: Production RAG System

**Upload research papers. Ask questions. Get cited, page-grounded answers with real-time CoT streaming.**

A production-grade Retrieval-Augmented Generation (RAG) system with hybrid retrieval (BM25 + Dense vector search with RRF), cross-encoder neural reranking, multi-provider LLM inference (Groq, Gemini, OpenAI, Claude, Ollama), refusal gating, and built-in answer evaluation.

<br />

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vite.dev)
[![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-1.0-FF6F61?style=flat-square)](https://www.trychroma.com)
[![Groq](https://img.shields.io/badge/Groq-LPU_Inference-F05A28?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-2fbb4f?style=flat-square)](LICENSE)

<br />

</div>

---

## Highlights

- **Hybrid Retrieval & RRF Fusion** — Dense vector semantic search (`all-MiniLM-L6-v2`) fused with sparse BM25 keyword search via Reciprocal Rank Fusion ($k=60$) to eliminate vocabulary mismatch.
- **Neural Cross-Encoder Reranking** — Precision reranking via `ms-marco-MiniLM-L-6-v2` over-fetches top candidate chunks and calculates cross-attention for high contextual relevance.
- **Ultra-Fast & Multi-Provider LLMs** — Native support for **Groq Cloud** (800+ tok/s, no quota bottleneck), **Google AI Studio Gemini**, **OpenAI**, **Anthropic**, and local **Ollama** with automated routing.
- **Page-Level Source Attribution** — Exact PDF page number tracking (`P. X` badge) propagated from ingestion to citation cards with relevance scores and chunk inspectors.
- **Refusal Gating (Anti-Hallucination)** — Configurable similarity threshold gate (`REFUSAL_ENABLED`, default `0.25`) that honestly declines queries when retrieved context is insufficient.
- **Real-Time Streaming & CoT** — Token-by-token WebSocket streaming with collapsible Chain-of-Thought ("Thinking") reasoning phase.
- **Embedded Zero-Ops Storage** — Zero external DB containers required; in-process **ChromaDB PersistentClient** for vectors and **SQLite + SQLModel** for conversations and messages.
- **RAGAS-Inspired Evaluation & Offline Benchmark** — LLM-as-judge faithfulness scoring alongside an offline evaluation harness tested against classic ML papers.
- **Comprehensive Academic Defense Suite** — Full thesis draft, 14-slide master defense deck with verbatim speaker notes, and mock defense examiner trap answers.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          INDEXING PIPELINE                              │
│                                                                         │
│   📄 PDF / Paper  →  Parser & Page Tracker  →  Recursive Chunker       │
│      (7 formats)             │                   (512 char, 64 ovlp)    │
│                              ▼                            │             │
│                      SQLite Metadata                      ▼             │
│                      (data/rag.db)             ChromaDB Vector Store    │
│                                                (data/chroma/)           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          QUERY PIPELINE                                 │
│                                                                         │
│   ❓ User Question                                                      │
│          │                                                              │
│          ├──→ Dense Vector Search (Top-20) ──┐                          │
│          │                                   ├──→ RRF Fusion (k=60)     │
│          └──→ BM25 Keyword Search (Top-20)  ─┘          │               │
│                                                         ▼               │
│                                              Neural Cross-Encoder       │
│                                              Reranker (Top-5)           │
│                                                         │               │
│                                                         ▼               │
│                                              Refusal Gate Check         │
│                                              (Threshold >= 0.25)        │
│                                                    │          │         │
│                                         [Sufficient]      [Below Cutoff]│
│                                              │                │         │
│                                              ▼                ▼         │
│                                   ┌─ Reasoning (CoT) ─┐   Honest        │
│                                   │  Groq / Gemini    │   Refusal       │
│                                   └─────────┬─────────┘   Response      │
│                                             ▼                           │
│                                   ┌─ Generation ──────┐                 │
│                                   │ Qwen 3.8 / Gemini │                 │
│                                   └─────────┬─────────┘                 │
│                                             │                           │
│                                             ▼                           │
│                         💬 Real-Time Streaming Answer                   │
│                         🏷️ Page-Numbered Citations (P. X)              │
│                         📊 Real-Time Faithfulness Score                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

<table>
<tr>
<td width="140"><b>🖥️ Frontend</b></td>
<td>React 19 · TypeScript 5.9 · Vite 7 · Tailwind CSS v4 · shadcn/ui · TanStack Query · Lucide Icons</td>
</tr>
<tr>
<td><b>⚙️ Backend</b></td>
<td>Python 3.12+ · FastAPI · Uvicorn · SQLModel · Pydantic v2</td>
</tr>
<tr>
<td><b>🔍 Retrieval</b></td>
<td>ChromaDB (HNSW PersistentClient) · all-MiniLM-L6-v2 (384-dim) · BM25 · Reciprocal Rank Fusion · Cross-Encoder</td>
</tr>
<tr>
<td><b>🤖 LLM Providers</b></td>
<td>
  <b>Groq Cloud</b> (Qwen 3.8 27B, GPT-OSS 120B — 800+ tok/s)<br />
  <b>Google AI Studio</b> (Gemini 3.1 Flash Lite, Gemini 3.1 Preview)<br />
  <b>OpenAI</b> (GPT-5, GPT-4.1) · <b>Anthropic</b> (Claude) · <b>Ollama</b> (Llama 3)
</td>
</tr>
<tr>
<td><b>📄 Parsing</b></td>
<td>pypdf (page tracking) · python-docx · BeautifulSoup4</td>
</tr>
<tr>
<td><b>💾 Storage</b></td>
<td>SQLite (embedded at <code>data/rag.db</code>) · ChromaDB (embedded at <code>data/chroma/</code>)</td>
</tr>
<tr>
<td><b>📊 Evaluation</b></td>
<td>LLM-as-judge faithfulness · Context recall · Precision · Arize Phoenix (OTel tracing)</td>
</tr>
</table>

---

## Defense & Research Documentation

For thesis presentation, viva preparation, and technical architecture review, refer to the dedicated documents in `docs/`:

- 📑 [**Thesis Report Draft**](docs/THESIS_REPORT_DRAFT.md) — 6-chapter comprehensive academic draft with IEEE-formatted citations and mathematical proofs.
- 🖼️ [**Master Defense Slides**](docs/DEFENSE_SLIDES.md) — 14-slide defense deck with verbatim speaker notes, slide visuals, and timing guidance.
- 🛡️ [**Examiner Trap Q&A**](docs/MOCK_DEFENSE_QA.md) — Defenses and mathematical answers for the top 7 hardest examiner questions.
- 📐 [**Technical Architecture Specification**](docs/Architecture.md) — End-to-end dataflow, sequence diagrams, and design decisions.
- 🗺️ [**Defense Roadmap**](docs/DEFENSE_ROADMAP.md) — 7-day execution checklist for project delivery.

---

## Features

### 1. Document Ingestion with Page-Number Grounding
- **Drag-and-drop auto-indexing** for PDF, DOCX, TXT, Markdown, HTML, CSV, JSON.
- **Page-Level Chunk Metadata**: PDF pages are individually tracked during parsing and retained across chunking so answers cite specific pages (e.g. `Attention Is All You Need.pdf (P. 3)`).
- **Smart Filtering**: Rejects table-of-contents dots and low-entropy snippets.

### 2. High-Speed Streaming Chat with CoT
- **WebSocket connection** (`/api/chat`) with sub-second token latency.
- **Thinking Process**: Collapsible Chain-of-Thought (CoT) panel showing intermediate reasoning before final answer delivery.
- **Markdown & Code Highlighting**: Syntax-highlighted code blocks, formulas, and formatted tables.

### 3. Multi-Provider Flexibility (Zero Token Bottleneck)
- **Groq LPU Support**: Up to 800+ tokens/second with generous free daily limits using `qwen/qwen3.8-27b` and `openai/gpt-oss-120b`.
- **Google AI Studio Support**: Direct support for `gemini-3.1-flash-lite` and preview models.
- **Local Fallback**: Full compatibility with local Ollama (`llama3`) and local embeddings.

### 4. Anti-Hallucination Refusal Gate
- When the maximum retrieval similarity falls below the threshold (`REFUSAL_SIMILARITY_THRESHOLD=0.25`), the system short-circuits LLM generation and honestly states:
  > *"I don't have enough information to answer that based on the provided documents."*

### 5. Automated Answer Quality Evaluation
- Real-time **Faithfulness** scoring per message using atomic claim decomposition.
- On-demand **Answer Relevancy** and **Context Precision** scoring.
- Offline evaluation suite with golden question datasets and baseline comparison metrics.

---

## Quick Start

### 1. Prerequisites
- **Python 3.12+**
- **Node.js 20+** and **npm**

### 2. Clone and Setup Environment

```bash
git clone https://github.com/mintopubali/ai-research-assistant.git
cd ai-research-assistant

# Create Python virtual environment
python -m venv .venv

# Activate on Windows:
.\.venv\Scripts\activate
# Activate on Linux/macOS:
# source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys in `.env`

Copy or edit `.env` in the root folder:

```ini
# Recommended: Groq Cloud (Free, ultra-fast 800 tok/s, no tight token quota)
GROQ_API_KEY=gsk_your_groq_api_key

# Optional: Google AI Studio Gemini
GEMINI_API_KEY=your_gemini_api_key

# Default Model Selection
DEFAULT_MODEL=qwen/qwen3.8-27b
REASONING_MODEL=qwen/qwen3.8-27b
EVAL_MODEL=qwen/qwen3.8-27b

# Retrieval Strategy (dense | hybrid | reranked | multi_query)
RETRIEVER_STRATEGY=dense
```

### 4. Run Backend & Frontend

**Terminal 1 — Backend API:**
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8001
```

**Terminal 2 — Frontend UI:**
```bash
cd frontend
npm install
npm run dev
```

| Service | URL | Description |
|---|---|---|
| **Frontend UI** | [http://localhost:3000](http://localhost:3000) | Full Chat & Upload UI |
| **Backend API** | [http://localhost:8001](http://localhost:8001) | FastAPI Server |
| **Interactive Docs** | [http://localhost:8001/docs](http://localhost:8001/docs) | Swagger OpenAPI UI |
| **Health Check** | [http://localhost:8001/health](http://localhost:8001/health) | API Status (`{"status":"healthy"}`) |

---

## Configuration Reference

All settings are centralized in `src/config.py`:

| Parameter | Default | Description |
|---|---|---|
| `DEFAULT_MODEL` | `qwen/qwen3.8-27b` | Primary generation model (env: `DEFAULT_MODEL`) |
| `REASONING_MODEL` | `qwen/qwen3.8-27b` | CoT reasoning pass model |
| `EVAL_MODEL` | `qwen/qwen3.8-27b` | Real-time faithfulness evaluation judge |
| `CHUNK_SIZE` | `512` | Characters per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap characters between consecutive chunks |
| `TOP_K_RESULTS` | `5` | Retrieved chunks passed into context prompt |
| `RETRIEVER_STRATEGY` | `dense` | Strategy selector: `dense`, `hybrid`, `reranked`, `multi_query` |
| `REFUSAL_ENABLED` | `false` | Enable/disable refusal gate |
| `REFUSAL_SIMILARITY_THRESHOLD` | `0.25` | Minimum cosine similarity to trigger generation |
| `HYBRID_RRF_K` | `60` | Damping constant for Reciprocal Rank Fusion |
| `SQLITE_PATH` | `data/rag.db` | Embedded chat history database |
| `CHROMA_PATH` | `data/chroma` | Embedded vector database directory |

### Model Provider Auto-Routing

| Prefix | Provider | Key Environment Variable |
|---|---|---|
| `qwen/*`, `groq/*`, `openai/gpt-oss-*` | Groq Cloud | `GROQ_API_KEY` |
| `gemini-*` | Google AI Studio | `GEMINI_API_KEY` |
| `gpt-*`, `o1-*`, `o3-*` | OpenAI | `OPENAI_API_KEY` |
| `claude-*` | Anthropic | `ANTHROPIC_API_KEY` |
| Everything else (`llama3`, etc.) | Ollama Local | None (uses local daemon) |

---

## Testing & Verification

Run the complete test suite (558 tests):

```bash
# Run all unit and integration tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing
```

---

<div align="center">

<sub>Built with FastAPI · React · ChromaDB · Groq · scikit-learn</sub>

</div>