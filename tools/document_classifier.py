from utils.text_utils import split_words

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "contract": ["agreement", "party", "parties", "clause", "termination", "obligations", "contract", "hereby", "governing law"],
    "technical": ["api", "system", "architecture", "server", "database", "algorithm", "software", "configuration", "deployment"],
    "financial": ["revenue", "budget", "invoice", "payment", "expense", "profit", "financial", "cost", "audit", "tax"],
    "policy": ["policy", "compliance", "regulation", "guideline", "procedure", "standard", "governance"],
    "proposal": ["proposal", "scope", "timeline", "deliverable", "quote", "estimate", "objective"],
    "report": ["report", "summary", "findings", "analysis", "results", "conclusion", "quarter"],
    "meeting_notes": ["meeting", "attendees", "agenda", "minutes", "action items", "discussed", "follow-up"],
}


def classify_document(text: str) -> dict:
    """Deterministic keyword-scoring document classifier."""

    words = split_words(text)
    text_lower = text.lower() if text else ""
    total_words = max(len(words), 1)

    scores: dict[str, float] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(text_lower.count(kw) for kw in keywords)
        scores[category] = round(hits / total_words * 100, 3)

    if all(v == 0 for v in scores.values()):
        best_category = "general"
    else:
        best_category = max(scores, key=scores.get)

    scores["general"] = scores.get("general", 0.0)

    return {
        "category": best_category,
        "scores": scores,
    }
