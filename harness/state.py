from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentState(str, Enum):
    INITIATED = "INITIATED"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class StateManager(BaseModel):
    current_state: AgentState = AgentState.INITIATED
    max_history_turns: int = 6

    def transition_to(self, new_state: AgentState) -> None:
        self.current_state = new_state

    def truncate_history(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Preserves system instructions and limits context window to recent turns."""
        if len(history) <= self.max_history_turns + 1:
            return history
        system_msg = history[0]
        recent_turns = history[-self.max_history_turns :]
        return [system_msg] + recent_turns