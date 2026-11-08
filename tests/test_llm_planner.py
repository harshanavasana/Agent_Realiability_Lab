import pytest
from agent.model import OllamaClient
from agent.planner import LLMPlanner
from agent.runtime import AgentRuntime


def test_ollama_client_connection():
    """Verify raw HTTP connection to local Ollama API."""
    client = OllamaClient()
    messages = [{"role": "user", "content": 'Respond strictly with JSON: {"status": "ok"}'}]
    response = client.generate_completion(messages)
    assert "status" in response


def test_llm_planner_search_task():
    """Verify LLMPlanner returns a structured Action for search tasks."""
    planner = LLMPlanner()
    action = planner.plan("Search for artificial intelligence documents", step=1)
    
    assert action is not None
    assert action.tool_name == "search_documents"
    assert "query" in action.tool_input


def test_full_llm_runtime_execution():
    """Verify AgentRuntime executes tasks end-to-end driven by local Qwen 2.5."""
    runtime = AgentRuntime(max_steps=3)
    planner = LLMPlanner()

    result = runtime.execute_task(
        "Search for artificial intelligence documents",
        planner.plan
    )

    assert result.status == "SUCCESS"
    assert result.output is not None
    assert "artificial intelligence" in result.output.lower()
    assert result.trace.status == "SUCCESS"