# workjournal

A lightweight CLI for capturing and structuring daily work notes.

## Setup

**Python environment**

```bash
pyenv install 3.13.11
pyenv local 3.13.11
poetry install
```

**System dependencies**

```bash
brew install ffmpeg          # for voice recording
pip install openai-whisper   # for transcription
ollama pull qwen2.5:7b       # Ollama must be running
```

**Run**

```bash
poetry run wj --help
```

Or add Poetry's bin directory to your `PATH` and run `wj` directly.

## Usage

```bash
wj log      # Record a voice note -> transcribe -> structure -> append
wj paste    # Type or pipe notes -> structure -> append
wj today    # Print today's log
wj edit     # Open today's log in $EDITOR
```

### Voice notes

```bash
wj log
# Recording... Press Enter to stop.
# <speak your notes>
# <press Enter>
# Transcribing...
# Cleaning up with Ollama...
# --- Preview ---
# ...
# [a]ppend / [e]dit / [d]iscard:
```

### Text notes

```bash
wj paste
# Enter your notes (Ctrl+D when done):
# ...

# or pipe from stdin:
echo "fixed the login bug, need to write tests" | wj paste
```

## Log format

Logs are stored at `~/worklog/YYYY/YYYY-MM-DD.md`:

```markdown
# 2026-03-06

## 09:42

done:
- fixed authentication bug in login flow

next:
- write tests for the fix
```

## Dependencies

- **ffmpeg** (`brew install ffmpeg`) — audio recording via AVFoundation
- **openai-whisper** (`pip install openai-whisper`) — local transcription
- **Ollama** with `qwen2.5:7b` pulled — note cleanup

## Troubleshooting

**Ollama is not running**

```bash
ollama serve
# or
brew services start ollama
```

**Model not pulled yet**

```bash
ollama pull qwen2.5:7b
```

**Verify everything is working**

```bash
bash tests/smoke_test.sh
```

The smoke test checks that Ollama is reachable and the model is available before running. If either check fails, it prints a clear message and exits non-zero.

## Smoke Testing

A simple manual sanity check (not a full test suite) is included:

```bash
bash tests/smoke_test.sh
```

This pipes `tests/sample_notes.txt` through `wj paste --dry-run`, running the full Ollama cleanup pipeline and printing the generated entry without writing anything to your journal. Use it to verify the CLI and Ollama integration are working.

You can also use `--dry-run` directly:

```bash
echo "fixed a bug, need to write tests" | wj paste --dry-run
```

## Customization

Edit `prompts-runtime/cleanup.md` to change how Ollama structures your notes.
