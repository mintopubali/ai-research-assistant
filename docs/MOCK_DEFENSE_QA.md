# 🛡️ Mock Defence Preparation: 7 Examiner Trap Questions & Model Answers

> **Purpose**: This document prepares the candidate for the most rigorous and adversarial technical questions typically asked by external examiners and review boards during a RAG / Applied AI thesis defence.

---

### Question 1: "Why did you use Reciprocal Rank Fusion (RRF) instead of a learned or weighted linear combination of BM25 and Dense scores?"

**The Trap**: The examiner wants to see if you understand score calibration and the mathematical differences between vector and lexical scoring spaces.

**Model Answer**:
> "Linear combination requires normalizing BM25 and Cosine similarity scores into a shared interval:
> $$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Score}_{\text{dense}} + (1 - \alpha) \cdot \text{Score}_{\text{sparse}}$$
> However, this approach is fundamentally fragile for three reasons:
> 1. **Distribution Mismatch**: Cosine similarity for dense embeddings (such as `all-MiniLM-L6-v2`) occupies a narrow range typically between 0.20 and 0.65, whereas BM25 scores are unbounded $[0, \infty)$ and scale with document length and term frequencies.
> 2. **Corpus Instability**: Any change in corpus size shifts the BM25 inverse document frequency ($\text{IDF}$), which breaks the tuned weighting parameter $\alpha$.
> 3. **Rank Invariant Guarantee**: As Cormack, Clarke, and Büttcher (2009) proved, **Reciprocal Rank Fusion (RRF)**:
>    $$\text{RRF\_Score}(d) = \sum_{m} \frac{1}{k + r_m(d)}$$
>    is completely agnostic to raw score scales because it operates strictly on ordinal ranks $r_m(d)$. Using the standard constant $k=60$ dampens the penalty for lower-ranked documents while ensuring that if an exact acronym appears high in BM25 or a conceptual match appears high in dense search, it ranks at the top of the fused set."

---

### Question 2: "How does your system guarantee that a retrieved chunk cites the exact page number of the original PDF?"

**The Trap**: Naive RAG splits raw text after parsing and loses page offsets, or stores nested objects that crash vector databases like ChromaDB.

**Model Answer**:
> "We implemented physical page tracking across three coordinated architectural layers:
> 1. **Page-by-Page Extraction**: In `src/ingestion/parsers.py`, `PyPDFParser` extracts text page-by-page and records a dictionary structure `meta['pages'] = [{'page_number': idx + 1, 'text': page_text}]`.
> 2. **Page-Bounded Chunking**: In `src/ingestion/chunking.py`, `TextChunker` chunks *within* each page rather than concatenating text across pages. Every produced chunk receives an explicit scalar `page_number` in its metadata.
> 3. **Schema Compliance**: ChromaDB enforces a strict scalar-only constraint (`str`, `int`, `float`, `bool`) on metadata. We strip the complex `pages` list before vector store upsert while preserving the scalar `page_number`.
> 4. **API and UI Propagation**: The backend `_source_dict` extracts `page_number` and passes it through FastAPI `SourceInfo` models to the React frontend, which renders physical badges like `(p. 4)` on every citation."

---

### Question 3: "If your vector database returns similarity scores, why do you need a Cross-Encoder reranker?"

**The Trap**: The examiner is probing your knowledge of the bi-encoder vs. cross-encoder computational trade-off.

**Model Answer**:
> "Bi-encoders (`all-MiniLM-L6-v2`) embed the query and document independently: $u = f(q)$ and $v = f(d)$. They compute similarity as a dot product, which enables sub-millisecond vector indexing using approximate nearest neighbors (HNSW). However, bi-encoders cannot model fine-grained token-level cross-attention between the query and passage.
> 
> In contrast, the Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) feeds the concatenated pair $[CLS] \circ q \circ [SEP] \circ p$ into full bidirectional transformer attention layers. Every token in the query attends to every token in the passage.
> 
> Because cross-encoders are computationally expensive ($O(N \cdot L^2)$), we utilize a two-stage retrieve-and-rerank design: the bi-encoder over-fetches candidates (e.g., top $2 \times k$), and the Cross-Encoder re-ranks only those candidates to place the causally answerable passage at rank 1."

---

### Question 4: "What mechanisms prevent your system from hallucinating when a question cannot be answered from the uploaded papers?"

**The Trap**: The examiner wants to see if you rely purely on prompt engineering or have architectural fail-safes.

**Model Answer**:
> "We employ a defense-in-depth strategy across three independent levels:
> 1. **Deterministic Refusal Gating (Phase 2 Lever 2g)**: Before calling the LLM, `RefusalHandler` inspects the candidate retrieval set. If the maximum similarity score across the set falls below the threshold ($\tau = 0.25$), the pipeline short-circuits immediately, returning a fixed refusal message with 0 LLM tokens consumed.
> 2. **Strict Context-Bounded Prompts**: The generation prompt explicitly instructs the LLM: *'Answer strictly using the provided context. If the context does not contain sufficient facts, state that you cannot answer.'*
> 3. **Post-Generation LLM-as-a-Judge Evaluation**: In `MessageEvaluator`, a secondary judge model evaluates the answer for **Faithfulness** against the retrieved chunks, detecting ungrounded claims."

---

### Question 5: "Why did you choose a chunk size of 512 characters and an overlap of 64 characters?"

**The Trap**: The examiner wants empirical or technical justification rather than an arbitrary choice.

**Model Answer**:
> "Chunk size represents a direct trade-off between semantic specificity and contextual completeness:
> - **Too Large (>1000 chars)**: Multiple distinct ideas and formulas become averaged into a single vector representation, reducing retrieval precision.
> - **Too Small (<150 chars)**: Chunks lose surrounding context, and pronouns/antecedents lose their referents.
> - **512 Characters**: In English academic prose, 512 characters corresponds to approximately 2 to 3 full grammatical sentences—sufficient to capture a complete scientific claim, definition, or formula.
> - **64 Character Overlap**: Ensures that sentences spanning across a chunk split boundary are not clipped abruptly, providing contextual continuity for the embedding model."

---

### Question 6: "How do you handle multi-turn conversations without overflowing the LLM context window or polluting retrieval?"

**The Trap**: Tests understanding of conversational state and sliding window memory management.

**Model Answer**:
> "In `src/conversations.py`, we implement a strict sliding window of prior completed message pairs (default: 3 pairs = 6 messages):
> 1. **Sliding Window Storage**: SQLite stores the full history for UI display, but `ConversationHistory` extracts only the last $N$ turns for the LLM prompt.
> 2. **Unpaired Turn Guard**: When generating an answer, the current user query is unpaired; the sliding window only includes previously answered turns, preventing dangling prompt injection.
> 3. **Retrieval Isolation**: Retrieval searches are executed using the current natural language query (or optionally expanded through `MultiQueryRetriever`), preventing historical chat noise from diluting vector search relevance."

---

### Question 7: "What happens if the external LLM API (Google AI Studio / OpenAI) experiences an outage or hits its rate limit during a live query?"

**The Trap**: Tests system reliability, error handling, and offline resilience.

**Model Answer**:
> "The system was designed for graceful degradation:
> 1. **Injected Client Factories**: As defined in ADR 0002, SDK clients are constructed per-request through injected zero-argument factories.
> 2. **Provider Fallback Adapter (`DummyAdapter`)**: If an API key is missing or an SDK raises a `ProviderUnavailableError` (or rate limit / connection timeout), the pipeline does not crash. It automatically catches the exception and falls back to `DummyAdapter`, returning a formatted response: `[LLM unavailable] The system retrieved the following sources...` along with the retrieved chunks and page citations.
> 3. **Local Offline Alternative**: In environments without internet access or strict privacy constraints, the system can be switched to local `Ollama` with a single configuration parameter: `DEFAULT_MODEL=llama3`."
