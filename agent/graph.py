from typing import Callable

from langgraph.graph import END, START, StateGraph

from .planner import plan
from .router import route_next
from .state import AgentState
from .synthesizer import synthesize
from models.schemas import ALL_TOOL_NAMES, ToolName
from services.chunking import TextChunker
from services.document_service import DocumentService
from services.llm_service import LLMService
from services.vector_store import VectorStore
from tools.action_extractor import extract_actions
from tools.document_classifier import classify_document
from tools.keywords import extract_keywords
from tools.question_generator import generate_questions
from tools.risk_extractor import extract_risks
from tools.text_stats import compute_text_stats
from tools.vector_search import search_chunks
from utils.logging_utils import get_logger

logger = get_logger(__name__)

_document_service = DocumentService()
_chunker = TextChunker()
_llm_service = LLMService()

# Per-run vector stores, keyed by id(state), so the FAISS index does not need
# to live inside the (otherwise plain-data) LangGraph state dict.
_vector_stores: dict[int, VectorStore] = {}


def _advance(state: AgentState, tool_name: str) -> AgentState:
    used = state.setdefault("tools_used", [])
    used.append(tool_name)

    remaining = state.get("selected_tools", [])
    if remaining and remaining[0] == tool_name:
        state["selected_tools"] = remaining[1:]

    return state


def make_node(name: str, fn: Callable[[AgentState], None]) -> Callable[[AgentState], AgentState]:
    def node(state: AgentState) -> AgentState:
        try:
            fn(state)
        except Exception as exc:  # noqa: BLE001 - surfaced in the response, not raised
            logger.exception("Tool '%s' failed", name)
            state.setdefault("errors", []).append(f"{name}: {exc}")
        return _advance(state, name)

    return node


def _planner_node(state: AgentState) -> AgentState:
    plan_result = plan(state.get("task", ""), bool(state.get("query")))
    state["intent"] = plan_result["intent"]
    state["selected_tools"] = list(plan_result["selected_tools"])
    state.setdefault("tools_used", [])
    state.setdefault("errors", [])
    return state


def _fn_document_loader(state: AgentState) -> None:
    text = _document_service.get_text(state.get("text"), state.get("document_path"))
    state["text"] = text


def _fn_chunk_document(state: AgentState) -> None:
    state["chunks"] = _chunker.chunk(state.get("text", ""))


def _fn_text_stats(state: AgentState) -> None:
    stats = compute_text_stats(state.get("text", ""))
    state.setdefault("analysis", {})["text_stats"] = stats


def _fn_extract_keywords(state: AgentState) -> None:
    keywords = extract_keywords(state.get("text", ""))
    state.setdefault("analysis", {})["keywords"] = keywords


def _fn_classify_document(state: AgentState) -> None:
    classification = classify_document(state.get("text", ""))
    state.setdefault("analysis", {})["classification"] = classification


def _fn_extract_risks(state: AgentState) -> None:
    state["risks"] = extract_risks(state.get("text", ""))


def _fn_extract_actions(state: AgentState) -> None:
    state["action_items"] = extract_actions(state.get("text", ""))


def _fn_embed_chunks(state: AgentState) -> None:
    chunks = state.get("chunks") or [state.get("text", "")]
    store = VectorStore()
    store.add(chunks)
    _vector_stores[id(state)] = store
    state.setdefault("analysis", {})["embedded_chunks"] = len(chunks)


def _fn_vector_search(state: AgentState) -> None:
    store = _vector_stores.get(id(state))
    query = state.get("query") or state.get("task", "")
    top_k = state.get("top_k") or 5
    state["retrieved_chunks"] = search_chunks(store, query, top_k=top_k)


def _fn_answer_question(state: AgentState) -> None:
    retrieved = state.get("retrieved_chunks") or []
    if retrieved:
        state["final_answer"] = "\n\n".join(retrieved)
    else:
        state["final_answer"] = "No relevant information was found in the document."


def _fn_generate_questions(state: AgentState) -> None:
    questions = generate_questions(state.get("text", ""))
    state.setdefault("analysis", {})["generated_questions"] = questions


def _fn_generate_summary(state: AgentState) -> None:
    summary = _llm_service.summarize(state.get("text", ""))
    state["final_answer"] = summary
    state.setdefault("analysis", {})["summary"] = summary


def _fn_compare_documents(state: AgentState) -> None:
    text_a = state.get("text", "")
    text_b = _document_service.get_text(state.get("text_b"), state.get("document_path_b"))

    stats_a = compute_text_stats(text_a)
    stats_b = compute_text_stats(text_b)

    keywords_a = {k["keyword"] for k in extract_keywords(text_a)}
    keywords_b = {k["keyword"] for k in extract_keywords(text_b)}

    state.setdefault("analysis", {})["comparison"] = {
        "text_stats_a": stats_a,
        "text_stats_b": stats_b,
        "shared_keywords": sorted(keywords_a & keywords_b),
        "unique_to_a": sorted(keywords_a - keywords_b),
        "unique_to_b": sorted(keywords_b - keywords_a),
    }


_TOOL_FUNCTIONS: dict[str, Callable[[AgentState], None]] = {
    ToolName.DOCUMENT_LOADER.value: _fn_document_loader,
    ToolName.CHUNK_DOCUMENT.value: _fn_chunk_document,
    ToolName.TEXT_STATS.value: _fn_text_stats,
    ToolName.EXTRACT_KEYWORDS.value: _fn_extract_keywords,
    ToolName.CLASSIFY_DOCUMENT.value: _fn_classify_document,
    ToolName.EXTRACT_RISKS.value: _fn_extract_risks,
    ToolName.EXTRACT_ACTIONS.value: _fn_extract_actions,
    ToolName.EMBED_CHUNKS.value: _fn_embed_chunks,
    ToolName.VECTOR_SEARCH.value: _fn_vector_search,
    ToolName.ANSWER_QUESTION.value: _fn_answer_question,
    ToolName.GENERATE_QUESTIONS.value: _fn_generate_questions,
    ToolName.GENERATE_SUMMARY.value: _fn_generate_summary,
    ToolName.COMPARE_DOCUMENTS.value: _fn_compare_documents,
}


def _synthesizer_node(state: AgentState) -> AgentState:
    state["response"] = synthesize(state)
    _vector_stores.pop(id(state), None)
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", _planner_node)
    for tool_name, fn in _TOOL_FUNCTIONS.items():
        graph.add_node(tool_name, make_node(tool_name, fn))
    graph.add_node("synthesizer", _synthesizer_node)

    graph.add_edge(START, "planner")

    routing_map = {name: name for name in ALL_TOOL_NAMES}
    routing_map["synthesizer"] = "synthesizer"

    graph.add_conditional_edges("planner", route_next, routing_map)
    for tool_name in _TOOL_FUNCTIONS:
        graph.add_conditional_edges(tool_name, route_next, routing_map)

    graph.add_edge("synthesizer", END)

    return graph.compile()


_compiled_graph = None


def get_agent_graph():
    """Return a cached, compiled instance of the agent graph."""

    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
