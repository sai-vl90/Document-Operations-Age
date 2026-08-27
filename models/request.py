from typing import Optional

from pydantic import BaseModel, model_validator


class AgentRequest(BaseModel):
    """Incoming request payload validated before entering the agent graph."""

    task: str

    text: Optional[str] = None
    document_path: Optional[str] = None

    # Optional free-text query, used for question answering / section retrieval.
    query: Optional[str] = None

    # Optional second document, used for comparison tasks.
    text_b: Optional[str] = None
    document_path_b: Optional[str] = None

    top_k: int = 5

    @model_validator(mode="after")
    def _check_source(self) -> "AgentRequest":
        if not self.text and not self.document_path:
            raise ValueError("Either 'text' or 'document_path' must be provided.")
        return self
