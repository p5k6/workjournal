Read CLAUDE.md before making changes.

Goal:
Standardize the Python development environment for this repository using pyenv and Poetry.

This project is developed on macOS using pyenv and Poetry.

The repository should define the Python version so the environment can be reproduced consistently.

Python Version

Use Python:

3.13.11

This version is already installed locally via pyenv and should be used as the project target.

Tasks

1. Create a file:

.python-version

with contents:

3.13.11

2. Ensure the project is managed with Poetry.

If pyproject.toml does not exist, initialize a Poetry project.

3. Ensure dependencies are managed through Poetry in pyproject.toml rather than requirements.txt.

4. Add minimal required dependencies.

Expected dependencies currently include:

requests

5. Configure the project so the CLI command `wj` can be executed through Poetry.

Add a script entry in pyproject.toml:

[tool.poetry.scripts]
wj = "workjournal.wj:main"

6. Update README.md with environment setup instructions.

Include instructions like:

pyenv install 3.13.11
pyenv local 3.13.11
poetry install

7. Ensure .gitignore includes:

.venv/
__pycache__/
*.pyc

8. Do not introduce unnecessary dependencies or frameworks.

This repository intentionally keeps the Python stack minimal.

The goal is a small, inspectable CLI tool rather than a large application.
