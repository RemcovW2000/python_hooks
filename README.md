# python-hooks

Centralised pre-commit config and custom hooks for all Python repos.

## Usage

In any repo, run once to install:

```bash
curl -o .pre-commit-config.yaml https://raw.githubusercontent.com/RemcovW2000/python_hooks/main/.pre-commit-config.yaml
pre-commit install
```

## Hooks

| Hook | Source |
|---|---|
| trailing-whitespace, end-of-file-fixer, check-yaml, check-toml, check-merge-conflict, check-added-large-files | pre-commit-hooks |
| ruff, ruff-format | astral-sh/ruff-pre-commit |
| flake8 (ANN rules) | pycqa/flake8 + flake8-annotations |
| check-docstrings | this repo |

### check-docstrings

Enforces NumPy-style docstrings with inline `name : description` format in Parameters, Attributes, and Raises sections. See [DOCSTRINGS.md](https://github.com/RemcovW2000/Structures/blob/main/DOCSTRINGS.md) for the format spec.

## Updating

1. Edit the hook or `.pre-commit-config.yaml` in this repo
2. Tag a new release: `git tag v1.x.0 && git push origin v1.x.0`
3. Re-sync each repo: re-run the `curl` command above, then `pre-commit autoupdate`
