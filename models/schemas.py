"""Shared enums and constants used across the agent and tools."""

from enum import Enum


class Intent(str, Enum):
    SUMMARIZE = "summarize"
    RISK_ANALYSIS = "risk_analysis"
    ACTION_EXTRACTION = "action_extraction"
    KEYWORD_ANALYSIS = "keyword_analysis"
    CLASSIFICATION = "classification"
    DOCUMENT_QA = "document_qa"
    QUESTION_GENERATION = "question_generation"
    SECTION_RETRIEVAL = "section_retrieval"
    COMPARISON = "comparison"
    FULL_REPORT = "full_report"
    TEXT_STATISTICS = "text_statistics"


class ToolName(str, Enum):
    DOCUMENT_LOADER = "document_loader"
    CHUNK_DOCUMENT = "chunk_document"
    TEXT_STATS = "text_stats"
    EXTRACT_KEYWORDS = "extract_keywords"
    CLASSIFY_DOCUMENT = "classify_document"
    EXTRACT_RISKS = "extract_risks"
    EXTRACT_ACTIONS = "extract_actions"
    EMBED_CHUNKS = "embed_chunks"
    VECTOR_SEARCH = "vector_search"
    ANSWER_QUESTION = "answer_question"
    GENERATE_QUESTIONS = "generate_questions"
    GENERATE_SUMMARY = "generate_summary"
    COMPARE_DOCUMENTS = "compare_documents"


# Ordered list of every tool node name known to the graph.
ALL_TOOL_NAMES: list[str] = [t.value for t in ToolName]


DOCUMENT_CATEGORIES: list[str] = [
    "contract",
    "technical",
    "financial",
    "policy",
    "proposal",
    "report",
    "meeting_notes",
    "general",
]
