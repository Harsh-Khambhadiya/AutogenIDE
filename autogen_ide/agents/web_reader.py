import requests


class WebReaderAgent:
    """Fetches online documentation if allowed."""

    def fetch(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # pragma: no cover - network
            return f"Error fetching {url}: {exc}"
