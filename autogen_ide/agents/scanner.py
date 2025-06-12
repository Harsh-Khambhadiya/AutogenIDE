from pathlib import Path


class ScannerAgent:
    """Scans the project folder and identifies files."""

    def scan(self, root: str) -> list[str]:
        return [str(p) for p in Path(root).rglob("*") if p.is_file()]
