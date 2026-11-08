import time
from typing import Any, Dict, Optional
from pydantic import BaseModel
from agent.tools import get_tool
from agent.traces import RunTrace
from observability.logging import get_logger
from observability.telemetry import get_tracer
from storage.repository import RunRepository

logger = get_logger("agent.runtime")
tracer = get_tracer()
repo = RunRepository()


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
        with tracer.start_as_current_span("agent_run") as parent_span:
            parent_span.set_attribute("task", task)
            trace_obj = RunTrace(task=task, max_steps=self.max_steps)
            start_time = time.time()
            step = 0
            final_output = None

            logger.info(f"Starting task execution: {task}", extra={"payload": {"task": task}})
            trace_obj.log_event(step=0, event_type="RUN_STARTED", payload={"task": task, "max_steps": self.max_steps})

            while step < self.max_steps:
                elapsed = time.time() - start_time
                if elapsed > self.timeout_seconds:
                    trace_obj.status = "TIMEOUT"
                    trace_obj.end_time = time.time()
                    trace_obj.log_event(step=step, event_type="RUN_TIMEOUT", payload={"elapsed": elapsed})
                    res = RunResult(
                        run_id=trace_obj.run_id,
                        status="TIMEOUT",
                        error=f"Execution timed out after {elapsed:.2f}s",
                        steps_taken=step,
                        trace=trace_obj,
                    )
                    repo.save_run(res)
                    return res

                step += 1
                trace_obj.total_steps = step

                with tracer.start_as_current_span(f"step_{step}") as step_span:
                    step_span.set_attribute("step", step)
                    try:
                        action: Optional[Action] = planner_fn(task, step)
                    except Exception as e:
                        trace_obj.status = "FAILED"
                        trace_obj.end_time = time.time()
                        trace_obj.log_event(step=step, event_type="PLANNER_ERROR", payload={"error": str(e)})
                        res = RunResult(
                            run_id=trace_obj.run_id,
                            status="FAILED",
                            error=f"Planner error: {str(e)}",
                            steps_taken=step,
                            trace=trace_obj,
                        )
                        repo.save_run(res)
                        return res

                    if action is None:
                        trace_obj.status = "SUCCESS"
                        trace_obj.end_time = time.time()
                        trace_obj.log_event(step=step, event_type="RUN_COMPLETE", payload={"result": final_output})
                        res = RunResult(
                            run_id=trace_obj.run_id,
                            status="SUCCESS",
                            output=final_output,
                            steps_taken=step - 1,
                            trace=trace_obj,
                        )
                        repo.save_run(res)
                        return res

                    trace_obj.log_event(
                        step=step,
                        event_type="PLANNER_DECISION",
                        payload={"tool_name": action.tool_name, "tool_input": action.tool_input},
                    )

                    try:
                        tool = get_tool(action.tool_name)
                        tool_result = tool.execute(action.tool_input)
                        final_output = tool_result.result

                        trace_obj.log_event(
                            step=step,
                            event_type="TOOL_EXECUTION_SUCCESS",
                            payload={"tool_name": action.tool_name, "result": tool_result.result},
                        )
                    except Exception as e:
                        trace_obj.log_event(
                            step=step,
                            event_type="TOOL_EXECUTION_FAILED",
                            payload={"tool_name": action.tool_name, "error": str(e)},
                        )
                        trace_obj.status = "FAILED"
                        trace_obj.end_time = time.time()
                        res = RunResult(
                            run_id=trace_obj.run_id,
                            status="FAILED",
                            error=str(e),
                            steps_taken=step,
                            trace=trace_obj,
                        )
                        repo.save_run(res)
                        return res

            trace_obj.status = "MAX_STEPS_EXCEEDED"
            trace_obj.end_time = time.time()
            trace_obj.log_event(step=step, event_type="MAX_STEPS_REACHED", payload={"max_steps": self.max_steps})
            res = RunResult(
                run_id=trace_obj.run_id,
                status="MAX_STEPS_EXCEEDED",
                error=f"Exceeded maximum allowed steps ({self.max_steps})",
                steps_taken=step,
                trace=trace_obj,
            )
            repo.save_run(res)
            return res