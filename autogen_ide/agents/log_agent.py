import json
from pathlib import Path


class LogAgent:
    """Records prompts, responses, changes, and errors into a JSON log."""

    def __init__(self, log_path: str = "logs/actions.json"):
        self.log_file = Path(log_path)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.write_text("[]", encoding="utf-8")

    def log(self, entry: dict) -> None:
        data = json.loads(self.log_file.read_text(encoding="utf-8"))
        data.append(entry)
        self.log_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
