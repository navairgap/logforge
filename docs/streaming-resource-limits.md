# Streaming parser resource limits (proposed)

LogForge should remain predictable when reading large or malformed log files. Streaming input alone is not sufficient if one line or one parsed object can consume unbounded memory.

## Input bounds

Define configurable limits for:
- maximum bytes in one record or line;
- maximum nesting depth for structured values;
- maximum input file size when a caller requests a hard cap;
- maximum number of simultaneous input files;
- maximum diagnostic and exported-record size.

A reader should process one bounded record at a time and release references before advancing. If a line exceeds the record limit, report the file and line number and follow a documented policy: reject the record or skip to the next line. Do not silently parse a truncated prefix as a complete event.

## Memory and output

Do not accumulate an entire file just to calculate counts or time-window summaries. Keep counters and bounded aggregation state. Any feature that groups by a field with potentially unbounded unique values needs an explicit cap or an opt-in mode.

When a limit is reached, distinguish a partial summary from a complete one. Do not report totals as complete if records were skipped or processing stopped early.

## Untrusted content

Treat field names, message text, timestamps, and nested JSON as untrusted. Escape terminal control characters in human-readable output. Bound diagnostic text and avoid echoing an entire oversized record into an error message.

## Tests

Use generated temporary files with empty lines, a line just below the limit, a line exactly at the limit, an oversized line, deeply nested JSON, many unique grouping keys, and a multi-file input exceeding the concurrency cap. Verify memory use remains bounded by design and that summary metadata clearly reports skipped or partial input.