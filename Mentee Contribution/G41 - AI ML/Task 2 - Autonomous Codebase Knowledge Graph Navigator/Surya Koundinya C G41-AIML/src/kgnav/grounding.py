
"""Anti-hallucination verifier: every backticked identifier in the report must exist in
the evidence collected from the graph."""
from __future__ import annotations

import json
import re
from typing import Any

_FENCE = re.compile(r"```.*?```", re.S)
_SPAN = re.compile(r"`([^`\n]+)`")
_SPLIT = re.compile(r"\s*(?:→|->|<-|,|;|\||\+|&)\s*")
_SKIP = re.compile(r"^[\d.\-%/ x×:,\[\]]+$")  # numbers, ratios, numeric lists like [7]


def _walk(value: Any, acc: set[str]) -> None:
    """Collect scalar values and dictionary keys recursively."""
    if value is None:
        return

    if isinstance(value, str):
        value = value.strip()
        if value:
            acc.add(value)

    elif isinstance(value, dict):
        for key, item in value.items():
            acc.add(str(key).strip())
            _walk(item, acc)

    elif isinstance(value, (list, tuple)):
        for item in value:
            _walk(item, acc)

    elif isinstance(value, bool):
        acc.add(str(value))

    elif isinstance(value, (int, float)):
        acc.add(str(value))


def collect_known(evidence: list[dict]) -> set[str]:
    """Build a case-insensitive set of values found in graph evidence."""
    acc: set[str] = set()

    for ev in evidence:
        output = ev.get("output", "")

        try:
            parsed = json.loads(output) if isinstance(output, str) else output
            _walk(parsed, acc)

        except (json.JSONDecodeError, TypeError, ValueError):
            if output is not None:
                _walk(str(output), acc)

        _walk(ev.get("input", {}), acc)

    return {item.lower() for item in acc if item}


def find_ungrounded(report_md: str, known: set[str]) -> list[str]:
    """Return unique backticked identifiers not supported by graph evidence."""
    text = _FENCE.sub("", report_md)
    known_lower = {item.lower() for item in known}

    bad: list[str] = []

    for span in _SPAN.findall(text):
        value = span.strip()
        low = value.lower()

        if not value or low in known_lower or _SKIP.fullmatch(value):
            continue

        # Ignore Cypher fragments and query expressions rather than treating
        # them as graph identifiers.
        if any(token in value for token in ("MATCH", "RETURN", "(", ")", "=", "{id}")):
            continue

        parts = [part.strip() for part in _SPLIT.split(value) if part.strip()]

        if parts and all(
            part.lower() in known_lower or _SKIP.fullmatch(part)
            for part in parts
        ):
            continue

        if value not in bad:
            bad.append(value)

    return bad