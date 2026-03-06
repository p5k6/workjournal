Read CLAUDE.md before making changes.

Goal:
Add lightweight smoke tests to the repository. These are not formal unit tests. They are simple sanity checks that help verify the CLI pipeline works end-to-end.

The purpose is to quickly validate:

- CLI commands run
- prompt loading works
- Ollama integration works
- file append logic works

Do NOT add heavy testing frameworks.

Do NOT add pytest or complex test infrastructure.

These should remain simple manual smoke tests.

Tasks:

1. Create a directory:

tests/

2. Inside tests/, add a file:

tests/sample_notes.txt

This file should contain anonymized messy work notes suitable for testing the CLI.

Example style:

spent time debugging an authentication issue with a data platform,
helped a teammate resolve access permissions,
discussed infrastructure planning with leadership,
still need to verify configuration related to role mapping

Avoid real company names, vendors, or personal names.

3. Add a simple smoke test script:

tests/smoke_test.sh

This script should:

- run the CLI using the sample notes
- verify the command runs successfully
- print the output so the user can inspect it

Example structure:

cat tests/sample_notes.txt | wj paste --dry-run

The smoke test should not modify the user's real worklog files.

If necessary, the CLI should support a dry-run mode.

4. If the CLI does not already support it, implement:

--dry-run

Behavior:
- run the full pipeline
- show the generated markdown entry
- do not append anything to the journal file

5. Update README.md with a short section:

## Smoke Testing

Explain how to run the smoke test:

bash tests/smoke_test.sh

Explain that this is a manual sanity check rather than a full automated test suite.

6. Ensure that example inputs and documentation use anonymized systems and roles rather than real coworkers or internal projects.

Constraints:

- Keep everything simple
- Do not introduce new dependencies
- Do not introduce testing frameworks
- These smoke tests should be easy to run and easy to understand

The repository should remain lightweight and easy to hack on.
