class SupervisorAgent:
    """Oversees task flow and fallback."""

    def supervise(self, task: str) -> str:
        return f"Supervising task: {task}"
