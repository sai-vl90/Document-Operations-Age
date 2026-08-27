from utils.text_utils import split_words


class TextChunker:
    """Splits large documents into overlapping, word-boundary-aware chunks."""

    def chunk(self, text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
        text = (text or "").strip()

        if not text:
            return []

        if len(text) <= chunk_size:
            return [text]

        if overlap >= chunk_size:
            overlap = chunk_size // 4

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)

            # Avoid cutting a word in half, by extending to the next space.
            if end < text_length:
                next_space = text.find(" ", end)
                if next_space != -1 and next_space - end < 50:
                    end = next_space

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - overlap

        return chunks
