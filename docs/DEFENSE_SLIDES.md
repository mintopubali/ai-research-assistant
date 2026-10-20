# 🎯 Final Master's Defence Slide Deck

**Title**: Verifiable and Cost-Aware Retrieval-Augmented Generation for Scientific Literature  
**Subtitle**: An Enterprise Architecture with Hybrid Retrieval, Physical Provenance, and Deterministic Gating  
**Author / Presenter**: **Mahadur Jaman Minto** | Student ID: `CE-180628`  
**Supervisor**: **Dr. Mostofa Kamal Nasir**, Professor, Department of Computer Science and Engineering  
**Institution**: Mawlana Bhashani Science and Technology University (MBSTU), Santosh, Tangail-1902  
**Target Duration**: 15–20 minutes (14 Slides)  

---

## Slide 1: Title & Research Overview
* **Header**: Verifiable & Cost-Aware RAG for Scientific Literature
* **Visual Asset**: University crest / MBSTU badge, clean academic card with system badges: `Hexagonal Architecture`, `Physical Provenance`, `RRF k=60`, `0-Token CI`.
* **Academic Credentials**:
  - **Presented by**: **Mahadur Jaman Minto** (ID: `CE-180628`)
  - **Supervised by**: **Dr. Mostofa Kamal Nasir**, Professor, Department of CSE, MBSTU
  - **Degree Program**: Master / Bachelor of Science in Computer Science and Engineering
* **Key Bullet Points**:
  - Bridging the trust chasm between Large Language Models and verifiable scientific synthesis.
  - Core Focus: Eliminating hallucinations, enforcing exact page-level provenance, and bounding inference expenditure.
  - Implemented System: Full-stack RAG Assistant (`FastAPI` + `React 19` + `ChromaDB` + `SQLite` + `Gemini 2.5 Flash / Groq / Ollama`).
* **Speaker Notes**:
  > "Respected supervisor Dr. Mostofa Kamal Nasir, honorable members of the defense committee, and distinguished faculty members: Assalamu Alaikum and good morning. I am Mahadur Jaman Minto, ID CE-180628. Today, I am privileged to present my defense on *'Verifiable and Cost-Aware Retrieval-Augmented Generation for Scientific Literature'*. In this research, we address the critical vulnerabilities of standard RAG systems—hallucinations, lost citation page numbers, and unpredictable inference costs—by introducing an enterprise-grade, verifiable architecture."
* **Examiner Q&A**:
  - *Q: "Why build a custom system instead of using LangChain or LlamaIndex?"*
  - *A: "LangChain and LlamaIndex are high-level prototyping libraries. They lack strict architectural boundaries, drop physical page provenance during chunking, and lack deterministic refusal gates. Our system uses Hexagonal Architecture with 10 formal ADRs, guaranteeing zero-token testability and verifiable page-level grounding."*

---

## Slide 2: The Problem: Three Fatal Flaws of Naive RAG
* **Header**: Why Naive RAG Fails in Scientific Synthesis
* **Visual Asset**: 3-column comparative diagram contrasting Naive RAG failures against our Enterprise Solution.
* **Three Critical Vulnerabilities**:
  1. **Lost Physical Provenance**: Conventional PDF parsers concatenate document pages into a continuous text stream. Chunks retain only arbitrary chunk indices, destroying page numbers and rendering citations unverifiable in peer review.
  2. **Vocabulary Mismatch**: Dense bi-encoders smooth over domain-specific acronyms and mathematical symbols (e.g., "LoRA", "DPR", "$\sqrt{d_k}$"), returning irrelevant semantic neighbors.
  3. **Unbounded Hallucination & Cost**: Naive pipelines always prompt the LLM, even when retrieved context is irrelevant. This guarantees fabricated facts and wastes API budget.
* **Speaker Notes**:
  > "When transitioning RAG from toy demos to academic literature, three fatal flaws emerge. First, if a researcher cannot verify the exact page of a cited claim, the system cannot be trusted. Second, dense vector embeddings alone fail on technical acronyms like LoRA or mathematical terms. Third, forcing an LLM to answer unanswerable queries guarantees hallucination and burns tokens needlessly."

---

## Slide 3: Research Questions & Core Contributions
* **Header**: Research Objectives & Engineering Contributions
* **Visual Asset**: 4-part research matrix linking Research Questions (RQ1–RQ4) to concrete software artifacts.
* **Core Research Matrix**:
  - **RQ1 (Provenance)**: Guaranteed page-level provenance via recursive page-bounded splitting (`(p. 3)` UI badge).
  - **RQ2 (Hybridity)**: Composable retrieval combining dense embeddings (`all-MiniLM-L6-v2`) and sparse lexical search (`BM25`) via Reciprocal Rank Fusion ($k=60$).
  - **RQ3 (Safety)**: Deterministic Refusal Gating ($\tau = 0.35$) inspecting $\max(\text{score})$ across candidates to intercept unanswerable queries with 0 LLM tokens.
  - **RQ4 (Observability)**: Two-pass WebSocket Chain-of-Thought (CoT) streaming with real-time per-query telemetry.
  - **Artifact**: `ML Papers v1` benchmark dataset (460 chunks, 10 labeled golden questions, SHA-256 byte verified).
* **Speaker Notes**:
  > "To resolve these challenges, we formulated four core research questions covering document provenance, hybrid rank fusion, deterministic safety gating, and cost observability. Our contributions are not speculative—each research question is resolved through production-hardened software modules backed by 558 automated tests."

---

## Slide 4: System Architecture: Hexagonal Seams
* **Header**: Hexagonal Architecture (Ports and Adapters)
* **Visual Asset**: Clean Hexagonal Architecture diagram showing Inbound Adapters, Core Domain Facade, and Outbound Adapters.
* **Architectural Organization**:
  - **Core Domain (`src/domain.py`)**: Immutable, vendor-free types (`Document`, `Chunk`, `SearchResult`, `StageTelemetry`).
  - **Inbound Ports**: FastAPI REST Routes (`/api/upload`, `/api/query`) + WebSocket Streaming (`/api/chat`).
  - **Orchestration Facade (`RAGBackend`)**: Coordinates ingestion, retrieval, conversation persistence, and evaluation without leaking vendor details.
  - **Outbound Ports**: Pluggable storage (`ChromaVectorStore`, `SQLite/SQLModel`) and Multi-Provider LLMs.
  - **Governance**: 10 formal Architectural Decision Records (ADRs) maintaining structural boundaries.
* **Speaker Notes**:
  > "We adopted Hexagonal Architecture, also known as Ports and Adapters. The core business logic depends solely on abstract protocols, never on vendor libraries. ChromaDB, SQLite, rerankers, and LLM providers are pluggable adapters. This architectural decoupling allows our entire 558-test suite to execute offline in seconds with zero API tokens consumed."

---

## Slide 5: Ingestion Pipeline & Physical Page Tracking
* **Header**: Guaranteeing Page Provenance from Bytes to UI
* **Visual Asset**: Ingestion dataflow diagram showing PDF page extraction, page-bounded chunking, and ChromaDB metadata isolation.
* **Engineering Pipeline**:
  1. `PyPDFParser`: Extracts text page-by-page, recording `meta["pages"] = [{"page_number": idx + 1, "text": page_text}]`.
  2. `TextChunker`: Enforces chunking *within* individual pages (512 chars, 64 overlap). No chunk crosses a physical page boundary.
  3. `ChromaDB Constraint Compliance`: Strips complex nested structures before vector upsert while preserving the scalar `page_number` attribute.
  4. `UI Grounding`: REST and WebSocket APIs emit `page_number` inside `SourceInfo`, rendering verifiable `(p. 3)` badges in the React client.
* **Speaker Notes**:
  > "Our ingestion pipeline solves RQ1 by enforcing physical page boundaries. While typical splitters flatten entire documents, our loader extracts text per page, and our chunker operates strictly within page boundaries. The scalar page number is preserved across storage and emitted to the UI, allowing instant manual verification against the original PDF."
* **Examiner Q&A**:
  - *Q: "What happens to sentences that cross chunk boundaries?"*
  - *A: "We use a 64-character word-boundary-safe sliding overlap. Sentences split at chunk boundaries retain semantic continuity in adjacent chunks, while never crossing physical page limits."*

---

## Slide 6: Hybrid Retrieval: Fusing Dense & Sparse with RRF
* **Header**: Overcoming Vocabulary Mismatch with RRF ($k=60$)
* **Visual Asset**: Mathematical formulation box and comparison curve between linear combination vs. ordinal rank fusion.
* **The Math & Engineering**:
  - **The Flaw of Linear Score Combination**:
    $$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Score}_{\text{dense}} + (1 - \alpha) \cdot \text{Score}_{\text{sparse}} \quad \text{[Fragile & Uncalibrated]}$$
    Cosine similarity $[0.2, 0.65]$ and BM25 scores $[0, \infty)$ have incompatible scales; IDF shifts break tuned weights.
  - **Reciprocal Rank Fusion (RRF $k=60$)**:
    $$\text{RRF\_Score}(d \in D) = \sum_{m \in \{\text{dense}, \text{sparse}\}} \frac{1}{60 + r_m(d)}$$
  - Operates purely on ordinal ranks $r_m(d)$, guaranteeing rank-scale invariance and capturing exact acronyms (LoRA, BART) alongside semantic matches.
* **Speaker Notes**:
  > "Combining dense and lexical search is essential for scientific papers. However, linear score combination is fundamentally uncalibrated because cosine distances and BM25 scores live in incompatible distributions. We employ Reciprocal Rank Fusion with constant k=60. As Cormack et al. proved, RRF operates strictly on ordinal ranks, making it completely invariant to score scaling."

---

## Slide 7: Neural Reranking: Cross-Encoder Attention
* **Header**: Precision Optimization with `ms-marco-MiniLM-L-6-v2`
* **Visual Asset**: Bi-Encoder independent embeddings vs. Cross-Encoder full query-passage cross-attention diagram.
* **Two-Stage Retrieve-and-Rerank**:
  - **Stage 1 (Bi-Encoder Candidate Generation)**: Fast approximate nearest neighbors (HNSW) over-fetches top $2 \times k$ candidates ($N=20$) in $<10\text{ms}$.
  - **Stage 2 (Cross-Encoder Neural Reranking)**: Concatenates Query and Passage into full bidirectional transformer attention:
    $$\text{Score}_{\text{CE}}(q, p) = \text{Softmax}(\text{Linear}(\text{BERT}([CLS] \circ q \circ [SEP] \circ p)))$$
  - Directly resolves bi-encoder rank inversions, ensuring the causally relevant passage occupies rank 1.
* **Speaker Notes**:
  > "Bi-encoders process queries and documents independently for fast retrieval, but cannot model fine-grained token-level cross-attention. In our second stage, the cross-encoder feeds the concatenated query and chunk through full transformer layers, allowing every word in the query to attend to every word in the context."

---

## Slide 8: Deterministic Refusal Gating (Phase 2 Lever 2g)
* **Header**: Preventing Hallucinations on Unanswerable Queries
* **Visual Asset**: Refusal decision flowchart demonstrating zero-token short-circuiting on out-of-domain queries.
* **The Refusal Rule**:
  $$\text{Decision} = \begin{cases} \text{Refuse immediately ("I don't have enough information..."),} & \text{if } \max_{c \in C} \text{score}(c) < 0.35 \\ \text{Proceed to Two-Pass Generation,} & \text{otherwise} \end{cases}$$
* **Engineering Hardening**:
  - Evaluates the **maximum score across candidates** rather than position 0, preventing false refusals in asymmetric hybrid rankings where position 0 is a sparse-only hit.
  - **Zero LLM Tokens Billed**: Short-circuits the pipeline before calling generative APIs, eliminating hallucinations and costs on unanswerable questions.
  - Empirically calibrated: Achieves **90.0% Refusal Correctness** on `ML Papers v1`.
* **Speaker Notes**:
  > "Standard RAG systems always call the LLM, hallucinating answers when papers do not contain the answer. Our Deterministic Refusal Gate inspects the candidate set before LLM invocation. If the maximum similarity falls below 0.35, the system immediately returns a refusal. This costs 0 API tokens and achieves 90% refusal correctness on out-of-domain questions."

---

## Slide 9: Multi-Provider LLM Seam & Gemini 2.5 Flash
* **Header**: High-Throughput Routing with Provider Fallbacks
* **Visual Asset**: Provider routing table with adapter fallback paths and zero-argument client factory flow.
* **Provider Ecosystem**:
  - **Google AI Studio**: Gemini 2.5 Flash / Lite via OpenAI-compatible REST endpoint (Free tier: 20 RPD optimized).
  - **Groq Cloud LPU**: Ultra-fast inference ($>500\text{ tok/s}$) for low-latency live querying.
  - **OpenAI & Anthropic**: GPT-4o, GPT-5-mini, Claude 3.5 Sonnet / Haiku.
  - **Local Air-Gapped**: Ollama (`llama3`, `mistral`) for 100% offline environments.
  - **Graceful Degradation (`DummyAdapter`)**: Catches API outages or missing credentials, returning retrieved citations without crashing.
* **Speaker Notes**:
  > "Our LLMHandler supports transparent routing across Google AI Studio, Groq, OpenAI, Anthropic, and local Ollama. Under ADR 0002, SDK clients are injected via zero-argument factories. If an external API is unavailable or rate-limited, the system falls back gracefully to DummyAdapter, presenting the user with verified sources rather than an unhandled error."

---

## Slide 10: Two-Pass Streaming UX: Visible Chain-of-Thought
* **Header**: Real-Time Reasoning Streaming over WebSockets
* **Visual Asset**: UI screenshot showing collapsible 'Thinking Process' accordion alongside streamed markdown response.
* **Two-Step Generation Protocol**:
  - **Pass 1 (Reasoning / Thinking)**: Fast model (`gpt-4.1-nano` or Gemini Flash) streams visible chain-of-thought tokens (`type: "reasoning"`) into an expandable thoughts accordion.
  - **Pass 2 (Grounded Answer)**: Primary LLM streams factual synthesized response (`type: "token"`) strictly conditioned on context and reasoning.
  - **User Impact**: Eliminates perceived latency; users observe analytical thought progression before reading the synthesized result.
* **Speaker Notes**:
  > "Over WebSockets, we implement a two-pass generation protocol. Pass 1 streams the model's intermediate Chain-of-Thought reasoning into a collapsible UI panel. Pass 2 streams the grounded final answer. This eliminates perceived latency and allows the researcher to audit the AI's logical deductions in real time."

---

## Slide 11: Real-Time Telemetry & Pricing Ledger
* **Header**: Transparent Latency & Cost Accounting
* **Visual Asset**: Telemetry data structure and live UI footer badge showing latency, token count, and USD expenditure.
* **Audited Telemetry Payload (`StageTelemetry`)**:
  - `retrieve_ms`: Exact millisecond retrieval time.
  - `generate_ms`: Generation latency.
  - `prompt_tokens` & `completion_tokens`: Provider-audited token tallies.
  - `cost_usd`: Calculated dynamically via internal pricing table.
* **UI Integration**:
  - Rendered in real-time message footer: `⏱️ 842ms | 🪙 1,240 tokens | 💵 $0.0003`.
* **Speaker Notes**:
  > "To satisfy RQ4, every query generates an immutable StageTelemetry record. We measure retrieval time, generation time, prompt tokens, completion tokens, and real-time USD cost. This provides institutional transparency and allows research labs to forecast deployment expenses."

---

## Slide 12: Empirical Evaluation & Benchmark Results
* **Header**: Validating Retrieval & Hallucination Resistance
* **Visual Asset**: Benchmark metric table and 95% confidence interval comparison chart.
* **Evaluation on `ML Papers v1` (460 Chunks, 10 Golden Questions)**:

| Metric | Dimension | Score | 95% Confidence Interval |
| :--- | :--- | :---: | :---: |
| **Refusal Correctness** | Hallucination Safety | **0.9000** | [0.7000, 1.0000] |
| **Judge Faithfulness** | Groundedness / Factual Truth | **1.0000** | [1.0000, 1.0000] |
| **Recall@5** | Document Coverage | **0.3889** | [0.1111, 0.6958] |
| **MRR@5** | Rank Precision | **0.3333** | [0.1375, 0.6403] |
| **Answer Correctness** | Response Quality | **0.5260** | [0.5060, 0.5416] |
| **Automated Test Suite** | CI/CD Code Integrity | **558 / 558 Passed** | **0 API Tokens Consumed** |

* **Speaker Notes**:
  > "We evaluated the architecture on ML Papers v1, an open benchmark of seminal literature in Transformers, RAG, and LoRA. The empirical results demonstrate 90% refusal correctness on unanswerable questions and a 1.0000 faithfulness score from an independent LLM judge, confirming zero hallucinated claims."

---

## Slide 13: Live Demonstration Walkthrough
* **Header**: Interactive System Demonstration
* **Visual Asset**: Live screen preview showing document upload, answerable query with page badge, and unanswerable query refusal.
* **Demonstration Protocol**:
  1. **Upload & Ingestion**: Uploading `attention_is_all_you_need.pdf` $\rightarrow$ Real-time page parsing and SHA-256 deduplication.
  2. **Answerable Query**: *"Why does scaled dot-product attention divide by square root of d_k?"*
     - Live CoT reasoning stream $\rightarrow$ Synthesized response $\rightarrow$ Clickable `(p. 4)` page citation badge.
  3. **Unanswerable Query**: *"What is the optimal learning rate for FlashAttention-2?"*
     - Refusal gate short-circuiting $\rightarrow$ Immediate deterministic refusal with 0 LLM tokens billed.
* **Speaker Notes**:
  > "I will now demonstrate the live system. First, we ingest the Vaswani et al. paper. Next, we submit an answerable question on scaled dot-product attention. Notice the visible reasoning stream and the page 4 citation badge. Finally, when asking an out-of-corpus question regarding FlashAttention-2, the refusal gate intercepts the request immediately with zero tokens consumed."

---

## Slide 14: Conclusion & Future Research Directions
* **Header**: Conclusion & Future Horizon
* **Visual Asset**: Summary roadmap showing current achievements and future GraphRAG / Multimodal extensions.
* **Core Takeaways**:
  - Proved that rigorous software architecture (Hexagonal seams, RRF, deterministic gating) solves the core vulnerabilities of scientific RAG.
  - Guaranteed exact physical page citation and 90% hallucination prevention.
  - Engineered an enterprise-ready system with 558 passing tests and multi-provider agility.
* **Future Work**:
  - **GraphRAG**: Entity-relation knowledge graphs across multi-paper citation networks.
  - **Multimodal Layout Models**: Integrating vision embeddings (ColPali) for embedded diagrams and scientific tables.
* **Closing**:
  > "In conclusion, verifiable AI over scientific literature requires disciplined engineering boundaries rather than ad-hoc scripts. I extend my sincere gratitude to my supervisor, Dr. Mostofa Kamal Nasir, and to the respected committee members. Thank you. I am now ready to answer your questions."
