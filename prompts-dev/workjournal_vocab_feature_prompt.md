# Claude Code Prompt --- Vocabulary Normalization Feature

You are helping implement a feature in a small personal CLI tool called
**workjournal**.

Please read the context carefully before making changes.

------------------------------------------------------------------------

## Project Overview

This tool captures short voice notes about work activities and converts
them into structured markdown entries.

Current pipeline:

voice recording\
→ transcription via faster-whisper\
→ cleanup via Ollama (model qwen2.5:7b)\
→ structured markdown appended to daily log

Logs are stored as:

\~/worklog/YYYY/YYYY-MM-DD.md

The cleanup stage already performs grammar cleanup and structuring.\
We want to extend it to also normalize **technical vocabulary and common
transcription mistakes**.

------------------------------------------------------------------------

# Design Philosophy

This project intentionally follows a **simple Unix-style design**.

Key constraints:

-   local-first
-   minimal dependencies
-   plain text files
-   easy debugging
-   minimal hidden state
-   no heavy frameworks

Because of this philosophy:

**Raw transcription output must remain untouched.**

Vocabulary normalization should occur only in the **LLM cleanup stage**.

This preserves the ability to debug:

raw transcript\
→ cleaned transcript\
→ final markdown entry

------------------------------------------------------------------------

# New Feature: Vocabulary Normalization

Voice transcription sometimes produces incorrect spellings for technical
tools or people's names.

Examples observed:

"5 train" → should be **Fivetran**\

We want to support two mechanisms to improve cleanup quality.

------------------------------------------------------------------------

# 1. Canonical Vocabulary Terms

Users should be able to define a list of preferred spellings for tools,
products, or names.

Examples:

Fivetran\
Snowflake\
Datadog\
Terraform\
OpenTofu

During cleanup, the LLM should **prefer these spellings when context
suggests they are intended**.

------------------------------------------------------------------------

# 2. Explicit Correction Mappings

Users should also be able to define known transcription mistakes.

Examples:

"5 train" → "Fivetran"\
"five train" → "Fivetran"\

The cleanup LLM should apply these corrections **when they appear likely
in context**.

Important rule:

Corrections must **not be forced blindly**.\
If the word clearly refers to something else, leave it unchanged.

------------------------------------------------------------------------

# Important: User Configurable Vocabulary

This project is open source. Different users will have different
coworkers, tools, and terminology.

Therefore:

-   Vocabulary terms must NOT be hardcoded in the repository.
-   Correction mappings must NOT be hardcoded in the repository.
-   All vocabulary normalization data must come from a **user
    configuration file**.

The repository may include an example configuration for documentation,
but runtime behavior must depend entirely on the user's configuration.

Users should be able to modify vocabulary behavior **without changing
code**.

------------------------------------------------------------------------

# Configuration Design

Vocabulary configuration should be loaded from a YAML file.

Suggested default location:

\~/.config/workjournal/vocabulary.yaml

Example file:

``` yaml
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

Both sections are optional.

Behavior requirements:

-   If the file does not exist → continue normally.
-   If the vocabulary list is empty → continue normally.
-   If the corrections list is empty → continue normally.

------------------------------------------------------------------------

# Implementation Requirements

## 1. Config Loader

Add logic that attempts to load:

\~/.config/workjournal/vocabulary.yaml

If the file exists:

-   parse YAML
-   extract `vocabulary`
-   extract `corrections`

If the file does not exist:

-   treat both lists as empty

Avoid introducing heavy dependencies. Use an existing YAML library if
one is already present.

------------------------------------------------------------------------

## 2. Prompt Injection

Extend the **cleanup prompt sent to Ollama** so that vocabulary and
corrections are included when available.

The prompt should communicate rules like:

-   Clean up grammar and punctuation
-   Preserve the intended meaning
-   Normalize technical terms using preferred vocabulary
-   Apply known correction mappings when context suggests they are
    intended
-   Do not force corrections if the transcript clearly refers to
    something else
-   Do not invent new facts

Vocabulary and corrections should be injected into the prompt in a
readable format.

Example:

Preferred vocabulary terms:

-   Fivetran
-   Snowflake
-   Datadog
-   Terraform
-   OpenTofu

Common transcription corrections:

-   "5 train" → "Fivetran"
-   "five train" → "Fivetran"

When updating prompt templates, modify files under `prompts-runtime/`.
Do not modify anything inside `prompts-dev/`, which stores development prompts only.

------------------------------------------------------------------------

## 3. Update Runtime Prompt Templates

This project stores prompts on disk.

Locate the runtime prompt template in:

`prompts-runtime/`

Update the cleanup prompt so it supports dynamic injection of:

-   preferred vocabulary terms
-   correction mappings

Do not hardcode vocabulary directly in the prompt file.\
The application should inject these lists dynamically at runtime.

------------------------------------------------------------------------

## 4. Graceful Behavior

The system must behave correctly when:

-   vocabulary file is missing
-   vocabulary list is empty
-   corrections list is empty

The tool should still run normally.

------------------------------------------------------------------------

## 5. Debugging Friendliness

Do not modify the raw transcript before it reaches the cleanup stage.

The pipeline must remain:

raw transcript\
→ LLM cleanup\
→ structured entry

All vocabulary normalization should occur during cleanup.

------------------------------------------------------------------------

## 6. Minimal Surface Area

Do not introduce new CLI commands.

Editing the YAML file manually is sufficient.

Possible future improvements (not part of this task):

    wj vocab add
    wj vocab list

But do not implement these yet.

------------------------------------------------------------------------

# Documentation

Add a short documentation page:

`docs/vocabulary.md`

Include:

-   explanation of vocabulary normalization
-   example YAML configuration
-   instructions for users

------------------------------------------------------------------------

# Deliverables

Implement:

-   YAML loader for vocabulary configuration
-   runtime prompt injection
-   graceful fallback behavior
-   prompt template update if necessary
-   documentation page

Keep the implementation small and simple.\
The goal is a lightweight normalization mechanism that improves
transcription accuracy for technical terms while keeping the tool easy
to inspect and debug.
