import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from agent.model import OllamaClient


class LLMJudgeScore(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    passed: bool


JUDGE_PROMPT = """You are an expert AI Evaluation Judge.
Your job is to strictly evaluate an AI agent's response against a user task and ground truth criteria.

Task: {task}
Agent Response: {output}
Ground Truth / Expected Content: {expected}

Evaluate the response based on:
1. Correctness: Does it answer the task accurately?
2. Groundedness: Is it supported by the expected content?
3. Concise Clarity: Is it clear and free of hallucinated noise?

Respond strictly in raw JSON with no markdown block formatting:
{{
    "score": <float between 0.0 and 1.0>,
    "reasoning": "<short explanation of your score>",
    "passed": <true if score >= 0.7 else false>
}}
"""


class LLMJudge:
    def __init__(self, model_client: Optional[OllamaClient] = None):
        self.client = model_client or OllamaClient()

    def evaluate(self, task: str, output: Optional[str], expected: Optional[str]) -> LLMJudgeScore:
        if output is None:
            return LLMJudgeScore(score=0.0, reasoning="No output produced by agent.", passed=False)

        prompt = JUDGE_PROMPT.format(task=task, output=output, expected=expected or "N/A")
        messages = [{"role": "user", "content": prompt}]

        try:
            raw_response = self.client.generate_completion(messages)
            
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()

            parsed = json.loads(cleaned)
            return LLMJudgeScore(
                score=float(parsed.get("score", 0.0)),
                reasoning=parsed.get("reasoning", "No reasoning provided."),
                passed=bool(parsed.get("passed", False)),
            )
        except Exception as e:
            return LLMJudgeScore(
                score=0.0,
                reasoning=f"LLM Judge parsing failure: {str(e)}",
                passed=False,
            )