from utils.text_utils import split_sentences

RISK_KEYWORDS: dict[str, list[str]] = {
    "schedule": ["delay", "deadline", "late", "overdue"],
    "financial": ["penalty", "penalties", "fine", "cost overrun", "budget"],
    "legal": ["breach", "non-compliance", "noncompliance", "liability", "lawsuit", "litigation"],
    "operational": ["failure", "failures", "outage", "downtime", "dependency", "dependencies"],
    "security": ["security issue", "vulnerability", "data breach", "unauthorized access"],
    "general": ["risk", "limitation", "constraint"],
}

SEVERITY_KEYWORDS = {
    "high": ["critical", "severe", "major", "breach", "lawsuit", "litigation", "unauthorized access"],
    "medium": ["penalty", "penalties", "delay", "failure", "non-compliance", "noncompliance"],
}


def _category_for(sentence_lower: str) -> str:
    for category, keywords in RISK_KEYWORDS.items():
        if category == "general":
            continue
        if any(kw in sentence_lower for kw in keywords):
            return category
    return "general"


def _severity_for(sentence_lower: str) -> str:
    for severity, keywords in SEVERITY_KEYWORDS.items():
        if any(kw in sentence_lower for kw in keywords):
            return severity
    return "low"


def extract_risks(text: str) -> list[dict]:
    """Identify sentences that reference risk-related language."""

    all_keywords = [kw for kws in RISK_KEYWORDS.values() for kw in kws]

    risks = []
    for sentence in split_sentences(text):
        sentence_lower = sentence.lower()
        if any(kw in sentence_lower for kw in all_keywords):
            risks.append(
                {
                    "text": sentence.strip(),
                    "category": _category_for(sentence_lower),
                    "severity": _severity_for(sentence_lower),
                }
            )

    return risks
