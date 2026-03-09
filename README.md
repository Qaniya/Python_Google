# Intermediate Python Project: Expense Tracker

This repository now contains an intermediate-level Python project featuring:

- Object-oriented domain modeling with `dataclass`.
- JSON persistence.
- Reporting by total and category.
- Command-line interface using `argparse`.
- Unit tests with `pytest`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
pytest
```

## Example usage

```bash
PYTHONPATH=src python -m intermediate_project.cli add 14.5 food "dinner"
PYTHONPATH=src python -m intermediate_project.cli summary
```
