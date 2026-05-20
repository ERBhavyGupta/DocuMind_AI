from database import get_collection
from embeddings import embed_texts, embed_query

def store_chunks(chunks: list[str], doc_name: str):
    """
    Save all chunks of a document into ChromaDB.
    Each chunk gets: an ID, its vector, and the original text as metadata.
    """
    collection = get_collection()
    embeddings = embed_texts(chunks)  # Generate vectors for all chunks

    ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,                   # Original text (for retrieval)
        metadatas=[{"source": doc_name}] * len(chunks)
    )
    print(f"Stored {len(chunks)} chunks from '{doc_name}'")


def retrieve_relevant_chunks(query: str, top_k: int = 5) -> list[str]:
    """
    Find the most relevant document chunks for a user's question.
    
    HOW IT WORKS:
    1. Convert query to a vector
    2. Measure cosine similarity against ALL stored vectors
    3. Return the top_k closest matches
    
    Cosine similarity = how similar the DIRECTION of two vectors is.
    Score of 1.0 = identical meaning, 0.0 = completely unrelated.
    """
    collection = get_collection()
    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # results["documents"][0] is a list of the top matching chunks
    chunks = results["documents"][0]
    return chunks