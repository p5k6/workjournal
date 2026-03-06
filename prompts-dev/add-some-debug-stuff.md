Please read `CLAUDE.md` first.

Make an incremental update to the existing CLI to improve debugging of the voice transcription path.

Current situation:
- FFmpeg recording is now working
- full flow worked on my personal laptop
- on my work laptop, the voice path is behaving strangely
- the transcript appears to contain almost nothing useful, sometimes just `you`
- then cleanup proceeds and I see repeated nonsense like `corporate data entry for Q1 2023`, which may be hallucinated transcription or unintended seed/example text showing up somewhere in the pipeline

I want a debug path that lets me test transcription without sending anything to Ollama.

Please implement one of the following, using whichever fits the current codebase best:
- `wj transcribe`
- or `wj log --transcript-only`
- or `wj log --debug-transcript`

Requirements:
- this should be an incremental change, not a rewrite
- record audio using the existing FFmpeg path
- run transcription only
- print the raw transcript clearly
- do not call Ollama in this mode
- keep the implementation simple and easy to inspect

Also please:
- add an option to preserve the recorded temp audio file for debugging, if practical
- print enough debug info to help diagnose issues, such as transcript text and optionally audio file path/duration
- inspect the current transcription and cleanup flow to make sure no sample/seed/example text is being accidentally injected into the live transcript path
- if there is currently any example text or fallback text that could leak into real runs, fix that

At the end, please summarize:
1. files changed
2. which command or flag you added
3. how I should test it on my work laptop
4. whether you found any likely cause for the repeated `corporate data entry for Q1 2023` text
