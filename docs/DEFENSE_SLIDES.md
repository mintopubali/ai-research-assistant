---
marp: true
theme: default
paginate: true
header: "Verifiable & Cost-Aware RAG | M.Engg. Project Defence | Mahadur Jaman Minto (CE-180628)"
footer: "Department of CSE, Mawlana Bhashani Science and Technology University (MBSTU)"
---

# 🎯 Master of Engineering (M.Engg.) Project Defence

**Project Title**: Verifiable and Cost-Aware Retrieval-Augmented Generation for Scientific Literature  
**Subtitle**: An Enterprise Architecture with Hybrid Retrieval, Physical Provenance, and Deterministic Gating  
**Candidate / Developer**: **Mahadur Jaman Minto** | Student ID: `CE-180628`  
**Project Supervisor**: **Dr. Mostofa Kamal Nasir**, Professor, Department of Computer Science and Engineering  
**Degree Program**: **Master of Engineering (M.Engg.) in Computer Science and Engineering**  
**Institution**: Mawlana Bhashani Science and Technology University (MBSTU), Santosh, Tangail-1902  
**Presentation Duration**: 15–20 minutes (15 Slides + Appendix)  

---

## Slide 1: Title & Project Overview

* **Project Header**: Verifiable & Cost-Aware RAG for Scientific Literature
* **Engineering Highlights**: `Hexagonal Architecture` | `Physical Page Provenance (p. X)` | `RRF k=60 Hybrid Search` | `0-Token Refusal Gate` | `558 Automated Tests`
* **Academic Credentials**:
  - **Presented by**: **Mahadur Jaman Minto** (ID: `CE-180628`)
  - **Supervised by**: **Dr. Mostofa Kamal Nasir**, Professor, Department of CSE, MBSTU
  - **Degree**: Master of Engineering (M.Engg.) in Computer Science and Engineering
* **Core Project Scope**:
  - Bridging the trust chasm between Large Language Models and verifiable academic literature.
  - Solving the three major engineering bottlenecks of RAG: citation inaccuracy, vocabulary mismatch, and unbounded inference costs.
  - Fully functional, production-ready full-stack software system: `FastAPI` (Backend) + `React 19` (Frontend) + `ChromaDB` (Vector Store) + `SQLite` (Chat State) + Multi-Provider LLMs (`Gemini 2.5 Flash`, `Groq`, `Ollama`).
* **Speaker Notes**:
  > "Respected supervisor Dr. Mostofa Kamal Nasir, honorable examination committee members, and faculty members: Assalamu Alaikum and good morning. I am Mahadur Jaman Minto, ID CE-180628. Today, I am presenting my Master of Engineering (M.Engg.) project on *'Verifiable and Cost-Aware Retrieval-Augmented Generation for Scientific Literature'*. In this project, we designed and built an enterprise-grade software architecture that eliminates hallucinations, guarantees exact physical page-level citations from PDFs, and controls cloud inference costs using deterministic gating and real-time telemetry."
* **Examiner Q&A**:
  - *Q: "Why build a custom system from scratch instead of wrapping LangChain or LlamaIndex?"*
  - *A: "LangChain and LlamaIndex are rapid prototyping toolkits. In production engineering, they suffer from leaky abstractions, drop physical page provenance during chunking, and lack deterministic refusal gates. Our system is built on Ports and Adapters (Hexagonal Architecture) governed by 10 formal ADRs, achieving modularity, 0-token CI/CD testing, and production maintainability."*

---

## Slide 2: The Engineering Problem: Three Flaws of Naive RAG

* **Header**: Why Naive RAG Architectures Fail in Production
* **Real-World System Vulnerabilities**:
  1. **Lost Physical Provenance**: Standard PDF parsers flatten pages into continuous text. Chunks receive arbitrary sequential IDs (`chunk_12`), permanently losing the source PDF page number. As a result, researchers cannot audit or verify claims against the physical document.
  2. **Vocabulary Mismatch**: Dense bi-encoders project queries and chunks into semantic vector spaces. However, they frequently smooth over critical technical acronyms and mathematical notation (e.g., "LoRA", "DPR", "$\sqrt{d_k}$"), returning irrelevant semantic neighbors.
  3. **Unbounded Hallucination & Cloud Cost**: Naive pipelines unconditionally invoke the LLM on every query, even when retrieved context is irrelevant or empty. This guarantees fabricated answers and burns billable API quotas.
* **Architecture Comparison**:
```mermaid
graph LR
    subgraph Naive["Naive RAG (Vulnerable)"]
        N1[Flattened PDF] --> N2[Unbounded Chunks]
        N2 --> N3[Dense-Only Search]
        N3 --> N4[Unconditional LLM Call]
        N4 --> N5[Hallucination & Lost Pages]
    end
    subgraph Ours["Our Enterprise Architecture (Verifiable)"]
        O1[Page-Bounded PDF] --> O2[Page-Tagged Chunks]
        O2 --> O3[RRF Hybrid + Cross-Encoder]
        O3 --> O4{Score >= 0.35?}
        O4 -- No --> O5[0-Token Refusal]
        O4 -- Yes --> O6[Two-Pass Stream + Page Badges]
    end
```
* **Speaker Notes**:
  > "When transitioning RAG from basic proof-of-concept scripts to production engineering over academic literature, three fatal flaws emerge. First, if a researcher cannot verify the exact page of a cited claim, the system cannot be trusted. Second, dense vector embeddings alone fail on technical acronyms like LoRA or mathematical terms. Third, forcing an LLM to answer unanswerable queries guarantees hallucination and burns tokens needlessly."

---

## Slide 3: Project Objectives & System Specifications

* **Header**: Engineering Requirements & Core Deliverables
* **System Design Goals**:
  - **Req 1 (Physical Provenance)**: Parse and preserve exact physical PDF page numbers from ingestion to UI citation badges (`(p. 3)`).
  - **Req 2 (Hybrid Retrieval Seam)**: Implement a composable retrieval seam combining sparse lexical search (`BM25`) and dense vector search (`all-MiniLM-L6-v2`) via Reciprocal Rank Fusion ($k=60$).
  - **Req 3 (Deterministic Refusal)**: Intercept unanswerable and out-of-corpus queries with a similarity threshold gate ($\tau = 0.35$), consuming **0 LLM API tokens**.
  - **Req 4 (Streaming UX & Telemetry)**: Implement a two-pass WebSocket protocol providing visible Chain-of-Thought (CoT) reasoning and real-time millisecond/token/cost telemetry.
  - **Req 5 (Zero-Token Testability & CI)**: Decouple external API dependencies with injected client factories, enabling full offline test coverage across 558 automated test cases.
* **Speaker Notes**:
  > "To resolve these enterprise challenges, our project defined five clear engineering deliverables covering provenance tracking, hybrid retrieval, deterministic cost gating, visible streaming UX, and test automation. Every specification was implemented as a production software module backed by automated unit and integration tests."

---

## Slide 4: End-to-End System Pipeline (7 Stages)

* **Header**: End-to-End Execution Flow: From Bytes to Grounded UI
* **Complete System Flowchart**:
```mermaid
flowchart TD
    classDef input fill:#f2ede4,stroke:#c4baa9,stroke-width:1.5px,color:#2c2c2c,rx:8,ry:8;
    classDef greenBox fill:#e4f4ed,stroke:#78c2a4,stroke-width:1.5px,color:#1b5e3d,rx:8,ry:8;
    classDef purpleBox fill:#eeeafc,stroke:#9d8cf2,stroke-width:1.5px,color:#2f1c6a,rx:8,ry:8;
    classDef gateBox fill:#ffffff,stroke:#5c42e2,stroke-width:2px,color:#2f1c6a,rx:8,ry:8;
    classDef refuseBox fill:#f4f1ea,stroke:#b8b0a2,stroke-width:1.5px,stroke-dasharray: 4 4,color:#3a352d,rx:8,ry:8;

    USER["<b>User document</b>"]:::input

    STEP1["<b>1. Ingestion and page tracking</b><br/><small>PyPDFParser, meta['pages']</small>"]:::greenBox
    STEP2["<b>2. Page-bounded chunking</b><br/><small>512 chars, 64 overlap, in-page</small>"]:::greenBox

    subgraph DUAL["3. Dual persistence"]
        direction LR
        CHROMA["<b>ChromaVectorStore</b><br/><small>page_number, doc_id</small>"]:::greenBox
        SQLITE["<b>SQLite / SQLModel</b><br/><small>SHA-256 idempotency</small>"]:::greenBox
    end
    style DUAL fill:none,stroke:#e0e0e0,stroke-width:1.2px,stroke-dasharray: 4 4

    subgraph RETR["4. Composable retrieval seam"]
        direction LR
        subgraph INPUTS[" "]
            DENSE["<b>Dense</b><br/><small>MiniLM cosine</small>"]:::purpleBox
            SPARSE["<b>Sparse</b><br/><small>BM25, thread-safe store</small>"]:::purpleBox
        end
        style INPUTS fill:none,stroke:none
        HYBRID["<b>Hybrid RRF</b><br/><small>k = 60</small>"]:::purpleBox
        RERANK["<b>Neural rerank</b><br/><small>Cross-encoder, N=20</small>"]:::purpleBox

        DENSE --> HYBRID
        SPARSE --> HYBRID
        HYBRID --> RERANK
    end
    style RETR fill:none,stroke:#e0e0e0,stroke-width:1.2px,stroke-dasharray: 4 4

    GATE["<b>5. Deterministic refusal gate</b><br/><small>Pass if max score ≥ 0.35</small>"]:::gateBox
    REFUSE["<b>Refuse</b><br/><small>0 LLM tokens</small>"]:::refuseBox

    subgraph GEN["6. Two-pass generation and telemetry"]
        direction LR
        PASS1["<b>Pass 1: reasoning</b><br/><small>Visible chain-of-thought</small>"]:::purpleBox
        PASS2["<b>Pass 2: grounded answer</b><br/><small>Markdown token stream</small>"]:::purpleBox
        PASS1 --> PASS2
    end
    style GEN fill:none,stroke:#e0e0e0,stroke-width:1.2px,stroke-dasharray: 4 4

    UI["<b>7. UI grounding</b><br/><small>SourcesPanel, p. 4 badge</small>"]:::input

    USER --> STEP1
    STEP1 --> STEP2
    STEP2 --> DUAL
    DUAL --> RETR
    RETR --> GATE
    GATE -- "Score < 0.35" --> REFUSE
    GATE -- "Score ≥ 0.35" --> GEN
    GEN --> UI
```
* **Speaker Notes**:
  > "This diagram presents the entire end-to-end dataflow of our software architecture across seven stages. From document upload, text normalisation, and page-bounded chunking, through dual persistence in ChromaDB and SQLite, to composable hybrid retrieval, neural reranking, deterministic refusal gating, two-pass generation, and interactive UI grounding."

---

## Slide 5: System Architecture: Hexagonal Seams

* **Header**: Hexagonal Architecture (Ports and Adapters Pattern)
* **System Component Boundaries**:
```mermaid
graph TD
    subgraph Inbound["Inbound Ports (Driving Adapters)"]
        REST["FastAPI REST API<br/>/api/upload, /api/query"]
        WS["WebSocket Endpoint<br/>/api/chat (Two-Pass CoT)"]
    end

    subgraph Core["Core Application & Domain (Business Logic)"]
        Facade["RAGBackend Facade"]
        Domain["Domain Entities (Immutable)<br/>Document, Chunk, SearchResult, StageTelemetry"]
        QEngine["QueryEngine (ask / ask_stream)"]
    end

    subgraph Outbound["Outbound Ports (Driven Adapters)"]
        VS["Vector Store Adapter<br/>(ChromaVectorStore - Cosine)"]
        DB["Relational Persistence<br/>(SQLite / SQLModel)"]
        Retr["Retrieval Seam<br/>(Dense / BM25 / RRF / Reranker)"]
        LLMs["Multi-Provider LLM Seam<br/>(Gemini 2.5 / Groq / OpenAI / Ollama)"]
    end

    REST --> Facade
    WS --> Facade
    Facade --> QEngine
    QEngine --> Domain
    QEngine --> Retr
    QEngine --> LLMs
    Facade --> VS
    Facade --> DB
```
* **Key Architectural Decisions**:
  - **Clean Boundary (`src/domain.py`)**: Vendor-free domain entities (`Document`, `Chunk`, `SearchResult`).
  - **RAGBackend Facade**: Coordinates ingestion, retrieval, and chat history persistence without leaking library internals to API routes.
  - **Governance via 10 ADRs**: Formal Architectural Decision Records enforcing single-responsibility and dependency inversion.
* **Speaker Notes**:
  > "We adopted Hexagonal Architecture, also known as Ports and Adapters. The core business logic depends strictly on abstract domain protocols, never on third-party libraries. ChromaDB, SQLite, rerankers, and LLM providers are pluggable adapters. This architectural decoupling allows our entire 558-test suite to execute offline in seconds with zero API tokens consumed."

---

## Slide 6: Ingestion Pipeline & Physical Page Tracking

* **Header**: Guaranteeing Page Provenance from File Upload to UI
* **Ingestion Dataflow Pipeline**:
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Upload as /api/upload
    participant Parser as PyPDFParser
    participant Chunker as TextChunker
    participant Chroma as ChromaDB
    participant DB as SQLite
    participant UI as React 19 Frontend

    User->>Upload: Upload Paper PDF
    Upload->>Parser: parse_pdf()
    Note over Parser: Page-by-page extraction & normalise_pdf_text()
    Parser-->>Chunker: text + meta["pages"]
    Note over Chunker: Within-page splitting (512 chars, 64 overlap)
    Chunker-->>Chroma: upsert() scalar metadata (doc_id, chunk_index, page_number)
    Chunker-->>DB: session.merge(DocumentRecord with SHA-256)
    Note over UI: Query triggers citation retrieval
    Chroma-->>UI: SourceInfo with page_number -> Render "(p. 4)" Badge
```
* **Engineering Implementation**:
  1. `PyPDFParser`: Reads PDFs page-by-page, normalizing hard layout line breaks while recording `meta["pages"] = [{"page_number": idx + 1, "text": page_norm}]`.
  2. `TextChunker`: Enforces recursive chunking *within* each page boundary (512 characters, 64 character overlap). Chunks never straddle physical pages.
  3. `ChromaDB Constraint Compliance`: Strips complex nested structures before upsert while preserving the scalar `page_number` attribute.
  4. `UI Grounding`: The REST and WebSocket APIs emit `page_number` inside `SourceInfo`, rendering verifiable `(p. 4)` badges in the React client.
* **Speaker Notes**:
  > "Our ingestion pipeline solves Req 1 by enforcing physical page boundaries. While typical splitters flatten entire documents, our loader extracts text per page, and our chunker operates strictly within page boundaries. The scalar page number is preserved across storage and emitted to the UI, allowing instant manual verification against the original PDF."

---

## Slide 7: Hybrid Retrieval: Fusing Dense & Sparse with RRF

* **Header**: Overcoming Vocabulary Mismatch with RRF ($k=60$)
* **The Mathematical Formulation & Engineering Justification**:
  - **The Flaw of Linear Score Combination**:
    $$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Score}_{\text{dense}} + (1 - \alpha) \cdot \text{Score}_{\text{sparse}} \quad \text{[Fragile & Uncalibrated]}$$
    Cosine similarity $[0.2, 0.65]$ and BM25 scores $[0, \infty)$ have incompatible scales; corpus additions alter IDF, breaking tuned weights.
  - **Reciprocal Rank Fusion (RRF $k=60$)**:
    $$\text{RRF\_Score}(d \in D) = \sum_{m \in \{\text{dense}, \text{sparse}\}} \frac{1}{60 + r_m(d)}$$
  - Operates purely on ordinal ranks $r_m(d)$, making the fusion scale-invariant and capturing exact acronyms (LoRA, BART) alongside semantic matches.
* **Corpus Sync & Thread Safety**:
  - In-memory BM25 index tracks ChromaDB's monotonic `_revision` counter.
  - Re-indexes only when writes or deletions occur, guarded by `threading.RLock`.
* **Speaker Notes**:
  > "Combining dense and lexical search is essential for scientific papers. However, linear score combination is fundamentally uncalibrated because cosine distances and BM25 scores live in incompatible distributions. We employ Reciprocal Rank Fusion with constant k=60. As Cormack et al. proved, RRF operates strictly on ordinal ranks, making it completely invariant to score scaling."

---

## Slide 8: Neural Reranking: Cross-Encoder Attention

* **Header**: Precision Optimization with `ms-marco-MiniLM-L-6-v2`
* **Bi-Encoder vs. Cross-Encoder Architecture**:
```mermaid
graph TD
    subgraph BiEncoder["Bi-Encoder (Stage 1: Fast Candidate Retrieval)"]
        Q1[Query q] --> E1[Encoder] --> V1[Dense Vector u]
        P1[Passage p] --> E2[Encoder] --> V2[Dense Vector v]
        V1 & V2 --> DOT["Dot Product / Cosine (Top 20 in <10ms)"]
    end

    subgraph CrossEncoder["Cross-Encoder (Stage 2: Full Deep Attention)"]
        QP["[CLS] + Query + [SEP] + Passage + [SEP]"] --> BERT["Full 6-Layer Transformer Cross-Attention"]
        BERT --> SC["Direct Relevance Logit / Sigmoid Score"]
    end
```
* **Two-Stage Retrieve-and-Rerank Protocol**:
  - **Stage 1 (Bi-Encoder Candidate Generation)**: Fast approximate nearest neighbors (HNSW) over-fetches top $N=20$ candidates in $<10\text{ms}$.
  - **Stage 2 (Cross-Encoder Neural Reranking)**: Concatenates Query and Passage into full bidirectional transformer attention:
    $$\text{Score}_{\text{CE}}(q, p) = \text{Softmax}(\text{Linear}(\text{BERT}([CLS] \circ q \circ [SEP] \circ p)))$$
  - Directly resolves bi-encoder rank inversions, ensuring the causally relevant passage occupies rank 1.
* **Speaker Notes**:
  > "Bi-encoders process queries and documents independently for fast retrieval, but cannot model fine-grained token-level cross-attention. In our second stage, the cross-encoder feeds the concatenated query and chunk through full transformer layers, allowing every word in the query to attend to every word in the context."

---

## Slide 9: Deterministic Refusal Gating (Phase 2 Lever 2g)

* **Header**: Preventing Hallucinations on Unanswerable Queries
* **Refusal Decision Flowchart**:
```mermaid
flowchart TD
    Q[User Question] --> RET[Retrieve Candidates C]
    RET --> CHECK{Candidates Empty<br/>OR max score < 0.35?}
    CHECK -- Yes --> REFUSE["Short-Circuit Immediately<br/>Return Refusal Text<br/><b>Cost: 0 LLM Tokens</b>"]
    CHECK -- No --> PASS1["Pass 1: Stream CoT Reasoning"]
    PASS1 --> PASS2["Pass 2: Stream Grounded Answer"]
```
* **The Deterministic Refusal Rule**:
  $$\text{Decision} = \begin{cases} \text{Refuse immediately ("I don't have enough information..."),} & \text{if } \max_{c \in C} \text{score}(c) < 0.35 \\ \text{Proceed to Two-Pass Generation,} & \text{otherwise} \end{cases}$$
* **Engineering Hardening**:
  - Evaluates the **maximum score across candidates** rather than position 0, preventing false refusals in asymmetric hybrid rankings where position 0 is a sparse-only hit.
  - **Zero LLM Tokens Billed**: Short-circuits the pipeline before calling generative APIs, eliminating hallucinations and costs on unanswerable questions.
  - Empirically calibrated: Achieves **90.0% Refusal Correctness** on the test benchmark.
* **Speaker Notes**:
  > "Standard RAG systems always call the LLM, hallucinating answers when papers do not contain the answer. Our Deterministic Refusal Gate inspects the candidate set before LLM invocation. If the maximum similarity falls below 0.35, the system immediately returns a refusal. This costs 0 API tokens and achieves 90% refusal correctness on out-of-domain questions."

---

## Slide 10: Multi-Provider LLM Seam & Fallback Handlers

* **Header**: Provider Independence via Injected Client Factories
* **Pluggable Provider Ecosystem**:
  - **Google AI Studio**: Gemini 2.5 Flash / Lite via OpenAI-compatible REST endpoint.
  - **Groq Cloud LPU**: Ultra-fast inference ($>500\text{ tok/s}$) for real-time querying.
  - **OpenAI & Anthropic**: GPT-4o, Claude 3.5 Sonnet / Haiku.
  - **Local Air-Gapped**: Ollama (`llama3`, `mistral`) for 100% offline environments.
  - **Graceful Degradation (`DummyAdapter`)**: Automatically catches API outages or missing credentials, returning retrieved citations without crashing.
* **Zero-Token Testability (ADR 0002)**:
  - All external clients are injected via `Callable[[], object]` zero-argument factories.
  - Test suites replace network calls with deterministic in-memory stubs.
* **Speaker Notes**:
  > "Our LLMHandler supports transparent routing across Google AI Studio, Groq, OpenAI, Anthropic, and local Ollama. Under ADR 0002, SDK clients are injected via zero-argument factories. If an external API is unavailable or rate-limited, the system falls back gracefully to DummyAdapter, presenting the user with verified sources rather than an unhandled error."

---

## Slide 11: Two-Pass Streaming UX: Visible Chain-of-Thought

* **Header**: Real-Time Reasoning Streaming over WebSockets
* **Two-Step Generation Protocol**:
```mermaid
sequenceDiagram
    autonumber
    participant UI as React 19 Frontend
    participant WS as WebSocket /api/chat
    participant FastLLM as Reasoning LLM (Gemini / Nano)
    participant AnswerLLM as Primary LLM (Gemini Flash / GPT-4o)

    UI->>WS: {"query": "Explain Scaled Dot-Product", "top_k": 5}
    WS-->>UI: {"type": "status", "content": "Searching indexed documents..."}
    WS-->>UI: {"type": "status", "content": "Retrieved 5 chunks across 1 paper"}
    Note over WS,FastLLM: Pass 1: Reasoning Analysis
    FastLLM-->>WS: Stream Reasoning Tokens
    WS-->>UI: {"type": "reasoning", "content": "Analyzing key dimension d_k..."}
    Note over WS,AnswerLLM: Pass 2: Factual Synthesis
    AnswerLLM-->>WS: Stream Answer Tokens
    WS-->>UI: {"type": "token", "content": "The dot products are scaled by..."}
    WS-->>UI: {"type": "done", "sources": [{"page_number": 4, ...}]}
    WS-->>UI: {"type": "telemetry", "retrieve_ms": 12, "generate_ms": 780, "cost_usd": 0.0002}
```
* **User Impact**: Eliminates perceived latency; users observe analytical thought progression before reading the synthesized result.
* **Speaker Notes**:
  > "Over WebSockets, we implement a two-pass generation protocol. Pass 1 streams the model's intermediate Chain-of-Thought reasoning into a collapsible UI panel. Pass 2 streams the grounded final answer. This eliminates perceived latency and allows the researcher to audit the AI's logical deductions in real time."

---

## Slide 12: Real-Time Telemetry & Pricing Ledger

* **Header**: Transparent Latency & Cost Accounting
* **Audited Telemetry Payload (`StageTelemetry`)**:
  - `retrieve_ms`: Exact millisecond retrieval time.
  - `generate_ms`: Generation latency.
  - `prompt_tokens` & `completion_tokens`: Provider-audited token tallies.
  - `cost_usd`: Calculated dynamically via internal pricing table.
* **UI Integration**:
  - Rendered in real-time message footer:  
    `⏱️ 842ms (ret: 18ms, gen: 824ms) | 🪙 1,240 tokens | 💵 $0.00028`
* **Institutional Value**: Allows engineering teams to audit per-query inference costs and forecast production cloud budgets.
* **Speaker Notes**:
  > "To satisfy Req 4, every query generates an immutable StageTelemetry record. We measure retrieval time, generation time, prompt tokens, completion tokens, and real-time USD cost. This provides institutional transparency and allows research labs to forecast deployment expenses."

---

## Slide 13: System Verification & Benchmark Results

* **Header**: Empirical Validation on `ML Papers v1` Benchmark
* **Dual-Evaluation Strategy**:
  1. **Macro Verification (SQuAD v2 - 200 Questions)**: Validated baseline reading comprehension and general-domain refusal.
  2. **Micro Academic Ground-Truth Benchmark (`ML Papers v1` - 460 Chunks, 10 Golden Questions)**: Byte-verified corpus (Attention, RAG, LoRA) measuring exact page provenance, mathematical formulas, and unanswerable refusal.

* **System Benchmark Metrics**:

| Metric | Dimension | Score | 95% Bootstrap Confidence Interval |
| :--- | :--- | :---: | :---: |
| **Refusal Correctness** | Hallucination Safety | **0.9000** | [0.7000, 1.0000] |
| **Judge Faithfulness** | Groundedness / Factual Truth | **1.0000** | [1.0000, 1.0000] |
| **Recall@5** | Document Coverage | **0.3889** | [0.1111, 0.6958] |
| **MRR@5** | Rank Precision | **0.3333** | [0.1375, 0.6403] |
| **Answer Correctness** | Response Quality | **0.5260** | [0.5060, 0.5416] |
| **Automated Test Suite** | Code & Architectural Integrity | **558 / 558 Passed** | **0 API Tokens Consumed** |

* **Speaker Notes**:
  > "We evaluated the architecture using a dual-benchmark approach. On ML Papers v1, the empirical results demonstrate 90% refusal correctness on unanswerable questions and a perfect 1.0000 faithfulness score from an independent LLM judge, confirming zero hallucinated claims. The non-parametric bootstrap confidence intervals reflect honest small-sample statistics over human-annotated academic gold standards."

---

## Slide 14: Live Demonstration Walkthrough

* **Header**: Interactive System Demonstration Protocol
* **Live Demonstration Protocol**:
  1. **Upload & Ingestion**:
     - Uploading `attention_is_all_you_need.pdf` $\rightarrow$ Page-by-page parsing $\rightarrow$ SHA-256 deduplication.
  2. **Answerable Query (Verifiable Provenance)**:
     - Query: *"Why does scaled dot-product attention divide by square root of d_k?"*
     - Live CoT reasoning stream $\rightarrow$ Synthesized response $\rightarrow$ Clickable `(p. 4)` page citation badge.
  3. **Unanswerable Query (Deterministic Safety)**:
     - Query: *"What is the optimal learning rate for FlashAttention-2?"*
     - Refusal gate short-circuiting $\rightarrow$ Immediate refusal with **0 LLM tokens billed**.
* **Speaker Notes**:
  > "I will now demonstrate the live system. First, we ingest the Vaswani et al. paper. Next, we submit an answerable question on scaled dot-product attention. Notice the visible reasoning stream and the page 4 citation badge. Finally, when asking an out-of-corpus question regarding FlashAttention-2, the refusal gate intercepts the request immediately with zero tokens consumed."

---

## Slide 15: Conclusion & Future Engineering Roadmap

* **Header**: Project Summary & Future Directions
* **Core Engineering Takeaways**:
  - Demonstrated that disciplined software architecture (Hexagonal seams, RRF, deterministic gating) solves production vulnerabilities in academic RAG.
  - Guaranteed exact physical page citation and 90% hallucination prevention.
  - Delivered a production-ready system backed by 558 passing tests and multi-provider agility.
* **Future Work**:
  - **GraphRAG**: Entity-relation knowledge graphs across multi-paper citation networks.
  - **Multimodal Layout Models**: Integrating vision embeddings (ColPali) for embedded scientific figures, schematics, and tables.
* **Closing & Q&A**:
  > "In conclusion, verifiable AI over scientific literature requires disciplined engineering boundaries rather than ad-hoc scripts. I extend my sincere gratitude to my supervisor, Dr. Mostofa Kamal Nasir, and to the respected committee members. Thank you. I am now ready to answer your questions."
