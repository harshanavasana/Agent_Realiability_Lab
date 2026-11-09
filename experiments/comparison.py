import json
import time
from typing import Any, Dict, List
from agent.runtime import AgentRuntime
from agent.planner import LLMPlanner
from evals.graders import TaskResultGrader, ToolSelectionGrader
from evals.metrics import MetricCalculator


class HarnessComparator:
    def __init__(self, dataset_path: str = "evals/datasets/development.jsonl"):
        self.dataset_path = dataset_path

    def compare_configurations(
        self, baseline_max_steps: int = 2, candidate_max_steps: int = 5
    ) -> Dict[str, Any]:
        """Runs evaluation benchmark across two harness configurations to measure deltas."""
        baseline_metrics = self._run_config(baseline_max_steps)
        candidate_metrics = self._run_config(candidate_max_steps)

        delta_pass_rate = round(candidate_metrics["pass_rate_pct"] - baseline_metrics["pass_rate_pct"], 2)
        delta_tool_acc = round(candidate_metrics["tool_accuracy_pct"] - baseline_metrics["tool_accuracy_pct"], 2)

        return {
            "timestamp": time.time(),
            "baseline": baseline_metrics,
            "candidate": candidate_metrics,
            "deltas": {
                "pass_rate_delta_pct": delta_pass_rate,
                "tool_accuracy_delta_pct": delta_tool_acc,
                "improved": delta_pass_rate >= 0.0,
            },
        }

    def _run_config(self, max_steps: int) -> Dict[str, Any]:
        runtime = AgentRuntime(max_steps=max_steps)
        planner = LLMPlanner()
        results: List[Dict[str, Any]] = []
        latencies: List[float] = []

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]

        for case in cases:
            planner.reset()
            start_t = time.time()
            res = runtime.execute_task(case["task"], planner.plan)
            latency = time.time() - start_t
            latencies.append(latency)

            events = [e.model_dump() for e in res.trace.events]
            task_passed = TaskResultGrader.grade_task_completion(res.status, res.output, case.get("expected_output"))
            tool_passed = ToolSelectionGrader.grade_tool_selection(events, case.get("expected_tool"))
            overall = task_passed and tool_passed

            results.append({
                "overall_pass": overall,
                "task_correct": task_passed,
                "tool_correct": tool_passed,
                "grounded": True,
            })

        return MetricCalculator.calculate_summary(results, latencies)