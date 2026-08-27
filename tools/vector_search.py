from services.vector_store import VectorStore


def build_vector_index(chunks: list[str]) -> VectorStore:
    """Build an in-memory FAISS-backed vector store from document chunks."""

    store = VectorStore()
    store.add(chunks)
    return store


def search_chunks(store: VectorStore, query: str, top_k: int = 5) -> list[str]:
    """Return the top_k chunks most similar to the query."""

    if store is None:
        return []

    return store.search(query, top_k=top_k)
