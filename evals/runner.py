import json
import os
import time
from typing import Any, Dict, List
from agent.runtime import AgentRuntime
from agent.planner import LLMPlanner
from evals.graders import TaskResultGrader


class EvaluationRunner:
    def __init__(self, dataset_path: str = "evals/dataset.jsonl", reports_dir: str = "reports"):
        self.dataset_path = dataset_path
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def run_evaluations(self) -> Dict[str, Any]:
        runtime = AgentRuntime(max_steps=4)
        planner = LLMPlanner()
        results: List[Dict[str, Any]] = []
        passed_cases = 0

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]

        total_cases = len(cases)

        for case in cases:
            case_id = case["case_id"]
            task = case["task"]
            expected_tool = case.get("expected_tool")
            expected_output = case.get("expected_output")

            # Reset planner memory for each isolated eval case
            planner.reset()

            res = runtime.execute_task(task, planner.plan)

            events_dict = [e.model_dump() for e in res.trace.events]
            task_passed = TaskResultGrader.grade_task_completion(res.status, res.output, expected_output)
            tool_passed = TaskResultGrader.grade_tool_usage(events_dict, expected_tool)
            overall_pass = task_passed and tool_passed

            if overall_pass:
                passed_cases += 1

            results.append({
                "case_id": case_id,
                "category": case.get("category", "general"),
                "task": task,
                "status": res.status,
                "overall_pass": overall_pass,
                "task_correct": task_passed,
                "tool_correct": tool_passed,
                "output": res.output,
                "error": res.error,
                "steps_taken": res.steps_taken,
                "run_id": res.run_id,
            })

        pass_rate = (passed_cases / total_cases * 100) if total_cases > 0 else 0.0

        report = {
            "timestamp": time.time(),
            "total_cases": total_cases,
            "passed_cases": passed_cases,
            "failed_cases": total_cases - passed_cases,
            "pass_rate_pct": round(pass_rate, 2),
            "case_results": results,
        }

        report_filename = os.path.join(self.reports_dir, f"eval_report_llm_{int(time.time())}.json")
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\n================ LLM EVALUATION SUMMARY ================")
        print(f"Total Cases : {total_cases}")
        print(f"Passed      : {passed_cases}")
        print(f"Failed      : {total_cases - passed_cases}")
        print(f"Pass Rate   : {report['pass_rate_pct']}%")
        print(f"Report saved: {report_filename}")
        print(f"========================================================\n")

        return report


if __name__ == "__main__":
    runner = EvaluationRunner()
    runner.run_evaluations()