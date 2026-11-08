from typing import Any, Dict
from agent.tools import Tool, ToolResult

class FlakyTool(Tool):
    """Wrapper that injects failures based on call counts."""
    fail_on_steps: list[int]
    current_step: int = 0

    def execute(self, tool_input: Dict[str, Any]) -> ToolResult:
        self.current_step += 1
        if self.current_step in self.fail_on_steps:
            raise RuntimeError(f"Simulated fault: Tool failure on step {self.current_step}")
        return super().execute(tool_input)