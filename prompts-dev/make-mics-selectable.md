Please read `CLAUDE.md` first.

Make an incremental update to the existing workjournal CLI so the audio input device can be configured persistently per machine.

Current situation:
- FFmpeg recording works
- on one machine, FFmpeg device `:0` is Zoom audio and not the real microphone
- the correct built-in microphone appears to be device `:1`
- we do not want to require passing an env var every time for normal daily use

Please update the CLI so audio device selection follows this precedence:

1. explicit CLI flag
2. environment variable
3. local persisted config
4. existing default behavior

Requirements:
- keep this as an incremental change, not a rewrite
- preserve the current flow and structure where reasonable
- keep the implementation lightweight and easy to inspect
- do not introduce heavy config frameworks
- use a simple local config file appropriate for a personal CLI tool
- store config outside the repo in a user-specific location
- keep env var override support for debugging and Unix-style workflows

Please implement something along these lines if it fits the current codebase:

- support `--audio-device N` on relevant voice/transcription commands
- support env var `WJ_AUDIO_DEVICE`
- add a simple config command, for example:
  - `wj config set audio_device 1`
  - `wj config get audio_device`
- have normal voice commands use the configured device automatically

Also please:
- choose a simple config file format and path, and explain why
- update any relevant docs/help text
- keep the behavior easy to debug
- make sure the selected device is clearly shown in debug output when useful

At the end, please summarize:
1. files changed
2. config file path and format chosen
3. precedence rules implemented
4. exact commands I should run on my work laptop to set device `1` and test it
