Please reorganize the prompt structure.

Runtime prompts should live in:

prompts-runtime/

Development prompts should live in:

prompts-dev/

The cleanup prompt that the CLI uses should be moved to:

prompts-runtime/cleanup.md

Update the code so runtime prompts are loaded from the prompts-runtime directory.

Update any documentation that refers to the old prompts directory.
