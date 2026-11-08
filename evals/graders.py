from typing import Any, Dict, Optional


class TaskResultGrader:
    @staticmethod
    def grade_task_completion(status: str, actual_output: Optional[str], expected_output: Optional[str]) -> bool:
        if expected_output is None:
            # Task was expected to fail or hit security policies safely
            return status in ["FAILED", "REJECTED"]
        if status != "SUCCESS":
            return False
        return actual_output == expected_output

    @staticmethod
    def grade_tool_usage(events: list[Dict[str, Any]], expected_tool: Optional[str]) -> bool:
        executed_tools = [
            e["payload"]["tool_name"] for e in events if e.get("event_type") == "TOOL_EXECUTION_SUCCESS"
        ]
        if expected_tool is None:
            # Expected no successful tool executions
            return len(executed_tools) == 0
        return expected_tool in executed_tools