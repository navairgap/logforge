import io
import unittest

from logforge import NormalizedEvent, ParseIssue, parse_jsonl, safe_terminal_text


class LogForgeParserTests(unittest.TestCase):
    def test_normalizes_offset_timestamp_and_warning_severity(self):
        stream = io.BytesIO(
            b'{"timestamp":"2026-10-20T14:30:00+02:00","level":"warning",'
            b'"service":"api","message":"slow","status":503}\n'
        )
        event = next(parse_jsonl(stream, "api.jsonl"))
        self.assertIsInstance(event, NormalizedEvent)
        self.assertEqual(event.timestamp, "2026-10-20T12:30:00.000000Z")
        self.assertEqual(event.severity, "warn")
        self.assertEqual(event.attributes["status"], 503)
        self.assertEqual(event.line_number, 1)

    def test_timezone_free_timestamp_is_preserved_not_assumed(self):
        stream = io.BytesIO(b'{"timestamp":"2026-10-20T12:30:00","message":"x"}\n')
        event = next(parse_jsonl(stream))
        self.assertIsNone(event.timestamp)
        self.assertEqual(event.timestamp_raw, "2026-10-20T12:30:00")
        self.assertIn("no local timezone", event.timestamp_warning)

    def test_malformed_line_does_not_hide_following_records(self):
        stream = io.BytesIO(b'{"message":\n{"message":"after"}\n')
        records = list(parse_jsonl(stream, "mixed.jsonl"))
        self.assertIsInstance(records[0], ParseIssue)
        self.assertEqual(records[0].line_number, 1)
        self.assertIsInstance(records[1], NormalizedEvent)
        self.assertEqual(records[1].message, "after")
        self.assertEqual(records[1].line_number, 2)

    def test_oversized_line_is_drained_before_next_record(self):
        stream = io.BytesIO(b'{"message":"' + b"x" * 40 + b'"}\n{"message":"ok"}\n')
        records = list(parse_jsonl(stream, "large.jsonl", max_record_bytes=24))
        self.assertIsInstance(records[0], ParseIssue)
        self.assertIn("byte limit", records[0].reason)
        self.assertEqual(records[1].message, "ok")

    def test_control_characters_are_rendered_visibly(self):
        self.assertEqual(safe_terminal_text("a\x1b[31m\n"), "a\\x1b[31m\\n")

    def test_rejects_invalid_limit(self):
        for value in (0, -1, True, "64"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                list(parse_jsonl(io.BytesIO(), max_record_bytes=value))


if __name__ == "__main__":
    unittest.main()
