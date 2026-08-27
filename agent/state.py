from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    task: str
    text: str
    document_path: str

    # Optional inputs for question answering / comparison.
    query: str
    text_b: str
    document_path_b: str
    top_k: int

    intent: str
    selected_tools: list[str]
    tools_used: list[str]

    chunks: list[str]

    analysis: dict[str, Any]
    retrieved_chunks: list[str]

    risks: list[dict]
    action_items: list[dict]

    final_answer: str
    response: dict[str, Any]
    errors: list[str]
