# Offline AI IDE Skeleton

This repository provides a minimal skeleton implementing some core features of the Offline AI IDE described in the System Requirement Document (SRD).

## Features

- **PlannerAgent** generates a simple plan for tasks.
- **CoderAgent** writes files to disk.
- **ReviewerAgent** returns a dummy review result.
- **ScannerAgent** lists files in the project directory.
- **LogAgent** records actions to `logs/actions.json`.
- **Memory** stores session data in `memory.json`.
- A basic CLI in `autogen_ide/ide.py` to run analysis or execute a task.

This is only a starting point and does not provide a full implementation of the SRD.
