# parser fixture guidelines

Maintain tiny fixtures with expected output for each supported format. Include malformed JSON, blank lines, missing timestamps, unknown severity, Unicode, and oversized lines. Preserve source file and line number in parse errors. Define timezone handling explicitly. Bound memory for long records, keep input order stable unless sorting is requested, and ensure exported JSON escapes control characters. Never use production logs containing tokens or personal data as fixtures.

## Offset semantics

Define whether reported positions are byte offsets or decoded-character offsets. Prefer byte offsets when pointing into the original UTF-8 file, because character indices do not map directly to file positions for multi-byte characters. Include fixtures with accented text and emoji before a malformed field, and assert that diagnostics identify the correct source line and byte position without printing the full record.
