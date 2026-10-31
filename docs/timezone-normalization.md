# Timestamp and timezone normalization (proposed)

Timestamp normalization must preserve the meaning of the input and make assumptions visible. A local-looking timestamp without an offset is not inherently UTC.

## Parsing policy

- Accept RFC 3339 timestamps with an explicit offset as the preferred input form.
- Preserve the original timestamp string and source location when practical.
- Normalize a successfully parsed instant to UTC for comparisons and time-window aggregation.
- Treat a timestamp without an offset according to an explicit configured policy: reject it, mark it as timezone-unknown, or apply a caller-supplied timezone. Never silently use the machine's local timezone.
- Keep invalid and unavailable timestamps distinct.

## Daylight-saving transitions

A local time in a daylight-saving timezone may be ambiguous or may not exist. When a caller supplies a timezone for offset-free input, define how ambiguous and nonexistent local times are handled. Prefer rejecting ambiguous values unless the caller provides an explicit disambiguation policy. Record the chosen offset so downstream reports remain reproducible.

## Ordering and precision

Do not assume input order is chronological. Keep source order as a separate sequence attribute. Document timestamp precision and avoid inventing sub-second precision that the source did not provide. If two events normalize to the same instant, use source identifier and line number as deterministic tie-breakers for display, not as a claim about real-world event order.

## Tests

Cover UTC timestamps, positive and negative offsets, fractional seconds, offset-free input under each configured policy, invalid offsets, daylight-saving ambiguous and nonexistent times, and stable sorting for equal instants. Use fixed fixtures; tests must not depend on the host timezone.