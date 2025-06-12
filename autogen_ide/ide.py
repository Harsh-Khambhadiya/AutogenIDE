from __future__ import annotations

import argparse
from pathlib import Path

from .agents.planner import PlannerAgent
from .agents.coder import CoderAgent
from .agents.reviewer import ReviewerAgent
from .agents.scanner import ScannerAgent
from .agents.log_agent import LogAgent
from .memory import Memory


class OfflineIDE:
    """Minimal offline IDE implementing core SRD features."""

    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.memory = Memory(self.root / "memory.json")
        self.planner = PlannerAgent()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.scanner = ScannerAgent()
        self.logger = LogAgent(str(self.root / "logs" / "actions.json"))

    def reset(self) -> None:
        self.memory.save({})
        self.logger.log({"action": "reset"})

    def analyze(self) -> list[str]:
        files = self.scanner.scan(str(self.root))
        self.logger.log({"action": "analyze", "files": files})
        return files

    def run_task(self, task: str) -> None:
        plan = self.planner.plan(task)
        self.logger.log({"action": "plan", "plan": plan})
        # placeholder for coding
        self.coder.apply_patch(self.root / "result.txt", plan)
        valid = self.reviewer.review(self.root / "result.txt")
        self.logger.log({"action": "review", "valid": valid})


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI IDE")
    parser.add_argument("root", help="project root directory")
    parser.add_argument("task", nargs="?", help="task description")
    parser.add_argument("--reset", action="store_true", help="reset memory")
    args = parser.parse_args()

    ide = OfflineIDE(args.root)
    if args.reset:
        ide.reset()
    if args.task:
        ide.run_task(args.task)
    else:
        ide.analyze()


if __name__ == "__main__":
    main()
