# Defence Roadmap & Stage Tracker

> Note: এই ডকুমেন্টের মূল বিস্তারিত সংস্করণ রুট ডিরেক্টরিতে [`PROJECT_STATUS.md`](file:///Users/mgtapp/dotnet/rag-document-qa/PROJECT_STATUS.md)-এ সংরক্ষিত আছে।

## পরবর্তী সেশনে কাজ শুরুর কুইক নির্দেশিকা:

1. **ফাইল রেফারেন্স**: সম্পূর্ণ অডিট ও প্ল্যানের জন্য রুট ফাইলের [`PROJECT_STATUS.md`](file:///Users/mgtapp/dotnet/rag-document-qa/PROJECT_STATUS.md) পড়ুন।
## বর্তমান অগ্রগতি ও সম্পন্ন ধাপসমূহ:

- [x] **Day 1: Environment & Base Setup** (venv, requirements.txt, .env, baseline test suite 556/556 passing).
- [x] **Day 2: Codebase Core Fixes** (PDF page number tracking, chunk page metadata propagation, backend API citations `page_number`, frontend `(p. X)` badge in `sources-panel.tsx`, Gemini 2.5 Flash OpenAI-compatible routing, and production RefusalHandler integration).
- [x] **Day 3: Custom Dataset & Mini Benchmark** (3টি পেপার Attention, RAG, LoRA যুক্ত ও ভেরিফাইড; ১০টি গোল্ডেন প্রশ্ন তৈরি; অফলাইন মিনি ইভ্যালুয়েশন রান সম্পন্ন: Recall@5: 0.3889, Refusal Correctness: 0.9000, 0 টোকেন খরচ)।
- [x] **Day 4: Architecture & Thesis Report Draft** ([`docs/Architecture.md`](file:///d:/work/dotnet/ai-research-assistant/docs/Architecture.md) এবং [`docs/THESIS_REPORT_DRAFT.md`](file:///d:/work/dotnet/ai-research-assistant/docs/THESIS_REPORT_DRAFT.md)-এ Chapter 1–4 সম্পন্ন)।
- [x] **Day 5: Results & Report Finalization** ([`docs/THESIS_REPORT_DRAFT.md`](file:///d:/work/dotnet/ai-research-assistant/docs/THESIS_REPORT_DRAFT.md)-এ Chapter 5-এর ফলাফল টেবিল ও Chapter 6-এর কনক্লুশন সম্পন্ন)।
- [x] **Day 6: Defence Presentation Slide Deck** ([`docs/DEFENSE_SLIDES.md`](file:///d:/work/dotnet/ai-research-assistant/docs/DEFENSE_SLIDES.md)-এ ১৪টি সম্পূর্ণ স্লাইড ও স্পিকার নোটস প্রস্তুত)।
- [x] **Day 7: Mock Defence & Rehearsal** ([`docs/MOCK_DEFENSE_QA.md`](file:///d:/work/dotnet/ai-research-assistant/docs/MOCK_DEFENSE_QA.md)-এ ৭টি ট্র্যাপ প্রশ্ন ও রেডিমেড ডিফেন্স উত্তর প্রস্তুত)।

## ডিফেন্স ও ফাইনাল ডেমো স্ট্যাটাস:
- সম্পূর্ণ কোডবেস, টেস্ট স্যুট (৫৫৮/৫৫৮ পাসিং), থিসিস রিপোর্ট ড্রাফট, প্রেজেন্টেশন স্লাইড এবং মক ডিফেন্স প্রশ্নোত্তর শতভাগ সম্পন্ন। ডিফেন্সের জন্য সিস্টেম সম্পূর্ণ রেডি!
