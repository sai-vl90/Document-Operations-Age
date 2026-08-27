from pathlib import Path

from utils.logging_utils import get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """Loads plain text from .txt, .pdf and .docx files."""

    SUPPORTED_EXTENSIONS = (".txt", ".pdf", ".docx")

    def load(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return self._load_txt(path)
        if suffix == ".pdf":
            return self._load_pdf(path)
        if suffix == ".docx":
            return self._load_docx(path)

        raise ValueError(
            f"Unsupported file type '{suffix}'. Supported: {self.SUPPORTED_EXTENSIONS}"
        )

    def _load_txt(self, path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="ignore")

    def _load_pdf(self, path: Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)

    def _load_docx(self, path: Path) -> str:
        import docx

        document = docx.Document(str(path))
        paragraphs = [p.text for p in document.paragraphs]
        return "\n".join(paragraphs)
