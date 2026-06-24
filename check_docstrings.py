"""Custom docstring format checker for the Structures project.

Complements ruff (which checks presence and summary shape) by enforcing the
inline `name : description` format in Parameters / Attributes / Raises blocks
that the project uses but ruff cannot validate. See DOCSTRINGS.md.

Checks each public class, function, and method in the files passed as
arguments and reports violations to stdout. Exits 1 if any are found.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

# Sections whose entries must be inline `name : description`.
NAMED_ITEM_SECTIONS = {"Parameters", "Attributes", "Raises", "Subclasses must"}


def is_public(name: str) -> bool:
    """Return True for names that are part of the public API."""
    return not name.startswith("_")


def check_docstring(doc: str, qualname: str, path: Path, lineno: int) -> list[str]:
    """Return a list of violation messages for one docstring."""
    errors: list[str] = []
    lines = doc.splitlines()
    if not lines:
        return errors

    # Rule: first line ends with a period.
    first = lines[0].strip()
    if first and not first.endswith("."):
        errors.append(f"{path}:{lineno}: {qualname}: first line must end with '.'")

    # Walk for known sections.
    i = 0
    while i < len(lines):
        header = lines[i].strip()
        if header in NAMED_ITEM_SECTIONS and i + 1 < len(lines):
            underline = lines[i + 1].strip()
            if underline == "-" * len(header):
                base_indent = len(lines[i]) - len(lines[i].lstrip())
                j = i + 2
                while j < len(lines):
                    line = lines[j]
                    if not line.strip():
                        break  # Blank line ends the section.
                    line_indent = len(line) - len(line.lstrip())
                    if line_indent > base_indent:
                        errors.append(
                            f"{path}:{lineno}: {qualname}: {header} section "
                            f"must use inline `name : description` format "
                            f"(no multi-line entries)"
                        )
                    elif " : " not in line:
                        errors.append(
                            f"{path}:{lineno}: {qualname}: {header} entry must "
                            f"be `name : description` (got: {line.strip()!r})"
                        )
                    else:
                        name_part, _, desc_part = line.partition(" : ")
                        if not name_part.strip() or not desc_part.strip():
                            errors.append(
                                f"{path}:{lineno}: {qualname}: {header} entry "
                                f"missing name or description"
                            )
                    j += 1
                i = j
                continue
        i += 1

    return errors


def check_file(path: Path) -> list[str]:
    """Return all violations found in one file."""
    try:
        src = path.read_text()
    except OSError as e:
        return [f"{path}: read error: {e}"]
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"{path}: syntax error: {e}"]

    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not is_public(node.name):
                continue
            doc = ast.get_docstring(node, clean=False)
            if doc is None:
                continue
            errors.extend(check_docstring(doc, node.name, path, node.lineno))
    return errors


def main(argv: list[str]) -> int:
    """Entry point. Args are file paths to check."""
    errors: list[str] = []
    for arg in argv:
        path = Path(arg)
        if path.suffix != ".py" or not path.is_file():
            continue
        errors.extend(check_file(path))
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
