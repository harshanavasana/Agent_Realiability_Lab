from agent.runtime import AgentRuntime, Action
from harness.policies import check_tool_permission, PermissionLevel
from harness.retries import execute_with_retry


def test_permission_policy_blocking():
    runtime = AgentRuntime(max_steps=2)

    def malicious_planner(task, step):
        return Action(tool_name="delete_database", tool_input={})

    result = runtime.execute_task("Delete db", malicious_planner)
    assert result.status == "FAILED"
    assert "Security Policy Violation" in result.error


def test_retry_mechanism_success():
    attempts = 0

    def flaky_operation():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("Temporary glitch")
        return "SUCCESS"

    result = execute_with_retry(flaky_operation, max_retries=3, initial_delay=0.01)
    assert result == "SUCCESS"
    assert attempts == 2