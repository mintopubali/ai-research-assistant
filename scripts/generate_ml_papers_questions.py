import hashlib
import json
from pathlib import Path

from src.eval.config import load_config
from src.eval.pipeline_factory import build_pipeline
from src.eval.schemas import EvalQuestion

def generate_questions():
    cfg = load_config(Path("configs/eval/baseline.yaml"))
    pipeline = build_pipeline(cfg, "ml_papers_v1")
    pipeline.ingest([])

    questions_data = [
        # 1. Definition - Attention
        {
            "query": "Scaled Dot-Product Attention scaling factor square root dk",
            "question": "In Vaswani et al. (2017), what scaling factor is applied to the dot products in Scaled Dot-Product Attention?",
            "gold_answer": "The dot products are divided by the square root of the dimension of the keys, 1/sqrt(d_k).",
            "paper": "attention-is-all-you-need",
            "difficulty": "definition",
            "unanswerable": False,
        },
        # 2. Reasoning - Attention
        {
            "query": "We suspect that for large values of dk the dot products grow large in magnitude softmax function",
            "question": "Why does the Transformer architecture scale the dot products by 1/sqrt(d_k) before applying the softmax function?",
            "gold_answer": "For large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions with extremely small gradients. Dividing by sqrt(d_k) counteracts this effect.",
            "paper": "attention-is-all-you-need",
            "difficulty": "reasoning",
            "unanswerable": False,
        },
        # 3. Definition - Attention FFN
        {
            "query": "Position-wise Feed-Forward Networks max(0, xW1 + b1)W2 + b2",
            "question": "What activation function and mathematical formula define the position-wise feed-forward networks (FFN) in the Transformer?",
            "gold_answer": "The position-wise FFN consists of two linear transformations with a ReLU activation in between: FFN(x) = max(0, xW_1 + b_1)W_2 + b_2.",
            "paper": "attention-is-all-you-need",
            "difficulty": "definition",
            "unanswerable": False,
        },
        # 4. Definition - RAG Models
        {
            "query": "Dense Passage Retriever DPR generator BART pre-trained seq2seq",
            "question": "In Lewis et al. (2020), which pre-trained models serve as the retriever and generator components in RAG?",
            "gold_answer": "RAG pairs a pre-trained Dense Passage Retriever (DPR) as the non-parametric retriever with BART as the parametric seq2seq generator.",
            "paper": "retrieval-augmented-generation",
            "difficulty": "definition",
            "unanswerable": False,
        },
        # 5. Reasoning - RAG-Sequence vs RAG-Token
        {
            "query": "RAG-Sequence model uses the same retrieved document to generate the complete sequence RAG-Token",
            "question": "How do RAG-Sequence and RAG-Token models differ in how they marginalize over retrieved documents?",
            "gold_answer": "RAG-Sequence treats the retrieved document as a single latent variable across the entire generated sequence, whereas RAG-Token marginalizes over retrieved documents on a per-token basis, allowing different documents to inform different tokens.",
            "paper": "retrieval-augmented-generation",
            "difficulty": "reasoning",
            "unanswerable": False,
        },
        # 6. Definition - LoRA Initialization
        {
            "query": "We use a random Gaussian initialization for A and zero for B so delta W is zero at the beginning",
            "question": "In the LoRA paper (Hu et al., 2021), how are the low-rank matrices A and B initialized at the beginning of training?",
            "gold_answer": "Matrix A is initialized with a random Gaussian distribution and matrix B is initialized to zero, ensuring Delta W = B * A is initially zero at the start of training.",
            "paper": "lora-low-rank-adaptation",
            "difficulty": "definition",
            "unanswerable": False,
        },
        # 7. Reasoning - LoRA No Inference Latency
        {
            "query": "No Additional Inference Latency W = W0 + BA during deployment",
            "question": "Why does LoRA introduce zero additional inference latency during production deployment compared to a fully fine-tuned model?",
            "gold_answer": "During deployment, the low-rank update Delta W = B * A can be explicitly folded into the frozen pre-trained weights W_0 by computing W = W_0 + B * A, restoring standard matrix multiplication with no extra latency.",
            "paper": "lora-low-rank-adaptation",
            "difficulty": "reasoning",
            "unanswerable": False,
        },
        # 8. Reasoning - LoRA Alpha Scaling
        {
            "query": "When optimizing with Adam we scale delta W by alpha over r",
            "question": "In LoRA, what is the purpose of scaling the weight update by alpha / r?",
            "gold_answer": "Scaling Delta W by alpha / r stabilizes training when varying the rank r, allowing hyperparameters (like learning rate) tuned for one rank to transfer without retuning.",
            "paper": "lora-low-rank-adaptation",
            "difficulty": "reasoning",
            "unanswerable": False,
        },
        # 9. Multi-Hop - Transformer Attention & LoRA
        {
            "query": "We limit our study to only adapting the attention weights Wq Wk Wv Wo in the Transformer",
            "question": "When applying LoRA to a Transformer architecture, which attention weight matrices are typically adapted, and how does this contrast with standard full fine-tuning?",
            "gold_answer": "LoRA typically adapts only the query (W_q) and value (W_v) projection matrices in the self-attention sublayer by freezing the original weights and injecting low-rank matrices, whereas full fine-tuning updates all Transformer parameters across all layers.",
            "paper": "lora-low-rank-adaptation",
            "difficulty": "multi_hop",
            "unanswerable": False,
        },
        # 10. Unanswerable
        {
            "query": "",
            "question": "What optimizer learning rate and warm-up step count does the FlashAttention-2 paper recommend for 8x A100 training?",
            "gold_answer": None,
            "paper": "unanswerable",
            "difficulty": "reasoning",
            "unanswerable": True,
        },
    ]

    eval_questions = []
    for item in questions_data:
        qid = hashlib.sha256(item["question"].encode("utf-8")).hexdigest()[:16]
        if item["unanswerable"]:
            gold_chunk_ids = []
        else:
            hits = pipeline.vector_store.query(item["query"], top_k=2)
            gold_chunk_ids = [h.chunk_id for h in hits[:2]]

        eq = EvalQuestion(
            id=qid,
            question=item["question"],
            gold_answer=item["gold_answer"],
            gold_chunk_ids=gold_chunk_ids,
            is_unanswerable=item["unanswerable"],
            metadata={
                "source_paper": item["paper"],
                "difficulty": item["difficulty"],
                "labeler": "agent_auto",
            },
        )
        eval_questions.append(eq)

    out_path = Path("eval_data/ml_papers_v1/questions.jsonl")
    with out_path.open("w", encoding="utf-8") as f:
        for eq in eval_questions:
            f.write(eq.model_dump_json() + "\n")

    print(f"Successfully generated and wrote {len(eval_questions)} golden questions to {out_path}")

if __name__ == "__main__":
    generate_questions()
