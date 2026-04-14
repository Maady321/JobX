from sentence_transformers import SentenceTransformer, util
import torch
import config

# Lazy-loaded model (prevents unnecessary reloads)
_model = None

def get_model():
    global _model
    if _model is None:
        print("[INFO] Loading AI model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


# Precompute keyword embeddings once
_keyword_embeddings = None

def get_keyword_embeddings():
    global _keyword_embeddings
    if _keyword_embeddings is None:
        model = get_model()
        print("[INFO] Encoding keywords...")
        _keyword_embeddings = model.encode(config.KEYWORDS, convert_to_tensor=True)
    return _keyword_embeddings


def is_relevant(job_title: str) -> bool:
    """
    Determine if a job title is relevant using:
    1. Keyword matching (precision)
    2. Semantic similarity (AI understanding)
    """

    if not job_title:
        return False

    title = job_title.lower()

    # 🔒 HARD FILTER (fast + precise)
    keyword_match = any(k.lower() in title for k in config.KEYWORDS)

    # 🧠 AI FILTER (semantic understanding)
    model = get_model()
    keyword_embeddings = get_keyword_embeddings()

    job_embedding = model.encode(job_title, convert_to_tensor=True)
    cosine_scores = util.cos_sim(job_embedding, keyword_embeddings)
    max_score = torch.max(cosine_scores).item()

    print(f"[DEBUG] '{job_title}' → Score: {max_score:.4f} | Keyword: {keyword_match}")

    # 🎯 Final decision
    return (
    max_score >= config.SIMILARITY_THRESHOLD
    and any(word in job_title.lower() for word in ["security", "monitor", "soc", "threat"])
)