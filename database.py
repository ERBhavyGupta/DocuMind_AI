import chromadb
from chromadb.config import Settings

# ChromaDB stores your documents as vectors on disk
# Think of it like a smart database that understands meaning, not just keywords

client = chromadb.PersistentClient(
    path="./chroma_storage"   # Saves to disk so knowledge persists
)

def get_collection(name: str = "documents"):
    """
    A 'collection' is like a table in a regular DB.
    Each row has: an ID, the original text, and its vector.
    """
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}  # cosine similarity = best for text
    )