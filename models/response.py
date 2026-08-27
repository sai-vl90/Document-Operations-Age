from typing import Any, Optional

from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Structured, top-level response shape returned for every operation."""

    success: bool
    intent: Optional[str] = None

    tools_used: list[str] = []

    result: dict[str, Any] = {}

    error: Optional[str] = None
