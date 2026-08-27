from tools.document_loader import DocumentLoader
from utils.text_utils import clean_text


class DocumentService:
    """Resolves the source text for a request, from raw text or a file path."""

    def __init__(self) -> None:
        self._loader = DocumentLoader()

    def get_text(self, text: str | None, document_path: str | None) -> str:
        if text:
            return clean_text(text)

        if document_path:
            raw = self._loader.load(document_path)
            return clean_text(raw)

        raise ValueError("Either 'text' or 'document_path' must be provided.")
