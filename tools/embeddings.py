from utils.logging_utils import get_logger

logger = get_logger(__name__)

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """Lazy-loaded, process-wide singleton wrapper around SentenceTransformer."""

    _instance: "EmbeddingService | None" = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info("Loading embedding model %s", _MODEL_NAME)
            self._model = SentenceTransformer(_MODEL_NAME)
        return self._model

    def embed(self, text: str) -> list[float]:
        model = self._ensure_model()
        vector = model.encode(text)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        model = self._ensure_model()
        vectors = model.encode(texts)
        return [v.tolist() for v in vectors]
