import numpy as np

from tools.embeddings import EmbeddingService


class VectorStore:
    """In-memory FAISS-backed similarity index over document chunks."""

    def __init__(self) -> None:
        self._index = None
        self._chunks: list[str] = []
        self._embedding_service = EmbeddingService()

    def add(self, chunks: list[str]) -> None:
        import faiss

        if not chunks:
            return

        vectors = np.array(
            self._embedding_service.embed_batch(chunks), dtype="float32"
        )

        dimension = vectors.shape[1]
        if self._index is None:
            self._index = faiss.IndexFlatL2(dimension)

        self._index.add(vectors)
        self._chunks.extend(chunks)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        if self._index is None or not self._chunks:
            return []

        query_vector = np.array(
            [self._embedding_service.embed(query)], dtype="float32"
        )

        top_k = min(top_k, len(self._chunks))
        _distances, indices = self._index.search(query_vector, top_k)

        return [self._chunks[i] for i in indices[0] if i != -1]
