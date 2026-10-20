# Normalized log event (draft v1)

LogForge should normalize supported source formats into a small common event shape while preserving enough source context to diagnose parsing problems. This is a proposal until parsing is implemented.

## Example

```json
{
  "schema_version": 1,
  "timestamp": "2026-10-20T12:00:00Z",
  "severity": "error",
  "source": "api",
  "message": "request failed",
  "attributes": { "status_code": 503 },
  "source_location": { "path": "service.jsonl", "line": 42 }
}
```

## Rules

- Preserve the original timestamp text when parsing fails, and expose a parse warning rather than silently substituting the current time.
- Normalize known severities to `trace`, `debug`, `info`, `warn`, `error`, or `fatal`; retain unknown source values in a separate field.
- `message` is untrusted text. Escape control characters before terminal output and never interpret ANSI escape sequences from input as formatting.
- Store source file and line number for malformed records. Continue parsing subsequent lines when safe.
- Stream input line by line so large files do not need to fit in memory.
- Keep arbitrary fields under `attributes` and cap nesting/record size to avoid resource exhaustion.

## Output determinism

For identical input and options, summary output should be stable. Document timezone handling and sort keys explicitly; do not rely on map iteration order.

## Tests

Fixtures should cover valid JSONL, missing fields, invalid timestamps, unknown severity, malformed lines between valid records, oversized records, control characters, and empty files.
