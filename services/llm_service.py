from collections import Counter

from utils.text_utils import split_sentences, split_words


class LLMService:
    """Placeholder LLM abstraction.

    Deterministic, dependency-free fallbacks are used so the project runs
    without any external API key. Phase 7 should replace these methods with
    real calls to the aXet LLM while keeping the same interface.
    """

    def generate(self, prompt: str) -> str:
        return (
            "LLM integration is not yet configured. "
            "This is a deterministic placeholder response."
        )

    def summarize(self, text: str, max_sentences: int = 5) -> str:
        """Extractive summary: pick the highest word-frequency-scored sentences."""

        sentences = split_sentences(text)

        if not sentences:
            return ""

        if len(sentences) <= max_sentences:
            return " ".join(sentences)

        word_freq = Counter(split_words(text))

        scored = []
        for sentence in sentences:
            words = split_words(sentence)
            score = sum(word_freq.get(w, 0) for w in words) / max(len(words), 1)
            scored.append((score, sentence))

        top_sentences = sorted(scored, key=lambda s: s[0], reverse=True)[:max_sentences]

        # Preserve original document order in the final summary.
        top_set = {s for _, s in top_sentences}
        ordered = [s for s in sentences if s in top_set]

        return " ".join(ordered)
