import importlib.metadata
import sys

def get_version(package_name):
    try:
        return importlib.metadata.version(package_name)
    except Exception as exc:
        return f"NOT FOUND: {exc}"

def handle_message(msg, node_id):
    checks = {}

    try:
        import langsmith
        checks["langsmith_import"] = "OK"
        checks["langsmith_file"] = langsmith.__file__
    except Exception as exc:
        checks["langsmith_import"] = f"FAILED: {exc}"

    try:
        import langchain_core
        checks["langchain_core_import"] = "OK"
        checks["langchain_core_file"] = langchain_core.__file__
    except Exception as exc:
        checks["langchain_core_import"] = f"FAILED: {exc}"

    try:
        from langsmith._openapi_client.types import (
            annotation_queue_rubric_item_schema_param
        )
        checks["missing_langsmith_module"] = "OK"
    except Exception as exc:
        checks["missing_langsmith_module"] = f"FAILED: {exc}"

    return {
        "payload": {
            "success": True,
            "node_id": node_id,
            "python": sys.version,
            "versions": {
                "langgraph": get_version("langgraph"),
                "langchain": get_version("langchain"),
                "langchain-core": get_version("langchain-core"),
                "langsmith": get_version("langsmith"),
                "pydantic": get_version("pydantic")
            },
            "checks": checks
        }
    }
