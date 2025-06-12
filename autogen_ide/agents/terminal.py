from __future__ import annotations

import subprocess
from typing import Iterable


class TerminalAgent:
    """Runs shell commands when permitted."""

    def run(self, cmd: str | Iterable[str]) -> tuple[int, str, str]:
        if isinstance(cmd, str):
            shell = True
            args = cmd
        else:
            shell = False
            args = list(cmd)
        proc = subprocess.run(args, capture_output=True, text=True, shell=shell)
        return proc.returncode, proc.stdout, proc.stderr
