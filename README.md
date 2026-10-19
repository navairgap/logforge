# logforge

A planned local tool for parsing structured logs and highlighting unusual patterns.

> **Status: design stage.** This repository currently contains documentation only; parsing, storage, and alerting are not implemented yet.

## Goal

Make it easier to inspect application and service logs without requiring a hosted analytics platform.

## Initial scope

- Read newline-delimited JSON logs first.
- Normalize timestamps, severity, source, and message fields when available.
- Report malformed records with file and line number.
- Summarize event counts and error rates over a selected time range.
- Export results in a stable format suitable for shell pipelines.

Additional formats such as syslog or common web-server logs should be added only with fixtures and tests.

## Design constraints

- Process files locally by default; no telemetry or remote upload.
- Bound memory use for large files by streaming input.
- Treat log messages as untrusted data; escape them in terminal output.
- Make timezone assumptions explicit.
- Avoid claiming anomaly detection until a baseline and evaluation method are defined.

## Planned milestones

- [ ] Choose and document the implementation language and dependency policy.
- [ ] Define a normalized event schema.
- [ ] Add parser fixtures for valid, malformed, and incomplete records.
- [ ] Implement streaming summaries and deterministic output.
- [ ] Add large-file tests and document performance measurements.

## Status honesty

No parser, database, rotation engine, benchmark, or alerting integration is available yet. The README will be updated as those milestones are implemented.

## License

MIT. See [LICENSE](LICENSE).
