from collections import Counter

from utils.text_utils import split_sentences, split_words

# Common English stopwords, kept small and dependency-free.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "is", "are", "was",
    "were", "be", "been", "being", "to", "of", "in", "on", "for", "with",
    "as", "by", "at", "from", "that", "this", "these", "those", "it", "its",
    "we", "you", "they", "he", "she", "his", "her", "their", "our", "not",
    "no", "do", "does", "did", "have", "has", "had", "will", "would",
    "shall", "should", "can", "could", "may", "might", "must", "so", "than",
    "such", "into", "about", "which", "who", "whom", "there", "here",
}


def extract_keywords(text: str, top_n: int = 10) -> list[dict]:
    """Deterministic keyword extraction using TF-IDF over document sentences."""

    sentences = split_sentences(text)

    if len(sentences) < 2:
        return _extract_keywords_by_frequency(text, top_n)

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(stop_words="english", lowercase=True)
        matrix = vectorizer.fit_transform(sentences)
        scores = matrix.sum(axis=0).A1
        terms = vectorizer.get_feature_names_out()

        pairs = sorted(zip(terms, scores), key=lambda p: p[1], reverse=True)
        max_score = pairs[0][1] if pairs else 1.0

        results = []
        for term, score in pairs[:top_n]:
            if score <= 0:
                continue
            results.append(
                {"keyword": term, "score": round(float(score / max_score), 2)}
            )
        return results
    except Exception:
        return _extract_keywords_by_frequency(text, top_n)


def _extract_keywords_by_frequency(text: str, top_n: int) -> list[dict]:
    words = [w for w in split_words(text) if w not in STOPWORDS and len(w) > 2]

    if not words:
        return []

    counts = Counter(words)
    max_count = counts.most_common(1)[0][1]

    return [
        {"keyword": word, "score": round(count / max_count, 2)}
        for word, count in counts.most_common(top_n)
    ]
