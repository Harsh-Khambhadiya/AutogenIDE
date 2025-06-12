import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


class LogAgent:
    """Records prompts, responses, and errors into a YAML or JSON log."""

    def __init__(self, log_path: str = "logs/actions.json") -> None:
        self.log_file = Path(log_path)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            if self.log_file.suffix == ".yaml" and yaml:
                self.log_file.write_text("[]", encoding="utf-8")
            else:
                self.log_file.write_text("[]", encoding="utf-8")

    def log(self, entry: dict[str, Any]) -> None:
        if self.log_file.suffix == ".yaml" and yaml:
            data = yaml.safe_load(self.log_file.read_text(encoding="utf-8")) or []
            data.append(entry)
            self.log_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        else:
            data = json.loads(self.log_file.read_text(encoding="utf-8"))
            data.append(entry)
            self.log_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
