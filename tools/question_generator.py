from .keywords import extract_keywords
from utils.text_utils import split_sentences

_TEMPLATES = [
    "What are the implications of {kw} discussed in this document?",
    "How is {kw} addressed or defined in this document?",
    "What obligations or requirements relate to {kw}?",
    "Are there any risks associated with {kw}?",
    "Who is responsible for {kw} according to this document?",
]


def generate_questions(text: str, num_questions: int = 5) -> list[str]:
    """Deterministic follow-up question generation based on top keywords."""

    keywords = extract_keywords(text, top_n=num_questions)

    if not keywords:
        sentences = split_sentences(text)[:num_questions]
        return [f"Can you clarify: '{s}'?" for s in sentences]

    questions = []
    for i, item in enumerate(keywords[:num_questions]):
        template = _TEMPLATES[i % len(_TEMPLATES)]
        questions.append(template.format(kw=item["keyword"]))

    return questions
