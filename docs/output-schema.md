# output schema

Define normalized fields for timestamp, severity, source, message, and original line location. Preserve unknown fields when feasible rather than silently discarding evidence. Specify timestamp timezone behavior and severity normalization. Keep malformed records visible with file and line numbers. Bound record size, escape control characters on output, and ensure JSON exports can be parsed by standard tools.

## Source provenance

Each normalized record should retain a source identifier and line number so a result can be traced to its original input. If parsing combines several source records, represent the contributing locations as a bounded list instead of dropping provenance. Keep the original raw line optional and opt-in because it may contain credentials or personal data; the normalized message must not accidentally leak those values into default logs.
