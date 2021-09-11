# Contributing

## Install pre-commit hooks

1. Install dependencies in requirements.txt.
 `pip install -r requirements.txt`
2. Execute `pre-commit install` to install pre-commit.
3. Execute `pre-commit install --hook-type commit-msg` to enable commitizen.

## Rules

The pre-commit hook will run black and flake8, so the committed code must follow the default rules of both formatters and the custom rules written on pyproject.yaml and .flake8.
