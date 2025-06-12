from __future__ import annotations

from typing import Any

from ..memory import Memory


class SupervisorAgent:
    """Oversees task flow, phase tracking and error handling."""

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def supervise(self, task: str, entry: dict[str, Any]) -> None:
        phase = self.memory.current_phase()
        self.memory.log_history(phase, {"task": task, **entry})
