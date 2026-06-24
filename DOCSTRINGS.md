# Docstring Guide

NumPy-style sections, inline parameter descriptions, no types in docstrings.

## Rules

1. Every public name has a docstring. Public = no leading underscore.
2. First line: imperative one-liner ending in a period.
3. Blank line between summary and the rest.
4. No types in docstrings. Type hints are the source of truth.
5. Always state units, sign conventions, and coordinate frames.
6. Don't document `__init__`. Put parameters on the class.
7. Parameter and attribute lines are inline: `name : description`. Colons aligned within each block.
8. Tests, examples, `__init__.py`, and material catalogues are exempt.

## Sections

```
Parameters
----------
Returns
-------
Raises
------
Attributes
----------
Notes
-----
```

## Templates

### Module

```python
"""<What this module is responsible for.>"""
```

### Dataclass

```python
"""<What it represents.>

Attributes
----------
<name_a> : <meaning, units, conventions.>
<name_b> : <meaning, units, conventions.>
"""
```

### Class

```python
"""<What it represents.>

Parameters
----------
<name_a> : <meaning, units.>
<name_b> : <meaning, units.>

Attributes
----------
<name_x> : <meaning, units. Only attributes not already in Parameters.>

Notes
-----
<Frame, conventions, side effects. Omit if none apply.>
"""
```

### Abstract base class

```python
"""<What subclasses model.>

Subclasses must
---------------
<method_name> : <what it returns and how it's enforced.>
"""
```

### Function or method

```python
"""<What it does.>

Parameters
----------
<name_a> : <meaning, units.>
<name_b> : <meaning, units.>

Returns
-------
<Meaning, units.>

Raises
------
<ExceptionName> : <when.>
"""
```

Omit any section that isn't applicable.

### Property

One line. Type hint shows the type; docstring states meaning.

```python
"""<What it represents, with units if applicable.>"""
```

### Enum

```python
"""<What the enum represents.>"""
```

### Exception

```python
"""Raised when <condition>."""
```

## Linting

Two layers:

1. **Ruff** (`pyproject.toml`) enforces docstring presence and summary shape (D100–D103, D200, D205, D400, D401).
2. **Custom hook** (`tools/check_docstrings.py`, wired in `.pre-commit-config.yaml`) enforces the inline `name : description` format in `Parameters` / `Attributes` / `Raises` blocks, since ruff does not support custom layouts.

Run both via `pre-commit run --all-files`.
