import json
import os
import time
from typing import Any, Dict, List
from agent.runtime import AgentRuntime
from agent.planner import LLMPlanner
from evals.graders import TaskResultGrader, ToolSelectionGrader, GroundednessGrader, BudgetComplianceGrader
from evals.metrics import MetricCalculator


class EvaluationRunner:
    def __init__(self, dataset_path: str = "evals/datasets/development.jsonl", reports_dir: str = "reports"):
        self.dataset_path = dataset_path
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def run_evaluations(self) -> Dict[str, Any]:
        runtime = AgentRuntime(max_steps=4)
        planner = LLMPlanner()
        results: List[Dict[str, Any]] = []
        latencies: List[float] = []

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]

        for case in cases:
            case_id = case["case_id"]
            task = case["task"]
            expected_tool = case.get("expected_tool")
            expected_output = case.get("expected_output")
            must_contain = case.get("must_contain", [])

            planner.reset()
            start_t = time.time()
            res = runtime.execute_task(task, planner.plan)
            latency = time.time() - start_t
            latencies.append(latency)

            events_dict = [e.model_dump() for e in res.trace.events]
            task_passed = TaskResultGrader.grade_task_completion(res.status, res.output, expected_output)
            tool_passed = ToolSelectionGrader.grade_tool_selection(events_dict, expected_tool)
            grounded = GroundednessGrader.grade_groundedness(res.output, must_contain)
            budget_passed = BudgetComplianceGrader.grade_budget(res.status, 4, res.steps_taken)

            overall_pass = task_passed and tool_passed and grounded and budget_passed

            results.append({
                "case_id": case_id,
                "category": case.get("category", "general"),
                "task": task,
                "status": res.status,
                "overall_pass": overall_pass,
                "task_correct": task_passed,
                "tool_correct": tool_passed,
                "grounded": grounded,
                "budget_passed": budget_passed,
                "latency_seconds": round(latency, 3),
                "output": res.output,
                "error": res.error,
                "run_id": res.run_id,
            })

        metrics = MetricCalculator.calculate_summary(results, latencies)

        report = {
            "timestamp": time.time(),
            "metrics": metrics,
            "case_results": results,
        }

        report_filename = os.path.join(self.reports_dir, f"eval_report_v3_{int(time.time())}.json")
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\n================ WEEK 3 MODULAR EVALUATION SUMMARY ================")
        print(f"Total Cases     : {metrics['total_cases']}")
        print(f"Pass Rate       : {metrics['pass_rate_pct']}%")
        print(f"Tool Accuracy   : {metrics['tool_accuracy_pct']}%")
        print(f"Groundedness    : {metrics['groundedness_rate_pct']}%")
        print(f"Latency (p50)   : {metrics['latency_p50_seconds']}s")
        print(f"Latency (p95)   : {metrics['latency_p95_seconds']}s")
        print(f"Report Saved    : {report_filename}")
        print(f"===================================================================\n")

        return report


if __name__ == "__main__":
    runner = EvaluationRunner()
    runner.run_evaluations()