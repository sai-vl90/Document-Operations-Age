from typing import Any

from .state import AgentState


def synthesize(state: AgentState) -> dict[str, Any]:
    """Combine tool outputs into the single, consistent response format."""

    errors = state.get("errors") or []

    result: dict[str, Any] = {}

    analysis = state.get("analysis")
    if analysis:
        result["analysis"] = analysis

    risks = state.get("risks")
    if risks is not None:
        result["risks"] = risks

    action_items = state.get("action_items")
    if action_items is not None:
        result["action_items"] = action_items

    retrieved_chunks = state.get("retrieved_chunks")
    if retrieved_chunks is not None:
        result["retrieved_chunks"] = retrieved_chunks

    final_answer = state.get("final_answer")
    if final_answer:
        result["final_answer"] = final_answer

    return {
        "success": len(errors) == 0,
        "intent": state.get("intent"),
        "tools_used": state.get("tools_used", []),
        "result": result,
        "error": "; ".join(errors) if errors else None,
    }
