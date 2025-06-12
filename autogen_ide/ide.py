from __future__ import annotations

import argparse
from pathlib import Path

from .agents.planner import PlannerAgent
from .agents.coder import CoderAgent
from .agents.reviewer import ReviewerAgent
from .agents.scanner import ScannerAgent
from .agents.supervisor import SupervisorAgent
from .agents.log_agent import LogAgent
from .agents.conversable import ConversableAgent
from .agents.web_reader import WebReaderAgent
from .memory import Memory


class OfflineIDE:
    """Offline IDE implementing core SRD features in a simplified form."""

    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.memory = Memory(self.root / "memory.json")
        self.conversable = ConversableAgent()
        self.planner = PlannerAgent(self.conversable)
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.scanner = ScannerAgent()
        self.web_reader = WebReaderAgent()
        self.logger = LogAgent(str(self.root / "logs" / "actions.yaml"))
        self.supervisor = SupervisorAgent(self.memory)

    def reset(self) -> None:
        self.memory.save({"phase": 0})
        self.logger.log({"action": "reset"})

    def analyze(self) -> list[str]:
        files = self.scanner.scan(str(self.root))
        modules = list(self.scanner.analyze_modules(str(self.root)))
        self.logger.log({"action": "analyze", "files": files, "modules": modules})
        return files

    def run_task(self, task: str) -> None:
        phase = self.memory.advance_phase()
        plan = self.planner.plan(task)
        self.logger.log({"action": "plan", "phase": phase, "plan": plan})
        self.coder.apply_patch(self.root / f"result_{phase}.txt", plan)
        valid = self.reviewer.review(self.root / f"result_{phase}.txt")
        self.logger.log({"action": "review", "phase": phase, "valid": valid})
        self.supervisor.supervise(task, {"plan": plan, "valid": valid})

    def chat(self, prompt: str) -> str:
        response = self.conversable.respond(prompt)
        self.logger.log({"action": "chat", "prompt": prompt, "response": response})
        return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI IDE")
    parser.add_argument("root", help="project root directory")
    sub = parser.add_subparsers(dest="cmd", required=False)

    sub.add_parser("analyze")
    run_p = sub.add_parser("run")
    run_p.add_argument("task")
    chat_p = sub.add_parser("chat")
    chat_p.add_argument("prompt")
    sub.add_parser("reset")

    args = parser.parse_args()

    ide = OfflineIDE(args.root)
    if args.cmd == "reset":
        ide.reset()
    elif args.cmd == "run":
        ide.run_task(args.task)
    elif args.cmd == "chat":
        print(ide.chat(args.prompt))
    else:
        ide.analyze()


if __name__ == "__main__":
    main()
