Please read `CLAUDE.md` first.

Make an incremental improvement to the existing config system.

Current situation:
- the config feature is working
- however, the current implementation is a bit naive
- I ran `wj config set audio_device ...` but the actual key was `audio-device`
- I would like the app to provide a built-in way to discover valid config keys and what they mean

Please update the config system so there is a single source of truth for supported config keys and their descriptions, and use that same source for both:
1. config validation / app behavior
2. `wj config help` output

Goals:
- add a command like `wj config help` that lists all supported config keys
- show each key with a short human-readable description
- make sure the app uses the same source of truth for accepted config keys, rather than duplicating the list in multiple places
- keep this as an incremental refactor, not a rewrite
- keep it lightweight and easy to inspect
- do not introduce a heavy config framework

Requirements:
- preserve the existing config behavior where reasonable
- keep the implementation simple
- choose a source-of-truth approach that fits the current codebase well
- it is fine if this is implemented in Python code, JSON, or another lightweight format, as long as the same source drives both help text and actual config handling
- if there is a sensible way to support aliases or provide helpful error messages for near-miss keys like `audio_device` vs `audio-device`, please do that too
- update any relevant help text or docs if needed

Ideal behavior:
- `wj config help` shows something like:
  - `audio-device` — audio input device index used for FFmpeg recording
  - any other supported config keys with descriptions
- invalid config keys should fail with a useful message
- if practical, suggest the closest valid key when the user mistypes one

At the end, please summarize:
1. files changed
2. what you chose as the config-key source of truth
3. how `wj config help` works
4. whether you added alias handling or near-match suggestions
5. exact commands I should run to test it
