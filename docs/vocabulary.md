# Vocabulary Normalization

Voice transcription sometimes misrecognizes technical terms, product names, or people's names.

For example:
- "5 train" might be transcribed instead of "Fivetran"

The vocabulary normalization feature lets you define preferred spellings and known corrections. These are injected into the Ollama cleanup prompt at runtime, so the LLM can apply them when structuring your notes.

The raw transcript is never modified — normalization only happens during the LLM cleanup stage, keeping the pipeline easy to debug.

## Configuration file

Create a YAML file at:

```
~/.config/workjournal/vocabulary.yaml
```

If the file does not exist, the tool runs normally with no vocabulary normalization.

## Example configuration

```yaml
vocabulary:
  - Fivetran
  - Snowflake
  - Datadog
  - Terraform
  - OpenTofu

corrections:
  "5 train": "Fivetran"
  "five train": "Fivetran"
```

## Sections

**`vocabulary`** — a list of preferred spellings for tools, products, or names. The LLM will use these spellings when context suggests they are intended.

**`corrections`** — a mapping of known transcription mistakes to their correct form. Corrections are applied contextually: if the word clearly refers to something else, it is left unchanged.

Both sections are optional. You can include one, both, or neither.

## How it works

When you run `wj log` or `wj paste`, the tool:

1. Loads `~/.config/workjournal/vocabulary.yaml` if it exists
2. Appends any vocabulary terms and corrections to the cleanup prompt sent to Ollama
3. Ollama applies normalization during the cleanup stage
4. The structured entry uses the corrected spellings

The raw transcript printed during `wj log --transcript-only` will still show the original transcription — this is intentional and useful for debugging.

## Tips

- Add terms as you encounter transcription mistakes in practice
- Corrections should be specific enough to avoid false positives
- The LLM applies corrections contextually, not blindly, so occasional misses are expected
- You can edit the file at any time — changes take effect on the next run
