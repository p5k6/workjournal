Build the first working version of the CLI tool for this repository.

Project: workjournal

Read CLAUDE.md first.

Goals for this commit:

Create a minimal CLI tool called `wj` that allows a user to quickly record a short voice note or provide messy text notes, convert them into a structured markdown entry using local transcription plus a local Ollama model, review the result, and append it to today's journal.

Commands to implement:

wj log
wj paste
wj today
wj edit

Behavior:

wj log
- Record a short voice note from the Mac command line
- Keep the recording flow simple
- Transcribe the audio locally into text
- Send the text to a local Ollama model
- Convert messy notes into a structured markdown entry
- Show preview
- Ask user to append / edit / discard

wj paste
- Accept text from stdin if provided
- Otherwise allow multi-line input
- Send the text to a local Ollama model
- Convert messy notes into a structured markdown entry
- Show preview
- Ask user to append / edit / discard

wj today
- Print today's log file

wj edit
- Open today's log file in $EDITOR or vim

Log storage:

~/worklog/YYYY/YYYY-MM-DD.md

File format:

# YYYY-MM-DD

## HH:MM

done:
- item
- item

next:
- item

Only include "next:" if a clear next step exists.

Implementation guidance:

- Use Python
- Use Poetry
- Use argparse
- Use requests for Ollama
- Keep dependencies minimal
- Prefer a very simple local transcription path for V1
- Prefer shelling out to stable local tools rather than building complex audio code if that simplifies implementation
- Mac-first is acceptable for V1
- It is okay if voice recording is basic as long as it works reliably

Ollama endpoint:

http://localhost:11434/api/generate

Default model:

qwen2.5:7b

Also create:

- pyproject.toml
- README.md
- prompts/cleanup.md

The code should be small, readable, and runnable immediately.
Do not over-engineer audio handling.

For V1, prioritize a working voice capture path over architectural purity.
A somewhat basic Mac-only implementation is acceptable if it is reliable and keeps the tool easy to use.
Text input should remain available as a fallback.
