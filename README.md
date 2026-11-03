# logforge

A local tool for parsing structured log lines and highlighting unusual patterns.

> **Current state: JSONL parser prototype.** A bounded, standard-library JSONL reader and v1 event normalizer are implemented with deterministic unit tests. Summaries, anomaly scoring, rotation, and alerting are not implemented.

## First parser

The parser streams from a binary file handle, enforces a byte limit while reading each physical line, reports malformed lines with a source path and line number, and continues at the next safe line boundary. Timestamps with explicit offsets are normalized to UTC. Timezone-free or invalid timestamps retain their source text and carry a warning rather than being silently interpreted as local time or UTC. Unknown severity values remain available in severity_raw.

Run the focused tests with:

    python -m unittest discover -s tests -v

## Scope and safety

Input is local by default. Log messages are untrusted text; use safe_terminal_text before displaying them in a terminal. Do not upload logs or include production logs with secrets or personal data in fixtures.

## Remaining work

- [ ] Add summary counts and error-rate windows.
- [ ] Define deterministic aggregation and export commands.
- [ ] Add parser fixtures for deeper nested attributes and additional timestamp formats.
- [ ] Add large-file memory and throughput measurements.
- [ ] Consider other source formats only with fixtures and tests.

## License

MIT. See [LICENSE](LICENSE).
