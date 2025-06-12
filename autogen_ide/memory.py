import json
from pathlib import Path
from typing import Any


class Memory:
    """JSON-based memory supporting multi-phase task tracking and chat history."""

    def __init__(self, path: str = "memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    # ------------------------------------------------------------------
    # basic storage helpers

    def reset(self) -> None:
        """Reset memory to a clean state."""
        self.save({"phase": 0, "chat": []})

    def load(self) -> dict[str, Any]:
        """Return the entire memory dictionary."""
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict[str, Any]) -> None:
        """Persist the provided memory dictionary."""
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # chat handling

    def append_chat(self, role: str, message: str) -> None:
        data = self.load()
        chat = data.setdefault("chat", [])
        chat.append({"role": role, "message": message})
        self.save(data)

    def chat_history(self) -> list[dict[str, str]]:
        return self.load().get("chat", [])

    # phase handling -----------------------------------------------------
    def current_phase(self) -> int:
        memory = self.load()
        return int(memory.get("phase", 0))

    def advance_phase(self) -> int:
        memory = self.load()
        memory["phase"] = self.current_phase() + 1
        self.save(memory)
        return memory["phase"]

    def log_history(self, phase: int, entry: dict[str, Any]) -> None:
        """Save entry to history/phase_<n>.json for audit trail."""
        history_dir = self.path.parent / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        phase_file = history_dir / f"phase_{phase}.json"
        if phase_file.exists():
            data = json.loads(phase_file.read_text(encoding="utf-8"))
        else:
            data = []
        data.append(entry)
        phase_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
