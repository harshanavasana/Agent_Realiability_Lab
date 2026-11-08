import json
from typing import List, Dict, Optional
from agent.model import OllamaClient
from agent.runtime import Action
from agent.instructions import SYSTEM_PROMPT


class LLMPlanner:
    def __init__(self, model_client: Optional[OllamaClient] = None):
        self.client = model_client or OllamaClient()
        self.history: List[Dict[str, str]] = []

    def reset(self):
        """Resets planner history between task runs."""
        self.history = []

    def plan(self, task: str, step: int) -> Optional[Action]:
        # Initialize conversation on step 1
        if step == 1 or not self.history:
            self.history = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Task: {task}"},
            ]

        raw_response = self.client.generate_completion(self.history)

        # Clean markdown code blocks if present
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned_response = "\n".join(lines).strip()

        try:
            parsed = json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"Model failed to return valid JSON. Raw output: {raw_response}")

        tool_name = parsed.get("tool_name")
        tool_input = parsed.get("tool_input", {})

        # Record model response in message history
        self.history.append({"role": "assistant", "content": cleaned_response})

        if tool_name == "final_answer":
            return None

        if not tool_name:
            raise ValueError(f"Model output missing 'tool_name'. Raw output: {raw_response}")

        # Inject simulated observation so the model knows the tool succeeded on step 2
        self.history.append({
            "role": "user", 
            "content": f"Observation from step {step}: Tool '{tool_name}' executed successfully. Provide final_answer if task is complete."
        })

        return Action(tool_name=tool_name, tool_input=tool_input)