import re

from utils.text_utils import split_sentences

ACTION_PATTERNS = [
    r"\bmust\b",
    r"\bshould\b",
    r"\brequired to\b",
    r"\bneed to\b",
    r"\bneeds to\b",
    r"\bresponsible for\b",
    r"\bshall\b",
    r"\baction item\b",
    r"\bfollow up\b",
    r"\bfollow-up\b",
]

_ACTION_RE = re.compile("|".join(ACTION_PATTERNS), re.IGNORECASE)


def extract_actions(text: str) -> list[dict]:
    """Identify sentences that look like action items / obligations."""

    actions = []
    for sentence in split_sentences(text):
        if _ACTION_RE.search(sentence):
            actions.append(
                {
                    "action": sentence.strip(),
                    "owner": None,
                    "deadline": None,
                }
            )

    return actions
