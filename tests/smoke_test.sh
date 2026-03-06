#!/usr/bin/env bash
# Smoke test for wj CLI.
# Runs the full paste pipeline in dry-run mode (no files are written).
# Inspect the output to verify the entry looks correct.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OLLAMA_URL="http://localhost:11434"
MODEL="qwen2.5:7b"

echo "=== wj smoke test ==="

# Check Ollama is reachable
if ! curl -sf "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
    echo "Error: Ollama is not running at $OLLAMA_URL."
    echo "Start it with: ollama serve   or   brew services start ollama"
    exit 1
fi
echo "Ollama: reachable"

# Check model is available
if ! curl -sf "$OLLAMA_URL/api/tags" | grep -q "$MODEL"; then
    echo "Error: Model '$MODEL' not found in Ollama."
    echo "Pull it with: ollama pull $MODEL"
    exit 1
fi
echo "Model '$MODEL': available"

echo ""
echo "Piping sample_notes.txt through: wj paste --dry-run"
echo ""

cat "$SCRIPT_DIR/sample_notes.txt" | poetry run wj paste --dry-run

echo ""
echo "=== done ==="
