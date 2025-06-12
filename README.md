# Offline AI IDE

This project provides an offline assistant that behaves similarly to ChatGPT but is tailored for local development tasks. It is inspired by the System Requirement Document (SRD) summarised in this repository.

## Implemented Components

- **PlannerAgent** – creates execution plans using a local model.
- **CoderAgent** – writes, appends or deletes files on disk.
- **ReviewerAgent** – validates Python code via `pyflakes` when available.
- **ScannerAgent** – scans folders and analyses Python modules.
- **WebReaderAgent** – fetches documentation from the internet (optional).
- **ConversableAgent** – wraps a HuggingFace model for chat style replies.
- **SupervisorAgent** – records phase history and supervises tasks.
- **Memory** – persistent JSON store with per-phase history.
- **LogAgent** – logs every action to `logs/actions.yaml`.
- **Streamlit UI** – `python -m autogen_ide.ui` launches a simple 3-pane interface.
- **CLI Tool** – `python -m autogen_ide <root> [command]` supports `analyze`, `run`, `chat`, and `reset`.

The implementation is intentionally lightweight so it can run fully offline with a locally available model. Heavy features from the SRD such as multi-model routing or GPU utilisation are left for future expansion.
