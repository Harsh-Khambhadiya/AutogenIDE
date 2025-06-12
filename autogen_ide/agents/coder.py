class CoderAgent:
    """Handles file creation and modification tasks."""

    def apply_patch(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
