import uuid
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TraceEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    run_id: str
    timestamp: float = Field(default_factory=time.time)
    step: int
    event_type: str
    payload: Dict[str, Any]


class RunTrace(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task: str
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    total_steps: int = 0
    max_steps: int
    status: str = "RUNNING"
    events: List[TraceEvent] = []

    def log_event(self, step: int, event_type: str, payload: Dict[str, Any]) -> None:
        event = TraceEvent(
            run_id=self.run_id,
            step=step,
            event_type=event_type,
            payload=payload,
        )
        self.events.append(event)