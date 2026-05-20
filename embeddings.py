from sentence_transformers import SentenceTransformer
import numpy as np

# Load once at startup — this is your "understanding" model
# It converts any text into a list of 384 numbers (a vector)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert text into vectors (embeddings).
    
    HOW IT WORKS:
    "The cat sat on the mat"  →  [0.23, -0.11, 0.87, ... 384 numbers]
    "A feline rested on a rug" →  [0.24, -0.10, 0.85, ... 384 numbers]
    
    These two sentences have SIMILAR vectors because they mean the same thing!
    This is what makes semantic search possible.
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    """Embed a single search query."""
    return embed_texts([query])[0]