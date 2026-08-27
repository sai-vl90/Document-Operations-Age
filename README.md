# Document Operations Agent

A modular, agentic document-processing platform built with **Python 3.12**
and **LangGraph**. It accepts a task (e.g. "extract risks", "summarize this
document") plus text or a document path, decides which internal tools to
run, executes them in the required order, and returns a single structured
JSON response.

It is designed to run locally during development and later be deployed
through the **aXet.flows Python Agent node**, using either:

- Local Directory (CWD)
- Git Repository

## Architecture

```
Incoming Request
       ↓
Request Validation (Pydantic)
       ↓
Agent Planner (intent + tool selection)
       ↓
Router (LangGraph conditional edges)
       ↓
Selected Tools (executed in sequence)
       ↓
Result Synthesizer
       ↓
Structured JSON Response
```

The agent does not run a fixed pipeline. The planner decides a task-specific
sequence of tools (`selected_tools`), and the graph dispatches through that
sequence one tool at a time until nothing is left, then synthesizes the
final response.

## Project layout

```
document-ops-agent/
├── main.py            # aXet.flows entrypoint: handle_message(msg, node_id)
├── agent/              # LangGraph state, planner, router, synthesizer, graph
├── tools/               # Deterministic document-intelligence tools
├── services/            # Chunking, vector store, document loading, LLM stub
├── models/              # Pydantic request/response models + shared enums
├── utils/               # Text utilities and logging
├── tests/               # Unit tests
└── data/                # Local sample documents (gitignored)
```

## Local development

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the local smoke test:

```powershell
python main.py
```

Run the unit tests:

```powershell
pytest
```

## Supported tasks

Summarization, risk extraction, action-item extraction, keyword extraction,
document classification, question answering over a document, follow-up
question generation, relevant-section retrieval, document comparison, and
full structured reports. See `agent/planner.py` for the exact routing rules.

## Message format

Input:

```json
{
  "payload": {
    "task": "extract risks",
    "text": "Document contents..."
  }
}
```

Output:

```json
{
  "payload": {
    "success": true,
    "intent": "risk_analysis",
    "tools_used": ["document_loader", "chunk_document", "extract_risks"],
    "result": { "risks": [] },
    "error": null,
    "node_id": "local-test"
  }
}
```

## Roadmap (Phase 7)

Once deployed via Git Repository and the aXet LLM is enabled, deterministic
components (intent detection, summarization, risk reasoning, action-item
extraction, question answering, synthesis) can be swapped for LLM-backed
implementations, while document loading, chunking, embeddings, vector
search and validation remain deterministic.
