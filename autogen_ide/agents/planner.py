class PlannerAgent:
    """Plans execution flow for tasks according to the SYSTEM REQUIREMENT DOCUMENT (SRD)."""

    def plan(self, task: str) -> str:
        """Return a basic plan description for the given task."""
        return f"Plan for task: {task}"
