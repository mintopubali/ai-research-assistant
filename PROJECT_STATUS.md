# 🚀 Project Status & Master Defence Handover

> **Document Purpose**: এই ফাইলটি প্রজেক্টের বর্তমান স্ট্যাটাস, অডিট রিপোর্ট এবং ডিফেন্সের সম্পূর্ণ রোডম্যাপ সংরক্ষণ করে। অন্য যেকোনো পিসি বা নতুন সেশনে এই ফাইলটি পড়েই এজেন্ট বা ডেভেলপার সাথে সাথে বুঝতে পারবে প্রজেক্ট কোন ধাপে আছে এবং ঠিক এরপর কী করতে হবে।
> 
> **Target Deadline**: আগামী সপ্তাহের ডিফেন্স ও ফাইনাল সাবমিশন।

---

## 📌 ১. প্রজেক্টের বর্তমান অবস্থা (Current Stage)

- **আর্কিটেকচার**: ৯৫% সম্পন্ন (Hexagonal Architecture, 10 ADRs, Clean Seams, SQLite + ChromaDB)।
- **ফ্রন্টএন্ড**: সম্পূর্ণ কোড করা আছে (React 19 + TypeScript + Vite + Tailwind v4 + WebSocket CoT Streaming)।
- **টেস্ট স্যুট**: ৫৫টি টেস্ট ফাইল প্রস্তুত (`tests/`), যার বেশিরভাগই ফেইক/মক দিয়ে কভার্ড।
- **পরিবেশ ও ডিপেনডেন্সি**:
  - লোকাল মেশিনে পাইথন ডিপেনডেন্সি এখনও ইনস্টল করা হয়নি।
  - `.env` ফাইল এখনও কনফিগার করা হয়নি।
- **API ও রেট লিমিট স্ট্যাটাস**:
  - ইউজারের কাছে **Google AI Studio (Free Tier)** আছে।
  - রেট লিমিট: **Gemini 2.5 Flash / Lite / 3 Flash = 20 Requests/Day (20 RPD)**।
  - তাই টেস্ট প্ল্যান এমনভাবে ডিজাইন করা হয়েছে যাতে দিনে ২০টি রিকোয়েস্টের একটিও অপচয় না হয় (ইউনিট টেস্টে ০ খরচ, লাইভ ডেমোতে ৩-৫টি টেস্ট কুয়েরি)।

---

## 🔍 ২. কোডবেস অডিট ফাইন্ডিংস (Audit Findings & Gaps)

সম্পূর্ণ এন্ড-টু-এন্ড ফ্লো অডিট করে নিচের বিষয়গুলো চিহ্নিত করা হয়েছে:

### ✅ যা সঠিকভাবে ইমপ্লিমেন্ট করা আছে:
1. **Validation & Upload**: `upload.py`-তে এক্সটেনশন ও ৫০ MB সাইজ লিমিট হ্যান্ডলিং।
2. **Chunking**: `chunking.py`-তে রিকার্সিভ চাঙ্কিং ও ToC ডট-লিডার ফিল্টার।
3. **Storage**: ChromaDB-তে কোসাইন স্পেস ভেক্টর স্টোরেজ এবং SQLite-এ চ্যাট হিস্ট্রি।
4. **Retrieval**: Dense, BM25 Hybrid (with RRF $k=60$), Cross-Encoder Reranker এবং Multi-Query Seam।
5. **Streaming UX**: WebSocket দিয়ে রিজনিং/থিঙ্কিং পাস ও অ্যান্সার জেনারেশন পাস।
6. **Fallback**: API কী না থাকলে `DummyAdapter` দিয়ে গ্রেসফুল ফলব্যাক।

### ⚠️ যে ৩টি প্রধান গ্যাপ অবিলম্বে ঠিক করতে হবে:
1. **Page Number Dropped (সবচেয়ে ক্রিটিক্যাল)**:
   - ফাইল: `src/ingestion/parsers.py` (`parse_pdf`)।
   - সমস্যা: সব পেজের টেক্সট `\n\n.join` করে জোড়া দেওয়া হয়, পেজ নম্বর মেটাডেটায় সংরক্ষণ করা হয় না।
   - প্রভাব: সাইটেশনে শুধু `chunk_index` আসে, কোনো `page_number` থাকে না।
2. **Refusal Gate Disconnected in Production**:
   - ফাইল: `src/backend.py` (`RAGBackend.__init__`)।
   - সমস্যা: `QueryEngine`-এ `refusal=None` পাঠানো হয়েছে। ফলে আন-অ্যান্সারেবল কুয়েরিতে প্রোডাকশন ফেসাড স্বয়ংক্রিয়ভাবে রিফিউজ করে না।
3. **Empty Benchmark Dataset**:
   - ডিরেক্টরি: `eval_data/ml_papers_v1/`
   - সমস্যা: `questions.jsonl` খালি (0 bytes) এবং `corpus_manifest.json`-এ কোনো পেপার নেই।

---

## 🗓️ ৩. ৭ দিনের ডিফেন্স স্প্রিন্ট প্ল্যান (Checklist)

- [x] **Day 1: Environment & Base Setup**
  - [x] Python venv তৈরি ও `pip install -r requirements.txt` সম্পন্ন করা (সব ২৪টি ডিপেনডেন্সি ইনস্টলড)।
  - [x] `.env` ফাইলে `GEMINI_API_KEY` কনফিগার করা।
  - [x] `pytest tests/` চালিয়ে বেসলাইন গ্রিন টেস্ট ভেরিফাই করা (৫৫৬/৫৫৬ পাস)।
- [x] **Day 2: Codebase Core Fixes**
  - [x] `src/ingestion/parsers.py`-তে PDF পেজ নম্বর ট্র্যাকিং ইমপ্লিমেন্ট করা (`meta["pages"]`)।
  - [x] `src/ingestion/chunking.py`-তে চাঙ্কের মেটাডেটায় `page_number` যোগ করা (ChromaDB সেফ)।
  - [x] `src/backend.py`-এর `_source_dict` ও API মডেলে `page_number` ফিল্ড পাঠানো এবং ফ্রন্টএন্ড UI-তে ব্যাজ দেখানো।
  - [x] `src/llm_handler/providers.py`-তে Gemini 2.5 Flash OpenAI-compatible অ্যাডাপ্টার রাউটিং যুক্ত করা।
  - [x] `src/backend.py`-এ `RefusalHandler` প্রোডাকশনে যুক্ত করা।
- [x] **Day 3: Custom Dataset & Mini Benchmark**
  - [x] `eval_data/ml_papers_v1/`-এ ৩টি ক্লাসিক পেপার (Attention, RAG, LoRA) যোগ ও ভেরিফাই করা (৪৬০ চাঙ্ক)।
  - [x] ১০টি গোল্ডেন প্রশ্ন তৈরি করে একটি মিনি-ইভ্যালুয়েশন রান চালানো (Recall@K ও Faithfulness, ০ টোকেন খরচ)।
- [ ] **Day 4: Thesis Report / Proposal Draft**
  - [ ] `Architecture.md` এবং ADRs ব্যবহার করে চ্যাপ্টার ১ থেকে ৪ লেখা।
- [ ] **Day 5: Results & Report Completion**
  - [ ] মিনি বেঞ্চমার্কের টেবিল ও গ্রাফ চ্যাপ্টার ৫-এ বসিয়ে চ্যাপ্টার ৬ সহ ফাইনাল রিপোর্ট সম্পন্ন করা।
- [ ] **Day 6: Defence Presentation Slide Deck**
  - [ ] ১২-১৪ স্লাইডের প্রেজেন্টেশন ডেক প্রস্তুত করা।
  - [ ] আর্কিটেকচার ডায়াগ্রাম ও লাইভ ডেমো স্ক্রিনশট বসানো।
- [ ] **Day 7: Mock Defence & Rehearsal**
  - [ ] এক্সামিনারদের সম্ভাব্য ৭টি ট্র্যাপ প্রশ্ন প্র্যাকটিস করা।
  - [ ] অফলাইন ফলব্যাক ডেমো রেডি রাখা।

---

## 💻 ৪. নতুন সেশন বা নতুন পিসিতে কাজ শুরুর স্টেপ-বাই-স্টেপ গাইড

নতুন পিসিতে এই রিপোজিটরি ওপেন করে এজেন্টকে বলুন:
> *"PROJECT_STATUS.md ফাইলটি পড়ো এবং Day 1 / পরবর্তী অসমাপ্ত চেকলিস্ট ধরে কাজ শুরু করো।"*

### এক্সিকিউশন কমান্ডসমূহ (Step-by-Step Commands):

#### Step 1: Virtual Environment তৈরি ও ডিপেনডেন্সি ইনস্টল
```bash
# ১. পাইথন ৩.১২ venv তৈরি
/opt/homebrew/bin/python3.12 -m venv venv
# অথবা
python3 -m venv venv

# ২. অ্যাক্টিভেট করা
source venv/bin/activate

# ৩. প্যাকেজ ইনস্টল করা
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: `.env` ফাইল কনফিগারেশন
প্রজেক্টের রুট ডিরেক্টরিতে `.env` ফাইল তৈরি করুন:
```env
# Gemini API Key (Google AI Studio থেকে প্রাপ্ত)
GEMINI_API_KEY=your_gemini_api_key_here

# Default Models
DEFAULT_MODEL=gemini-2.5-flash
REASONING_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash

# Retrieval Strategy (dense / hybrid / reranked / multi_query)
RETRIEVER_STRATEGY=dense
```

#### Step 3: বেসলাইন টেস্ট চালানো (০ API টোকেন খরচ)
```bash
pytest tests/ -v
```

#### Step 4: ব্যাকএন্ড ও ফ্রন্টএন্ড রান করা
```bash
# টার্মিনাল ১: ব্যাকএন্ড সার্ভার (Port 8001)
uvicorn src.api.main:app --host 0.0.0.0 --port 8001 --reload

# টার্মিনাল ২: ফ্রন্টএন্ড সার্ভার (Port 5173)
cd frontend
npm install
npm run dev
```

---

## 🎓 ৫. ডিফেন্স প্রেজেন্টেশন ও থিসিস চ্যাপ্টার গাইড

### থিসিস রিপোর্টের ৬টি চ্যাপ্টার:
1. **Chapter 1: Introduction**: হ্যালুসিনেশন সমস্যা, ভেরিফায়েবল সোর্সের গুরুত্ব, অবজেক্টিভস।
2. **Chapter 2: Literature Review**: BM25, Dense Retrieval (`all-MiniLM-L6-v2`), RRF ফিউশন (Cormack et al., 2009), Cross-Encoders, RAGAS (Es et al., 2023)।
3. **Chapter 3: System Architecture**: Hexagonal Seams, Ingestion Pipeline, Hybrid Retrieval, CoT Streaming, Evaluation Engine।
4. **Chapter 4: Implementation Details**: FastAPI, React 19, ChromaDB, SQLModel, Telemetry/Cost Tracking, Fallback Adapters।
5. **Chapter 5: Evaluation & Results**: SQuAD v2 ও ML Papers v1 বেঞ্চমার্ক (Recall@5, MRR@5, Faithfulness, Latency vs Cost)।
6. **Chapter 6: Limitations & Future Scope**: ফলো-আপ কুয়েরি রি-রাইটিং, GraphRAG, মাল্টিমোডাল ভিশন।

### এক্সামিনারদের টপ ৩টি প্রশ্ন ও রেডিমেড ডিফেন্স উত্তর:
1. **"BM25 এবং ভেক্টর সার্চ কীভাবে কম্বাইন করেছেন?"**  
   👉 *উত্তর*: "আমরা **Reciprocal Rank Fusion (RRF, $k=60$)** ব্যবহার করেছি। BM25 এবং কোসাইন দূরত্বের স্কেল ভিন্ন হওয়ায় সরাসরি স্কোর যোগ করা যায় না। RRF তাদের অর্ডিনাল র‍্যাংকের ভিত্তিতে কম্বাইন করে: $\text{Score}(d) = \sum \frac{1}{60 + r(d)}$।"
2. **"হ্যালুসিনেশন ঠেকাতে আপনার সিস্টেমের মেকানিজম কী?"**  
   👉 *উত্তর*: "তিনটি স্তর: (ক) স্ট্রিক্ট কনটেক্সট-অনলি প্রম্পট, (খ) ডিটারমিনিস্টিক রিফিউজাল গেট (থ্রেশহোল্ড ০.৩৫-এর নিচে নামলে সরাসরি রিফিউজ করে), এবং (গ) এলএলএম-অ্যাজ-আ-জাজ দিয়ে পোস্ট-জেনারেশন ফেথফুলনেস যাচাই।"
3. **"চাঙ্ক সাইজ ৫১২ এবং ওভারল্যাপ ৬৪ বেছে নেওয়ার কারণ কী?"**  
   👉 *উত্তর*: "চাঙ্ক বেশি ছোট হলে অর্থ বিচ্ছিন্ন হয়ে যায়, বেশি বড় হলে একাধিক টপিক একসাথে মিশে ভেক্টর এভারেজিং হয়ে রিট্রিভাল প্রিসিশন কমে। ৫১২ ক্যারেক্টার ২-৩টি পূর্ণাঙ্গ বাক্যের জন্য আদর্শ এবং ৬৪ অক্ষরের ওভারল্যাপ বাক্য ভাঙার সমস্যা দূর করে।"

---
*সর্বশেষ আপডেট: অক্টোবর ২০২৬ | প্রস্তুতকারী: Antigravity AI Pair Programmer*
