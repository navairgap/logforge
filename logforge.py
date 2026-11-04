"""Streaming JSONL normalization for the LogForge prototype.

The parser is intentionally local-only and uses the Python standard library.
It yields NormalizedEvent values and bounded ParseIssue diagnostics.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import BinaryIO, Iterator, Union


SEVERITY_MAP = {
    "trace": "trace",
    "debug": "debug",
    "info": "info",
    "notice": "info",
    "warn": "warn",
    "warning": "warn",
    "error": "error",
    "err": "error",
    "fatal": "fatal",
    "critical": "fatal",
}
KNOWN_FIELDS = {
    "timestamp", "time", "@timestamp", "severity", "level",
    "source", "service", "message", "attributes",
}
BIDI_CONTROL_CODES = {
    0x061C, 0x200E, 0x200F, 0x202A, 0x202B, 0x202C,
    0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069,
}


@dataclass(frozen=True)
class NormalizedEvent:
    schema_version: int
    timestamp: str | None
    timestamp_raw: str | None
    timestamp_warning: str | None
    severity: str | None
    severity_raw: str | None
    source: str
    message: str
    attributes: dict
    source_path: str
    line_number: int


@dataclass(frozen=True)
class ParseIssue:
    source_path: str
    line_number: int
    reason: str


ParsedLine = Union[NormalizedEvent, ParseIssue]


def safe_terminal_text(value: str) -> str:
    """Render control bytes visibly instead of allowing terminal escapes."""
    out = []
    for char in value:
        code = ord(char)
        if char == "\x1b":
            out.append("\\x1b")
        elif char == "\n":
            out.append("\\n")
        elif char == "\r":
            out.append("\\r")
        elif char == "\t":
            out.append("\\t")
        elif code in BIDI_CONTROL_CODES:
            out.append(f"\\u{code:04x}")
        elif code < 32 or 0x7f <= code <= 0x9f:
            out.append(f"\\x{code:02x}")
        else:
            out.append(char)
    return "".join(out)


def _normalize_timestamp(raw: object) -> tuple[str | None, str | None, str | None]:
    if raw is None:
        return None, None, None
    if not isinstance(raw, str):
        return None, None, "timestamp is not a string"
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None, raw, "timestamp is not valid ISO-8601"
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None, raw, "timestamp has no UTC offset; no local timezone was assumed"
    normalized = parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")
    normalized = normalized.replace("+00:00", "Z")
    return normalized, raw, None


def _normalize_object(obj: object, source_path: str, line_number: int) -> ParsedLine:
    if not isinstance(obj, dict):
        return ParseIssue(source_path, line_number, "record must be a JSON object")

    raw_timestamp = obj.get("timestamp", obj.get("@timestamp", obj.get("time")))
    timestamp, timestamp_raw, timestamp_warning = _normalize_timestamp(raw_timestamp)

    raw_severity = obj.get("severity", obj.get("level"))
    if isinstance(raw_severity, str):
        severity_raw = raw_severity
        severity = SEVERITY_MAP.get(raw_severity.strip().lower())
    elif raw_severity is None:
        severity_raw = None
        severity = None
    else:
        return ParseIssue(source_path, line_number, "severity must be a string")

    source = obj.get("source", obj.get("service", "unknown"))
    message = obj.get("message", "")
    attributes = obj.get("attributes", {})
    if not isinstance(source, str) or not isinstance(message, str):
        return ParseIssue(source_path, line_number, "source and message must be strings")
    if not isinstance(attributes, dict):
        return ParseIssue(source_path, line_number, "attributes must be a JSON object")

    extras = dict(attributes)
    for key, value in obj.items():
        if key not in KNOWN_FIELDS:
            extras.setdefault(key, value)

    return NormalizedEvent(
        schema_version=1,
        timestamp=timestamp,
        timestamp_raw=timestamp_raw,
        timestamp_warning=timestamp_warning,
        severity=severity,
        severity_raw=severity_raw,
        source=source,
        message=message,
        attributes=extras,
        source_path=source_path,
        line_number=line_number,
    )


def _discard_remainder(stream: BinaryIO) -> None:
    """Drain one oversized physical line using bounded reads."""
    while True:
        chunk = stream.readline(4096)
        if not chunk or chunk.endswith(b"\n"):
            return


def parse_jsonl(
    stream: BinaryIO,
    source_path: str = "<stream>",
    max_record_bytes: int = 65536,
) -> Iterator[ParsedLine]:
    """Parse a binary JSONL stream without retaining the full file or long lines."""
    if isinstance(max_record_bytes, bool) or not isinstance(max_record_bytes, int) or max_record_bytes < 1:
        raise ValueError("max_record_bytes must be a positive integer")

    line_number = 0
    while True:
        raw = stream.readline(max_record_bytes + 2)
        if not raw:
            return
        line_number += 1

        if raw.endswith(b"\n"):
            content = raw[:-1]
            if content.endswith(b"\r"):
                content = content[:-1]
            if len(content) > max_record_bytes:
                yield ParseIssue(source_path, line_number, "record exceeds configured byte limit")
                continue
        else:
            if len(raw) > max_record_bytes:
                _discard_remainder(stream)
                yield ParseIssue(source_path, line_number, "record exceeds configured byte limit")
                continue
            content = raw

        if not content.strip():
            continue
        try:
            import json
            decoded = content.decode("utf-8")
            obj = json.loads(decoded)
        except UnicodeDecodeError:
            yield ParseIssue(source_path, line_number, "record is not valid UTF-8")
            continue
        except (ValueError, RecursionError):
            yield ParseIssue(source_path, line_number, "record is not valid bounded JSON")
            continue

        yield _normalize_object(obj, source_path, line_number)


__all__ = ["NormalizedEvent", "ParseIssue", "parse_jsonl", "safe_terminal_text"]
