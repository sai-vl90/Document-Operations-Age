import re

_WHITESPACE_RE = re.compile(r"[ \t\f\v]+")
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph breaks."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WHITESPACE_RE.sub(" ", text)
    text = _MULTI_NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    sentences = _SENTENCE_SPLIT_RE.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]


def split_paragraphs(text: str) -> list[str]:
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split("\n\n")]
    return [p for p in paragraphs if p]


def split_words(text: str) -> list[str]:
    if not text:
        return []
    return _WORD_RE.findall(text.lower())
