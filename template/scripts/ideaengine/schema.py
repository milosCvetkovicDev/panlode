"""Per-record validation for the four record types (09-08 spec §4.1–4.3 and §4.5)."""

import re
from dataclasses import dataclass
from datetime import date

from ideaengine.frontmatter import Value


@dataclass(frozen=True)
class Issue:
    level: str  # "error" or "warning"
    path: str  # repo-relative
    message: str

    def __str__(self) -> str:
        return f"{self.level} {self.path}: {self.message}"


SIGNAL_SOURCES = (
    "local-interview", "online-interview", "reddit", "hn", "indiehackers", "g2", "capterra", "trustpilot",
    "upwork", "freelance", "job-post", "regulation", "marketplace", "github", "forum", "linkedin", "other",
)
FREQUENCIES = ("daily", "weekly", "monthly", "event-driven", "unknown")
SIGNAL_STATUSES = ("new", "clustered", "promoted", "dismissed")
IDEA_STATUSES = ("shaped", "validating", "go", "parked", "killed", "building-elsewhere")
SHAPES = ("service", "product", "hybrid")
EXPERIMENT_METHODS = ("outreach", "interviews", "landing-page", "pre-sale", "concierge", "fake-door", "other")
EXPERIMENT_STATUSES = ("planned", "running", "done")
DECISIONS = ("continue", "pivot", "kill")
CHANNELS = ("in-person", "call", "chat", "email")

SCORES = ("score_pain", "score_reach", "score_willingness", "score_speed", "score_fit")
MAX_PAIN_CHARS = 200
MAX_BUDGET_EUR = 100
MAX_EXPERIMENT_DAYS = 14

# Field kinds: ("text",), ("date",), ("enum", values), ("int", lo, hi), ("id", prefix),
# ("ids", prefix), ("list",). Each type maps to (required specs, optional specs).
_SPECS: dict[str, tuple[dict[str, tuple], dict[str, tuple]]] = {
    "signal": (
        {
            "id": ("id", "sig"), "type": ("text",), "title": ("text",), "source": ("enum", SIGNAL_SOURCES),
            "ref": ("text",), "captured": ("date",), "segment": ("text",), "pain": ("text",),
            "frequency": ("enum", FREQUENCIES), "workaround": ("text",), "pays_today": ("text",),
            "evidence": ("int", 1, 5), "status": ("enum", SIGNAL_STATUSES),
        },
        {"trigger": ("text",), "cluster": ("text",), "related": ("ids", "sig"), "ideas": ("ids", "idea")},
    ),
    "idea": (
        {
            "id": ("id", "idea"), "type": ("text",), "title": ("text",), "status": ("enum", IDEA_STATUSES),
            "shape": ("enum", SHAPES), "signals": ("ids", "sig"), "segment": ("text",), "offer": ("text",),
            "price_hypothesis": ("text",), "first_customer_days": ("int", 1, None),
            **{score: ("int", 1, 5) for score in SCORES},
            "score_total": ("int", 5, 25), "created": ("date",), "updated": ("date",),
        },
        {"product_path": ("text",), "kill_criteria": ("list",), "next": ("id", "exp"), "archive_ref": ("text",)},
    ),
    "experiment": (
        {
            "id": ("id", "exp"), "type": ("text",), "idea": ("id", "idea"),
            "method": ("enum", EXPERIMENT_METHODS), "hypothesis": ("text",), "success_metric": ("text",),
            "budget_eur": ("int", 0, None), "deadline": ("date",), "status": ("enum", EXPERIMENT_STATUSES),
            "created": ("date",), "updated": ("date",),
        },
        {"result": ("text",), "decision": ("enum", DECISIONS)},
    ),
    "interview": (
        {
            "type": ("text",), "date": ("date",), "channel": ("enum", CHANNELS), "segment": ("text",),
            "consent": ("enum", ("yes", "no")),
        },
        {"promoted_to": ("ids", "sig")},
    ),
}

FIELDS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    kind: (frozenset(required), frozenset(optional)) for kind, (required, optional) in _SPECS.items()
}

FOLDER_TYPES = {"signals": "signal", "ideas": "idea", "experiments": "experiment", "interviews": "interview"}

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_FILE_PATTERNS = {
    "signal": re.compile(rf"^signals/\d{{4}}-\d{{2}}-\d{{2}}-{_SLUG}\.md$"),
    "idea": re.compile(rf"^ideas/{_SLUG}/idea\.md$"),
    "experiment": re.compile(rf"^experiments/(exp-\d{{4}})-{_SLUG}\.md$"),
    "interview": re.compile(rf"^interviews/\d{{4}}-\d{{2}}-\d{{2}}-{_SLUG}\.md$"),
}
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_ANYWHERE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def _is_empty(value: Value | None) -> bool:
    return value is None or value == "" or value == []


def _is_placeholder(value: Value) -> bool:
    """A value still in its template form, `<...>`."""
    items = value if isinstance(value, list) else [value]
    return any(item.strip().startswith("<") and item.strip().endswith(">") for item in items)


def _as_list(value: Value) -> list[str]:
    return value if isinstance(value, list) else [value]


def parse_date(value: Value | None) -> date | None:
    if not isinstance(value, str) or not _DATE.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_int(value: Value | None) -> int | None:
    if isinstance(value, str) and re.fullmatch(r"\d+", value):
        return int(value)
    return None


def _check_kind(key: str, value: Value, spec: tuple) -> str | None:
    kind = spec[0]
    if kind == "text":
        return f"{key} must be a single value, not a list" if isinstance(value, list) else None
    if kind == "date":
        return None if parse_date(value) else f"invalid date in {key}: {value}"
    if kind == "enum":
        return None if value in spec[1] else f"{key} must be one of: {', '.join(spec[1])}"
    if kind == "int":
        lo, hi = spec[1], spec[2]
        number = parse_int(value)
        if number is None or number < lo or (hi is not None and number > hi):
            return f"{key} must be an integer from {lo} to {hi}" if hi else f"{key} must be an integer of at least {lo}"
        return None
    if kind == "id":
        return None if isinstance(value, str) and re.fullmatch(rf"{spec[1]}-\d{{4}}", value) else (
            f"{key} must look like {spec[1]}-0001"
        )
    if kind == "ids":
        bad = [item for item in _as_list(value) if not re.fullmatch(rf"{spec[1]}-\d{{4}}", item)]
        return f"{key} must list ids like {spec[1]}-0001" if bad else None
    return None  # "list": any list of strings


def _filename_issues(rel_path: str, kind: str, fields: dict[str, Value]) -> list[str]:
    if not rel_path.isascii() or rel_path != rel_path.lower():
        return ["file name must be ASCII lowercase"]
    match = _FILE_PATTERNS[kind].match(rel_path)
    if not match:
        return [f"file name does not follow the {kind} pattern"]
    if kind == "experiment" and fields.get("id") != match.group(1):
        return [f"file name does not match id {fields.get('id')}"]
    return []


def _conditional_issues(kind: str, fields: dict[str, Value]) -> list[str]:
    found = []
    status = fields.get("status")
    if kind == "signal" and status in ("clustered", "promoted") and _is_empty(fields.get("cluster")):
        found.append(f"cluster is required when status is {status}")
    if kind == "idea":
        shape = fields.get("shape")
        if shape in ("service", "hybrid") and _is_empty(fields.get("product_path")):
            found.append(f"product_path is required when shape is {shape}")
        if status == "validating":
            for key in ("kill_criteria", "next"):
                if _is_empty(fields.get(key)):
                    found.append(f"{key} is required when status is validating")
            for item in _as_list(fields.get("kill_criteria") or []):
                if not _DATE_ANYWHERE.search(item):
                    found.append("kill_criteria item has no date")
        scores = [parse_int(fields.get(score)) for score in SCORES]
        total = parse_int(fields.get("score_total"))
        if None not in scores and total is not None and total != sum(scores):
            found.append(f"score_total is {total} but the scores sum to {sum(scores)}")
    if kind == "experiment" and status == "done":
        for key in ("result", "decision"):
            if _is_empty(fields.get(key)):
                found.append(f"{key} is required when status is done")
    return found


def _warnings(kind: str, fields: dict[str, Value]) -> list[str]:
    found = []
    required, optional = FIELDS[kind]
    found += [f"unknown field: {key}" for key in fields if key not in required | optional]
    pain = fields.get("pain")
    if kind == "signal" and isinstance(pain, str) and len(pain) > MAX_PAIN_CHARS:
        found.append(f"pain is {len(pain)} characters; keep it to {MAX_PAIN_CHARS}")
    if kind == "experiment":
        budget = parse_int(fields.get("budget_eur"))
        if budget is not None and budget > MAX_BUDGET_EUR:
            found.append(f"budget_eur is {budget}; the limit is {MAX_BUDGET_EUR}")
        created, deadline = parse_date(fields.get("created")), parse_date(fields.get("deadline"))
        if created and deadline and (deadline - created).days > MAX_EXPERIMENT_DAYS:
            found.append(f"deadline is {(deadline - created).days} days after created; the limit is {MAX_EXPERIMENT_DAYS}")
    return found


def validate_record(rel_path: str, fields: dict[str, Value]) -> list[Issue]:
    """Check one record against its type's schema; the type comes from the folder."""
    kind = FOLDER_TYPES.get(rel_path.split("/", 1)[0])
    if kind is None:
        return [Issue("error", rel_path, "not in a record folder")]
    errors = _filename_issues(rel_path, kind, fields)
    if fields.get("type") not in (None, "", kind):
        errors.append(f"type is {fields['type']} but files in {rel_path.split('/', 1)[0]}/ must be {kind}")
    required, optional = _SPECS[kind]
    for key, spec in required.items():
        if _is_empty(fields.get(key)):
            errors.append(f"missing required field: {key}")
        elif message := _check_kind(key, fields[key], spec):
            errors.append(message)
    for key, spec in optional.items():
        if not _is_empty(fields.get(key)) and (message := _check_kind(key, fields[key], spec)):
            errors.append(message)
    errors += _conditional_issues(kind, fields)
    errors += [f"template placeholder left in {key}" for key, value in fields.items() if _is_placeholder(value)]
    return [Issue("error", rel_path, m) for m in errors] + [Issue("warning", rel_path, m) for m in _warnings(kind, fields)]
