from __future__ import annotations

from pathlib import Path
from typing import Iterable


class CoderAgent:
    """Handles file creation, modification and deletion tasks."""

    def apply_patch(self, file_path: str, content: str) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def delete(self, file_path: str) -> None:
        path = Path(file_path)
        if path.exists():
            path.unlink()

    def append(self, file_path: str, lines: Iterable[str]) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
