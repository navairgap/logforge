# logforge

Structured log parser and anomaly flagger

> 🚧 **Status: planning** — architecture and README first, code next.

## Why

Servers drown in logs and starve for insight. logforge parses structured logs (JSON, syslog, combined), extracts patterns, and flags the anomalies — error spikes, new error types, weird IPs — before humans notice.

## Planned features

- Parse JSON/syslog/common log formats into a queryable store
- Baselines per-service error rates; alerts on spikes
- Detect never-before-seen error signatures
- CLI + scheduled reports, all local (SQLite backend)

## Stack

`python` `sqlite` `pandas`

## Notes

Anomaly = statistical outlier vs your own baseline, not ML magic.

## License

MIT, see [LICENSE](LICENSE).

---
maintained · verified 2026-09-30
---
maintained · verified 2026-10-01
---
maintained · verified 2026-10-02
