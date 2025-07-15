from typing import List, Tuple
from langchain.docstore.document import Document
from models.user_profile import UserProfile

# tunable weights
ALPHA = 0.6  # similarity
BETA = 0.3   # role match
GAMMA = 0.1  # interest overlap


def _role_match(chunk_meta: dict, role: str) -> float:
    return 1.0 if role in chunk_meta.get("audience", []) else 0.0


def _interest_overlap(chunk_meta: dict, interests: List[str]) -> float:
    chunk_topics = set(chunk_meta.get("topics", []))
    if not chunk_topics or not interests:
        return 0.0
    overlap = chunk_topics.intersection(interests)
    union = chunk_topics.union(interests)
    return len(overlap) / len(union)


def rank(
    candidates: List[Tuple[Document, float]],
    profile: UserProfile,
    top_k: int = 6,
) -> List[Tuple[Document, float]]:
    """
    Re-sorts (Document, similarity_score) using blended metric.
    Returns top_k tuples.
    """
    scored = []
    for doc, sim in candidates:
        meta = doc.metadata or {}
        score = (
            ALPHA * sim
            + BETA * _role_match(meta, profile.role)
            + GAMMA * _interest_overlap(meta, profile.interests)
        )
        scored.append((doc, score))

    scored.sort(key=lambda tup: tup[1], reverse=True)
    return scored[:top_k]
