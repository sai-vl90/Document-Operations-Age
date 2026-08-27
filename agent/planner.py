from models.schemas import Intent, ToolName

L = ToolName


def plan(task: str, has_query: bool = False) -> dict:
    """Deterministic routing: decide the intent and tool pipeline for a task.

    This is intentionally rule-based for the local/offline version of the
    project. Phase 7 should replace or extend this logic with the aXet LLM.
    """

    task_lower = (task or "").lower()

    def has_any(*keywords: str) -> bool:
        return any(kw in task_lower for kw in keywords)

    if has_any("report", "structured report"):
        return {
            "intent": Intent.FULL_REPORT.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.TEXT_STATS.value,
                L.EXTRACT_KEYWORDS.value,
                L.CLASSIFY_DOCUMENT.value,
                L.EXTRACT_RISKS.value,
                L.EXTRACT_ACTIONS.value,
            ],
        }

    if has_any("compare"):
        return {
            "intent": Intent.COMPARISON.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.COMPARE_DOCUMENTS.value,
            ],
        }

    if has_any("risk"):
        return {
            "intent": Intent.RISK_ANALYSIS.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.EXTRACT_RISKS.value,
            ],
        }

    if has_any("action item", "action items", "action point", "to-do", "todo"):
        return {
            "intent": Intent.ACTION_EXTRACTION.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.EXTRACT_ACTIONS.value,
            ],
        }

    if has_any("keyword", "topic", "important terms"):
        return {
            "intent": Intent.KEYWORD_ANALYSIS.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.EXTRACT_KEYWORDS.value,
            ],
        }

    if has_any("classify", "classification", "category", "categorize"):
        return {
            "intent": Intent.CLASSIFICATION.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CLASSIFY_DOCUMENT.value,
            ],
        }

    if has_any("generate question", "follow-up question", "follow up question", "questions i should ask"):
        return {
            "intent": Intent.QUESTION_GENERATION.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.GENERATE_QUESTIONS.value,
            ],
        }

    if has_any("section", "relevant part", "retrieve"):
        return {
            "intent": Intent.SECTION_RETRIEVAL.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.EMBED_CHUNKS.value,
                L.VECTOR_SEARCH.value,
            ],
        }

    if has_query or has_any("question", "answer", "what", "who", "how", "?"):
        return {
            "intent": Intent.DOCUMENT_QA.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.EMBED_CHUNKS.value,
                L.VECTOR_SEARCH.value,
                L.ANSWER_QUESTION.value,
            ],
        }

    if has_any("summar"):
        return {
            "intent": Intent.SUMMARIZE.value,
            "selected_tools": [
                L.DOCUMENT_LOADER.value,
                L.CHUNK_DOCUMENT.value,
                L.GENERATE_SUMMARY.value,
            ],
        }

    return {
        "intent": Intent.TEXT_STATISTICS.value,
        "selected_tools": [
            L.DOCUMENT_LOADER.value,
            L.TEXT_STATS.value,
        ],
    }
