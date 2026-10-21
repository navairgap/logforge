# parser fixture guidelines

Maintain tiny fixtures with expected output for each supported format. Include malformed JSON, blank lines, missing timestamps, unknown severity, Unicode, and oversized lines. Preserve source file and line number in parse errors. Define timezone handling explicitly. Bound memory for long records, keep input order stable unless sorting is requested, and ensure exported JSON escapes control characters. Never use production logs containing tokens or personal data as fixtures.
