import time
from typing import Any, Dict, Optional
from pydantic import BaseModel
from agent.tools import get_tool
from agent.traces import RunTrace


class Action(BaseModel):
    tool_name: str
    tool_input: Dict[str, Any]


class RunResult(BaseModel):
    run_id: str
    status: str
    output: Optional[Any] = None
    error: Optional[str] = None
    steps_taken: int
    trace: RunTrace


class AgentRuntime:
    def __init__(self, max_steps: int = 5, timeout_seconds: float = 30.0):
        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds

    def execute_task(self, task: str, planner_fn) -> RunResult:
        trace = RunTrace(task=task, max_steps=self.max_steps)
        start_time = time.time()
        step = 0
        final_output = None

        trace.log_event(step=0, event_type="RUN_STARTED", payload={"task": task, "max_steps": self.max_steps})

        while step < self.max_steps:
            elapsed = time.time() - start_time
            if elapsed > self.timeout_seconds:
                trace.status = "TIMEOUT"
                trace.end_time = time.time()
                trace.log_event(step=step, event_type="RUN_TIMEOUT", payload={"elapsed_seconds": elapsed})
                return RunResult(
                    run_id=trace.run_id,
                    status="TIMEOUT",
                    error=f"Execution timed out after {elapsed:.2f}s",
                    steps_taken=step,
                    trace=trace,
                )

            step += 1
            trace.total_steps = step

            try:
                action: Optional[Action] = planner_fn(task, step)
            except Exception as e:
                trace.status = "FAILED"
                trace.end_time = time.time()
                trace.log_event(step=step, event_type="PLANNER_ERROR", payload={"error": str(e)})
                return RunResult(
                    run_id=trace.run_id,
                    status="FAILED",
                    error=f"Planner error: {str(e)}",
                    steps_taken=step,
                    trace=trace,
                )

            if action is None:
                trace.status = "SUCCESS"
                trace.end_time = time.time()
                trace.log_event(step=step, event_type="RUN_COMPLETE", payload={"result": final_output})
                return RunResult(
                    run_id=trace.run_id,
                    status="SUCCESS",
                    output=final_output,
                    steps_taken=step - 1,
                    trace=trace,
                )

            trace.log_event(
                step=step,
                event_type="PLANNER_DECISION",
                payload={"tool_name": action.tool_name, "tool_input": action.tool_input},
            )

            try:
                tool = get_tool(action.tool_name)
                tool_result = tool.execute(action.tool_input)
                final_output = tool_result.result

                trace.log_event(
                    step=step,
                    event_type="TOOL_EXECUTION_SUCCESS",
                    payload={"tool_name": action.tool_name, "result": tool_result.result},
                )
            except Exception as e:
                trace.log_event(
                    step=step,
                    event_type="TOOL_EXECUTION_FAILED",
                    payload={"tool_name": action.tool_name, "error": str(e)},
                )
                trace.status = "FAILED"
                trace.end_time = time.time()
                return RunResult(
                    run_id=trace.run_id,
                    status="FAILED",
                    error=str(e),
                    steps_taken=step,
                    trace=trace,
                )

        trace.status = "MAX_STEPS_EXCEEDED"
        trace.end_time = time.time()
        trace.log_event(step=step, event_type="MAX_STEPS_REACHED", payload={"max_steps": self.max_steps})
        return RunResult(
            run_id=trace.run_id,
            status="MAX_STEPS_EXCEEDED",
            error=f"Exceeded maximum allowed steps ({self.max_steps})",
            steps_taken=step,
            trace=trace,
        )