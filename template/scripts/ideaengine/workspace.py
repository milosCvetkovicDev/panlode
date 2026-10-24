"""Load every record in the workspace and check the cross-record invariants (09-08 spec §4.6)."""

import re
from dataclasses import dataclass
from pathlib import Path

from ideaengine.frontmatter import FrontmatterError, Value, parse
from ideaengine.schema import FOLDER_TYPES, Issue, validate_record

MAX_VALIDATING = 3

_RECORD_GLOBS = ("signals/*.md", "ideas/*/idea.md", "experiments/*.md", "interviews/*.md")
_ID_LINE = re.compile(r"^id:\s*(sig|idea|exp)-(\d{4})", re.MULTILINE)
_WELL_FORMED_ID = re.compile(r"^(sig|idea|exp)-\d{4}$")

# Fields that point at other records, per record type.
_REFERENCES = {
    "signal": ("related", "ideas"),
    "idea": ("signals", "next"),
    "experiment": ("idea",),
    "interview": ("promoted_to",),
}


@dataclass
class Record:
    rel_path: str
    type: str
    fields: dict[str, Value]
    body: str

    @property
    def id(self) -> str:
        value = self.fields.get("id", "")
        return value if isinstance(value, str) else ""


def is_record_path(rel_path: str) -> bool:
    parts = rel_path.split("/")
    if not parts[-1].endswith(".md"):
        return False
    if len(parts) == 2 and parts[0] in ("signals", "experiments"):
        return True
    if len(parts) == 2 and parts[0] == "interviews":
        return not parts[1].startswith("targets-")
    return len(parts) == 3 and parts[0] == "ideas" and parts[2] == "idea.md"


def _record_paths(root: Path) -> list[tuple[Path, str]]:
    found = {}
    for pattern in _RECORD_GLOBS:
        for path in root.glob(pattern):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and is_record_path(rel):
                found[rel] = path
    return [(found[rel], rel) for rel in sorted(found)]


def load(root: Path) -> tuple[list[Record], list[Issue]]:
    """Parse every record file; files that cannot be parsed become issues instead of records."""
    records, issues = [], []
    for path, rel in _record_paths(root):
        try:
            fields, body = parse(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            issues.append(Issue("error", rel, "file is not UTF-8 text"))
            continue
        except FrontmatterError as e:
            issues.append(Issue("error", rel, f"line {e.line}: {e}"))
            continue
        records.append(Record(rel, FOLDER_TYPES[rel.split("/", 1)[0]], fields, body))
    return records, issues


def _cross_record_issues(records: list[Record]) -> list[Issue]:
    issues = []
    by_id: dict[str, list[Record]] = {}
    for record in records:
        if record.id:
            by_id.setdefault(record.id, []).append(record)
    for record_id, owners in by_id.items():
        if len(owners) > 1:
            issues += [Issue("error", r.rel_path, f"duplicate id {record_id}") for r in owners]

    for record in records:
        for key in _REFERENCES[record.type]:
            value = record.fields.get(key) or []
            for ref in value if isinstance(value, list) else [value]:
                if _WELL_FORMED_ID.match(ref) and ref not in by_id:
                    issues.append(Issue("error", record.rel_path, f"unknown id {ref} in {key}"))

    validating = [r for r in records if r.type == "idea" and r.fields.get("status") == "validating"]
    if len(validating) > MAX_VALIDATING:
        message = f"{len(validating)} ideas are validating; the limit is {MAX_VALIDATING}"
        issues += [Issue("error", r.rel_path, message) for r in validating]
    return issues


def check(root: Path) -> list[Issue]:
    """All errors and warnings for the workspace: parse, per-record schema, then cross-record."""
    records, issues = load(root)
    for record in records:
        issues += validate_record(record.rel_path, record.fields)
    return issues + _cross_record_issues(records)


def next_id(root: Path, prefix: str) -> str:
    """Next free id for a prefix; reads raw text so a malformed record still reserves its number."""
    highest = 0
    for path, _ in _record_paths(root):
        for match in _ID_LINE.finditer(path.read_text(encoding="utf-8", errors="replace")):
            if match.group(1) == prefix:
                highest = max(highest, int(match.group(2)))
    return f"{prefix}-{highest + 1:04d}"
