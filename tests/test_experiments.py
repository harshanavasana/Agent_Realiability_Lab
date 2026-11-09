from experiments.comparison import HarnessComparator


def test_harness_comparator_execution():
    comparator = HarnessComparator(dataset_path="evals/datasets/development.jsonl")
    comparison = comparator.compare_configurations(baseline_max_steps=1, candidate_max_steps=2)
    
    assert "baseline" in comparison
    assert "candidate" in comparison
    assert "deltas" in comparison
    assert isinstance(comparison["deltas"]["improved"], bool)