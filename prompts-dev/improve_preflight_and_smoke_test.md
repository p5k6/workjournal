Read CLAUDE.md before making changes.

Goal:
Improve the CLI's preflight checks and error handling around Ollama, and improve the smoke test so failures are clearer and more actionable.

This repository is a lightweight personal CLI tool. Keep changes small, readable, and practical. Do not add heavy frameworks or unnecessary abstractions.

Objectives:

1. Improve CLI preflight behavior
2. Improve Ollama-related error messages
3. Improve the smoke test script so it checks prerequisites before running
4. Keep the code simple and easy to debug

Tasks:

1. Review the current CLI implementation and identify how it behaves when:
   - Ollama is not running
   - the Ollama server is unreachable
   - the configured model has not been pulled yet
   - the Ollama request times out or otherwise fails

2. Improve the CLI so that these conditions produce clear, friendly error messages.

Desired behavior:
- If Ollama is not running or localhost:11434 is unreachable, print a clear message such as:
  "Ollama does not appear to be running at http://localhost:11434. Start it with `ollama serve` or `brew services start ollama`."
- If the configured model is unavailable, print a clear message telling the user which model is missing and suggesting `ollama pull <model>`.
- If the request fails for another reason, show a concise error message without a large traceback unless a debug mode is explicitly enabled.
- Exit with a non-zero status on failure.

3. Add a lightweight preflight helper in the CLI if it improves readability.
This can be a small function that:
- checks whether Ollama is reachable
- optionally checks whether the configured model exists
- returns a user-friendly error

Keep it simple. Do not over-engineer.

4. Improve the smoke test script:

tests/smoke_test.sh

Requirements:
- Before running the CLI, check whether Ollama is reachable
- If Ollama is not reachable, print a clear message and exit non-zero
- Optionally check whether the configured model is available if this can be done simply
- Then run the smoke test command
- The smoke test should continue to use anonymized sample notes
- The smoke test must not modify the user's real worklog files

If the CLI already supports `--dry-run`, use it.
If not, keep the smoke test non-destructive.

5. Update README.md with a short troubleshooting section covering:
- Ollama not running
- model not pulled yet
- how to start Ollama
- how to run the smoke test

6. Keep all example text anonymized.
Do not use real coworker names, internal project names, or vendor-specific confidential examples.

Constraints:

- Do not add pytest or any testing framework
- Do not add unnecessary dependencies
- Keep the implementation lightweight
- Prefer concise, readable code over cleverness
- Maintain the current spirit of the tool: low-friction, local-first, easy to inspect

Deliverables:
- updated CLI error handling and preflight behavior
- updated tests/smoke_test.sh
- updated README.md
- any small refactors needed to support the above

Please keep this as a small, understandable iteration rather than a major redesign.
