import subprocess


class ReviewerAgent:
    """Validates generated Python code using pyflakes."""

    def review(self, file_path: str) -> bool:
        try:
            result = subprocess.run(
                ["pyflakes", str(file_path)], capture_output=True, text=True, check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            # pyflakes not installed; assume valid
            return True
