from agent.planner import plan


def test_planner_routes_risk_analysis():
    result = plan("Find the main risks in this document.")

    assert result["intent"] == "risk_analysis"
    assert "extract_risks" in result["selected_tools"]


def test_planner_routes_action_extraction():
    result = plan("Extract all action items.")

    assert result["intent"] == "action_extraction"
    assert "extract_actions" in result["selected_tools"]


def test_planner_routes_keyword_analysis():
    result = plan("Find the five most important keywords.")

    assert result["intent"] == "keyword_analysis"
    assert "extract_keywords" in result["selected_tools"]


def test_planner_routes_default_stats():
    result = plan("")

    assert result["intent"] == "text_statistics"


def test_graph_executes_risk_pipeline():
    from agent.graph import get_agent_graph

    graph = get_agent_graph()

    state = {
        "task": "extract risks",
        "text": (
            "Failure to meet the deadline may result in penalties. "
            "The vendor agrees to deliver the software on time."
        ),
    }

    result = graph.invoke(state)
    response = result["response"]

    assert response["intent"] == "risk_analysis"
    assert "document_loader" in response["tools_used"]
    assert "extract_risks" in response["tools_used"]
    assert response["success"] is True
    assert "risks" in response["result"]


def test_graph_executes_keyword_pipeline():
    from agent.graph import get_agent_graph

    graph = get_agent_graph()

    state = {
        "task": "extract keywords",
        "text": "Python applications can perform document analysis and keyword extraction.",
    }

    result = graph.invoke(state)
    response = result["response"]

    assert response["intent"] == "keyword_analysis"
    assert response["success"] is True
    assert "keywords" in response["result"]["analysis"]
