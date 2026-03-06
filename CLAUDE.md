# CLAUDE.md

v2

This repository contains a small personal CLI tool called **workjournal**.

Purpose:
Provide a lightweight way for an engineer to quickly capture messy spoken or written notes about work done during the day and convert them into structured markdown work-log entries.

Primary workflow:
1. User records a short voice note from the CLI, or pastes/types messy notes as fallback
2. Tool transcribes audio to text when needed
3. Tool sends the messy text to a local LLM via Ollama
4. LLM converts the notes into a structured entry
5. Entry is reviewed
6. Entry is appended to a daily markdown file

Storage:
Logs are stored outside the repository under:

~/worklog/YYYY/YYYY-MM-DD.md

This repository contains only the tool, not the data.

Design philosophy:

- extremely simple
- low friction
- local-first
- easy to inspect
- avoid heavy frameworks
- prioritize readability
- voice-first if practical

Implementation preferences:

- Python
- Poetry for dependency management
- argparse for CLI
- minimal dependencies
- one main Python file for V1 if practical
- use requests for HTTP calls to Ollama

V1 priorities:

- voice capture from Mac CLI
- local transcription
- cleanup via Ollama
- append to markdown journal
- text input fallback

The CLI command should be:

wj

Future features (do not implement unless asked):

- phone-based voice capture
- raw transcript storage beyond simple local support
- log search commands
- weekly/monthly summaries
- alternate storage backends
- global hotkeys / background app behavior

Important constraint:

This tool should feel like a capture tool, not administrative overhead.
If the workflow becomes cumbersome, simplify it.

Prompt management:

* Prompts should be stored in the `prompts/` directory.
* Code should load prompt files from disk at runtime rather than embedding them in the source code.
* This makes prompts editable without modifying code and keeps them version controlled.

## Prompt organization

This repository uses two categories of prompts.

prompts-runtime/
    Prompts used by the CLI tool when interacting with Ollama.

prompts-dev/
    Prompts used during development with Claude Code.

Runtime prompts are loaded by the application at runtime.
Development prompts are not used by the CLI itself.

## Python environment

Development assumes:

- Python managed with pyenv
- Python version defined via `.python-version`
- Dependency management via Poetry

Current project Python version:

3.13.11

Typical setup:

pyenv install 3.13.11
pyenv local 3.13.11
poetry install

Poetry should use the interpreter provided by pyenv when available.

## Audio capture guidance

For microphone/audio recording in this repository, prefer shelling out to `ffmpeg`
via Python `subprocess` rather than introducing Python audio driver dependencies.

Goals:
- keep the implementation lightweight and inspectable
- avoid PyAudio / sounddevice / other device-specific Python audio stacks unless absolutely necessary
- use temporary files for V1 rather than streaming
- keep the recording path easy to test and debug from the terminal

When implementing or modifying `wj log`:
- prefer `ffmpeg` as the recording backend
- provide clear preflight checks for required local binaries
- fail with actionable install guidance when a required binary is missing
- keep macOS behavior simple and well documented
- preserve the existing local-first pipeline:
  recording -> transcription -> cleanup -> confirmation -> append
