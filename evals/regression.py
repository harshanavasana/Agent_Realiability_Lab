import sys
from evals.runner import ComprehensiveEvaluationRunner


def run_regression_gate(min_pass_rate: float = 60.0) -> None:
    runner = ComprehensiveEvaluationRunner(dataset_path="evals/datasets/development.jsonl")
    report = runner.run_evaluations(use_llm_judge=False)

    pass_rate = report["metrics"]["pass_rate_pct"]
    print(f"\n[REGRESSION GATE] Measured Pass Rate: {pass_rate}% | Threshold Required: {min_pass_rate}%")

    if pass_rate < min_pass_rate:
        print("[REGRESSION GATE ERROR] Pass rate dropped below threshold! Blocking release.")
        sys.exit(1)
    else:
        print("[REGRESSION GATE SUCCESS] All quality thresholds satisfied.")
        sys.exit(0)


if __name__ == "__main__":
    run_regression_gate()