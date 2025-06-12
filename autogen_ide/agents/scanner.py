from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable


class ScannerAgent:
    """Scans project folders and checks module implementation status."""

    def scan(self, root: str) -> list[str]:
        return [str(p) for p in Path(root).rglob("*") if p.is_file()]

    def analyze_modules(self, root: str) -> Iterable[dict[str, str]]:
        modules = []
        for file in Path(root).rglob("*.py"):
            code = file.read_text(encoding="utf-8")
            status = "Done" if len(code.strip()) > 0 else "Pending"
            try:
                ast.parse(code)
                valid = "Valid"
            except SyntaxError:
                valid = "Syntax Error"
            modules.append(
                {
                    "module": str(file.relative_to(root)),
                    "status": status,
                    "validation": valid,
                }
            )
        return modules
