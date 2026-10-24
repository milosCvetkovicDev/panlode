"""Parser for the flat YAML subset used in record frontmatter.

Supported: `key: scalar`, `key: [a, b]`, `key:` followed by `  - item` lines, and full-line `#`
comments. No nested maps. Standard library only, so the engine and its hooks need no third-party package.
"""

import re

Value = str | list[str]

_KEY_LINE = re.compile(r"^([a-z_]+):(.*)$")


class FrontmatterError(ValueError):
    """A frontmatter problem; `line` is 1-based in the normalised text."""

    def __init__(self, line: int, message: str):
        super().__init__(message)
        self.line = line


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _inline_list(value: str) -> list[str]:
    inner = value[1:-1].strip()
    return [_unquote(part.strip()) for part in inner.split(",") if part.strip()]


def parse(text: str) -> tuple[dict[str, Value], str]:
    """Split a record into (fields, body); raise FrontmatterError on anything outside the subset."""
    text = text.removeprefix("﻿").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines[0].strip() != "---":
        raise FrontmatterError(1, "no frontmatter")

    fields: dict[str, Value] = {}
    list_key: str | None = None
    for index in range(1, len(lines)):
        number = index + 1
        line = lines[index]
        stripped = line.strip()
        if stripped == "---":
            return fields, "\n".join(lines[index + 1:])
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "-" or stripped.startswith("- "):
            if list_key is None:
                raise FrontmatterError(number, "list item without a key above it")
            if fields[list_key] == "":
                fields[list_key] = []
            fields[list_key].append(_unquote(stripped[1:].strip()))
            continue
        if line[0].isspace():
            raise FrontmatterError(number, "nested maps are not supported")
        match = _KEY_LINE.match(line)
        if not match:
            raise FrontmatterError(number, f"cannot read line: {line!r}")
        key, value = match.group(1), match.group(2).strip()
        if key in fields:
            raise FrontmatterError(number, f"duplicate key: {key}")
        if value == "":
            fields[key] = ""
            list_key = key
        elif value.startswith("[") and value.endswith("]"):
            fields[key] = _inline_list(value)
            list_key = None
        else:
            fields[key] = _unquote(value)
            list_key = None

    last_line = len(text.rstrip("\n").split("\n"))
    raise FrontmatterError(last_line, "frontmatter not closed: no second --- line")
