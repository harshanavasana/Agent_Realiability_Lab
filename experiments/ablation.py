from typing import Dict, Any
from experiments.comparison import HarnessComparator


def run_retry_ablation_study() -> Dict[str, Any]:
    comparator = HarnessComparator()
    # Compare constrained budget (step limit=2) against full budget (step limit=5)
    return comparator.compare_configurations(baseline_max_steps=2, candidate_max_steps=5)