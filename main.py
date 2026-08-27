import os
import sys

# Ensure this file's directory (the repo root) is importable regardless of
# the working directory the Python Agent node invokes this entrypoint from.
_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from pydantic import ValidationError

from agent.graph import get_agent_graph
from models.request import AgentRequest
from utils.logging_utils import get_logger

logger = get_logger(__name__)

_graph = None


def get_graph():
    global _graph

    if _graph is None:
        _graph = get_agent_graph()

    return _graph


def handle_message(msg: dict, node_id: str) -> dict:
    """Entrypoint used by the aXet.flows Python Agent node.

    Accepts a message with a 'payload' dict containing at least 'task' and
    either 'text' or 'document_path', executes the LangGraph agent, and
    returns a structured JSON-serializable response. Does not start a web
    server or perform any I/O outside of what the agent tools require.
    """

    payload = msg.get("payload", {}) or {}
    request_id = payload.get("request_id")

    try:
        request = AgentRequest(
            task=payload.get("task", ""),
            text=payload.get("text"),
            document_path=payload.get("document_path"),
            query=payload.get("query"),
            text_b=payload.get("text_b"),
            document_path_b=payload.get("document_path_b"),
            top_k=payload.get("top_k", 5),
        )
    except ValidationError as exc:
        return {
            "payload": {
                "success": False,
                "node_id": node_id,
                "request_id": request_id,
                "error": str(exc),
            }
        }

    graph = get_graph()

    state = {
        "task": request.task,
        "text": request.text or "",
        "document_path": request.document_path or "",
        "query": request.query or "",
        "text_b": request.text_b or "",
        "document_path_b": request.document_path_b or "",
        "top_k": request.top_k,
    }

    final_state = graph.invoke(state)
    response = final_state.get("response", {})
    response["node_id"] = node_id
    response["request_id"] = request_id

    return {"payload": response}


if __name__ == "__main__":
    test_msg = {
        "payload": {
            "task": "extract keywords",
            "text": """
            Python applications can perform document analysis.
            Python can extract keywords and process documents.
            Agentic workflows can dynamically select tools.
            """,
        }
    }

    response = handle_message(test_msg, "local-test")

    print(response)
