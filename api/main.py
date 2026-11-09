import sqlite3
import time
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent.runtime import AgentRuntime
from agent.planner import LLMPlanner
from evals.runner import ComprehensiveEvaluationRunner
from storage.database import DB_PATH

app = FastAPI(
    title="Agent Reliability Lab (ARL) API",
    description="Production REST API for Agent Execution, Trace Inspection, and Evaluation",
    version="1.0.0",
)


class TaskRequest(BaseModel):
    task: str
    max_steps: Optional[int] = 4


class TaskResponse(BaseModel):
    run_id: str
    status: str
    output: Optional[Any] = None
    error: Optional[str] = None
    steps_taken: int


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/api/v1/run", response_model=TaskResponse)
def run_task(req: TaskRequest):
    """Executes an agent task end-to-end using the local LLM planner and safety harness."""
    try:
        runtime = AgentRuntime(max_steps=req.max_steps or 4)
        planner = LLMPlanner()
        planner.reset()
        result = runtime.execute_task(req.task, planner.plan)
        return TaskResponse(
            run_id=result.run_id,
            status=result.status,
            output=result.output,
            error=result.error,
            steps_taken=result.steps_taken,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@app.get("/api/v1/runs")
def get_runs(limit: int = 50):
    """Retrieves execution run histories from SQLite persistence."""
    try:
        with sqlite3.connect(DB_PATH, timeout=10.0) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT run_id, task, status, output, error, steps_taken, created_at FROM runs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
            return {"runs": [dict(row) for row in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/v1/runs/{run_id}/trace")
def get_run_trace(run_id: str):
    """Retrieves step-by-step trace events for a specific execution run."""
    try:
        with sqlite3.connect(DB_PATH, timeout=10.0) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT event_id, step, event_type, payload, timestamp FROM trace_events WHERE run_id = ? ORDER BY step ASC, timestamp ASC",
                (run_id,),
            )
            rows = cursor.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="Run trace not found")
            return {"run_id": run_id, "events": [dict(row) for row in rows]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/v1/evaluate")
def trigger_evaluation(dataset: str = "evals/datasets/development.jsonl"):
    """Triggers an evaluation benchmark run across specified dataset."""
    try:
        runner = ComprehensiveEvaluationRunner(dataset_path=dataset)
        report = runner.run_evaluations(use_llm_judge=False)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")