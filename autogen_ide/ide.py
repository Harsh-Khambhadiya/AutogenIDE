from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agents.planner import PlannerAgent
from .agents.coder import CoderAgent
from .agents.reviewer import ReviewerAgent
from .agents.scanner import ScannerAgent
from .agents.supervisor import SupervisorAgent
from .agents.log_agent import LogAgent
from .agents.conversable import ConversableAgent
from .agents.web_reader import WebReaderAgent
from .agents.terminal import TerminalAgent
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
        self.terminal = TerminalAgent()

    def reset(self) -> None:
        self.memory.reset()
        self.logger.log({"action": "reset"})

    def analyze(self) -> list[str]:
        files = self.scanner.scan(str(self.root))
        modules = list(self.scanner.analyze_modules(str(self.root)))
        self.logger.log({"action": "analyze", "files": files, "modules": modules})
        return files

    def run_task(self, task: str, auto_confirm: bool = False) -> None:
        phase = self.memory.advance_phase()
        plan = self.planner.plan(task)
        self.logger.log({"action": "plan", "phase": phase, "plan": plan})
        print("Execution plan:\n", plan)
        if not auto_confirm:
            confirm = input("Proceed with execution? [y/N] ").strip().lower()
            if confirm != "y":
                print("Aborted")
                return
        self.coder.apply_patch(self.root / f"result_{phase}.txt", plan)
        valid = self.reviewer.review(self.root / f"result_{phase}.txt")
        self.logger.log({"action": "review", "phase": phase, "valid": valid})
        self.supervisor.supervise(task, {"plan": plan, "valid": valid})

    def chat(self, prompt: str) -> str:
        self.memory.append_chat("user", prompt)
        response = self.conversable.respond(prompt)
        self.memory.append_chat("assistant", response)
        self.logger.log({"action": "chat", "prompt": prompt, "response": response})
        return response

    def shell(self, cmd: str) -> tuple[int, str, str]:
        ret, out, err = self.terminal.run(cmd)
        self.logger.log({"action": "shell", "cmd": cmd, "returncode": ret})
        return ret, out, err


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI IDE")
    parser.add_argument("root", help="project root directory")
    sub = parser.add_subparsers(dest="cmd", required=False)

    sub.add_parser("analyze")
    run_p = sub.add_parser("run")
    run_p.add_argument("task")
    run_p.add_argument("--yes", action="store_true", help="auto confirm")
    chat_p = sub.add_parser("chat")
    chat_p.add_argument("prompt")
    shell_p = sub.add_parser("shell")
    shell_p.add_argument("command")
    sub.add_parser("reset")

    args = parser.parse_args()

    ide = OfflineIDE(args.root)
    if args.cmd == "reset":
        ide.reset()
    elif args.cmd == "run":
        ide.run_task(args.task, auto_confirm=args.yes)
    elif args.cmd == "chat":
        print(ide.chat(args.prompt))
    elif args.cmd == "shell":
        code, out, err = ide.shell(args.command)
        print(out)
        if err:
            print(err, file=sys.stderr)
    else:
        ide.analyze()


if __name__ == "__main__":
    main()
