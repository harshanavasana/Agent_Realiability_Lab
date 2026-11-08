from typing import Any, Dict, List


class MetricCalculator:
    @staticmethod
    def calculate_summary(results: List[Dict[str, Any]], latencies: List[float]) -> Dict[str, Any]:
        total = len(results)
        if total == 0:
            return {}

        passed = sum(1 for r in results if r["overall_pass"])
        task_correct_count = sum(1 for r in results if r["task_correct"])
        tool_correct_count = sum(1 for r in results if r["tool_correct"])
        grounded_count = sum(1 for r in results if r.get("grounded", False))

        latencies_sorted = sorted(latencies)
        p50 = latencies_sorted[int(0.50 * len(latencies_sorted))] if latencies_sorted else 0.0
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))] if latencies_sorted else 0.0

        return {
            "total_cases": total,
            "pass_rate_pct": round((passed / total) * 100, 2),
            "task_correctness_rate_pct": round((task_correct_count / total) * 100, 2),
            "tool_accuracy_pct": round((tool_correct_count / total) * 100, 2),
            "groundedness_rate_pct": round((grounded_count / total) * 100, 2),
            "latency_p50_seconds": round(p50, 3),
            "latency_p95_seconds": round(p95, 3),
        }