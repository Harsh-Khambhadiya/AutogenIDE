from __future__ import annotations

from .conversable import ConversableAgent


class PlannerAgent:
    """Generates an execution plan using the ConversableAgent."""

    def __init__(self, conversable: ConversableAgent | None = None) -> None:
        self.conv = conversable or ConversableAgent()

    def plan(self, task: str) -> str:
        prompt = f"Create a concise plan for the following task:\n{task}\nPlan:"
        return self.conv.respond(prompt)
