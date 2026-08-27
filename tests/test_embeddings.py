import pytest


def test_embedding_service_returns_vector():
    try:
        from tools.embeddings import EmbeddingService

        service = EmbeddingService()
        vector = service.embed("This is a test sentence.")
    except Exception as exc:  # model download / offline environments
        pytest.skip(f"Embedding model unavailable in this environment: {exc}")
        return

    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(v, float) for v in vector)


def test_embedding_service_is_singleton():
    from tools.embeddings import EmbeddingService

    assert EmbeddingService() is EmbeddingService()
