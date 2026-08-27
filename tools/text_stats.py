from typing import Any

from utils.text_utils import split_paragraphs, split_sentences, split_words


def compute_text_stats(text: str) -> dict[str, Any]:
    """Compute basic descriptive statistics for a piece of text."""

    text = text or ""

    characters = len(text)
    characters_without_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))

    words = split_words(text)
    word_count = len(words)
    unique_words = len(set(words))

    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)

    average_word_length = (
        round(sum(len(w) for w in words) / word_count, 2) if word_count else 0.0
    )

    return {
        "characters": characters,
        "characters_without_spaces": characters_without_spaces,
        "words": word_count,
        "unique_words": unique_words,
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "average_word_length": average_word_length,
    }
