"""Builders for valid records, shared by the test modules."""

import atexit
import shutil
import tempfile
from pathlib import Path


def valid_signal(**over) -> dict:
    fields = {
        "id": "sig-0001",
        "type": "signal",
        "title": "Accountants re-key e-invoices into bookkeeping software",
        "source": "reddit",
        "ref": "https://example.com/forum/threads/123",
        "captured": "2026-10-20",
        "segment": "Small accounting firms",
        "pain": "Invoices received through the e-invoicing portal are typed into the bookkeeping software again by hand",
        "frequency": "weekly",
        "workaround": "Manual re-keying",
        "pays_today": "Junior bookkeeper hours",
        "evidence": "2",
        "status": "new",
    }
    fields.update(over)
    return fields


def valid_idea(**over) -> dict:
    fields = {
        "id": "idea-0001",
        "type": "idea",
        "title": "E-invoice import for small accounting firms",
        "status": "shaped",
        "shape": "product",
        "signals": ["sig-0001"],
        "segment": "Small accounting firms",
        "offer": "E-invoice-to-bookkeeping import, 49 EUR per month per firm",
        "price_hypothesis": "49 EUR per month",
        "first_customer_days": "21",
        "score_pain": "3",
        "score_reach": "3",
        "score_willingness": "3",
        "score_speed": "3",
        "score_fit": "3",
        "score_total": "15",
        "created": "2026-10-20",
        "updated": "2026-10-20",
    }
    fields.update(over)
    return fields


def valid_experiment(**over) -> dict:
    fields = {
        "id": "exp-0001",
        "type": "experiment",
        "idea": "idea-0001",
        "method": "outreach",
        "hypothesis": "Accounting firms re-key supplier invoices every week",
        "success_metric": "3 of 10 confirm a paid workaround",
        "budget_eur": "0",
        "deadline": "2026-10-30",
        "status": "running",
        "created": "2026-10-20",
        "updated": "2026-10-20",
    }
    fields.update(over)
    return fields


def valid_interview(**over) -> dict:
    fields = {
        "type": "interview",
        "date": "2026-10-23",
        "channel": "call",
        "segment": "Small accounting firms",
        "consent": "yes",
    }
    fields.update(over)
    return fields


def to_markdown(fields: dict, body: str = "") -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}:" if value else f"{key}: []")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{key}: {value}".rstrip())
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def make_workspace(files: dict[str, str]) -> Path:
    """Write files into a fresh temp folder (removed at exit) and return its resolved path."""
    root = Path(tempfile.mkdtemp(prefix="ideaengine-test-")).resolve()
    atexit.register(shutil.rmtree, root, True)
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root
