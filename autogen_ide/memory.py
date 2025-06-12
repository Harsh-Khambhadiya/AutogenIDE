import json
from pathlib import Path
from typing import Any


class Memory:
    """Simple JSON-based memory for persisting state."""

    def __init__(self, path: str = "memory.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self) -> dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
