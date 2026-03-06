Please read `CLAUDE.md` first.

Make an incremental update to the existing CLI so `wj log` uses `ffmpeg`
for microphone recording instead of `rec` / SoX.

## Current status

-   `wj paste --dry-run` works
-   Ollama cleanup path works
-   `wj log` currently fails with:

```{=html}
<!-- -->
```
    Error: 'rec' not found. Install sox: brew install sox

## Requirements

-   Preserve the current flow and existing code structure where
    reasonable
-   Use `ffmpeg` via `subprocess`
-   Do not introduce Python audio dependencies unless absolutely
    necessary
-   Record to a temporary file
-   Prefer mono 16 kHz WAV if practical for transcription
-   Update preflight/error handling for missing FFmpeg
-   Update docs if needed
-   Remove SoX-specific assumptions if FFmpeg is now the intended
    backend

## Deliverables

At the end, please summarize:

1.  Files changed
2.  Recording command used
3.  macOS assumptions
4.  How I should test `poetry run wj log`

