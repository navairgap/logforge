# output schema

Define normalized fields for timestamp, severity, source, message, and original line location. Preserve unknown fields when feasible rather than silently discarding evidence. Specify timestamp timezone behavior and severity normalization. Keep malformed records visible with file and line numbers. Bound record size, escape control characters on output, and ensure JSON exports can be parsed by standard tools.
