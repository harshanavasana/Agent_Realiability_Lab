from typing import Any, Dict, List, Optional


class TaskResultGrader:
    @staticmethod
    def grade_task_completion(status: str, actual_output: Optional[str], expected_output: Optional[str]) -> bool:
        if expected_output is None:
            return status in ["FAILED", "REJECTED"]
        if status != "SUCCESS":
            return False
        return actual_output == expected_output


class ToolSelectionGrader:
    @staticmethod
    def grade_tool_selection(events: List[Dict[str, Any]], expected_tool: Optional[str]) -> bool:
        executed_tools = [
            e["payload"]["tool_name"] for e in events if e.get("event_type") == "TOOL_EXECUTION_SUCCESS"
        ]
        if expected_tool is None:
            return len(executed_tools) == 0
        return expected_tool in executed_tools


class GroundednessGrader:
    @staticmethod
    def grade_groundedness(output: Optional[str], must_contain: List[str]) -> bool:
        if output is None:
            return True if not must_contain else False
        output_lower = output.lower()
        return all(phrase.lower() in output_lower for phrase in must_contain)


class BudgetComplianceGrader:
    @staticmethod
    def grade_budget(status: str, max_steps: int, actual_steps: int) -> bool:
        return status != "MAX_STEPS_EXCEEDED" and actual_steps <= max_steps