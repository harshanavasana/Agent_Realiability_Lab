from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class TrajectoryScore(BaseModel):
    is_efficient: bool
    total_steps: int
    optimal_steps: int
    redundant_tool_calls: int
    trajectory_score: float  # Scale: 0.0 to 1.0


class TrajectoryEvaluator:
    @staticmethod
    def evaluate_trajectory(events: List[Dict[str, Any]], optimal_steps: int = 1) -> TrajectoryScore:
        tool_decisions = [
            e["payload"]["tool_name"] for e in events if e.get("event_type") == "PLANNER_DECISION"
        ]

        total_steps = len(tool_decisions)
        
        # Calculate redundant repeated tool calls
        redundant_calls = 0
        seen_calls = set()
        for call in tool_decisions:
            if call in seen_calls:
                redundant_calls += 1
            seen_calls.add(call)

        # Calculate efficiency score (penalize extra steps and repetitions)
        if total_steps == 0:
            score = 1.0
        else:
            step_penalty = max(0.0, (total_steps - optimal_steps) * 0.2)
            redundancy_penalty = redundant_calls * 0.3
            score = max(0.0, 1.0 - step_penalty - redundancy_penalty)

        return TrajectoryScore(
            is_efficient=score >= 0.8,
            total_steps=total_steps,
            optimal_steps=optimal_steps,
            redundant_tool_calls=redundant_calls,
            trajectory_score=round(score, 2),
        )