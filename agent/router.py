from .state import AgentState


def route_next(state: AgentState) -> str:
    """Return the name of the next node to execute, or 'synthesizer' if done."""

    remaining = state.get("selected_tools") or []

    if not remaining:
        return "synthesizer"

    return remaining[0]
