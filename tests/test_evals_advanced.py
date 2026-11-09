from evals.graders.trajectory import TrajectoryEvaluator
from evals.graders.llm_judge import LLMJudge


def test_trajectory_evaluator_efficiency():
    events = [
        {"event_type": "PLANNER_DECISION", "payload": {"tool_name": "search_documents"}},
        {"event_type": "PLANNER_DECISION", "payload": {"tool_name": "search_documents"}},
    ]
    result = TrajectoryEvaluator.evaluate_trajectory(events, optimal_steps=1)
    assert result.redundant_tool_calls == 1
    assert result.trajectory_score < 1.0


def test_llm_judge_fallback_on_none():
    judge = LLMJudge()
    res = judge.evaluate("Test task", None, "Expected output")
    assert res.passed is False
    assert res.score == 0.0