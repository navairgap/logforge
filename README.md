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

## Rotation strategy

Files rotate on size (`max_bytes`, default 10MB) or on schedule, whichever comes first. The active file is never compressed; rotated files are gzip'd and pruned to `keep` (default 5). Set `keep: 0` to disable pruning.

## Development

```bash
git clone https://github.com/navairgap/logforge && cd logforge
cargo test            # unit + proptest suite
cargo bench           # rotation throughput
```

PRs welcome; keep the public API surface small on purpose.


## Comparison

vs logrotate: smaller, one binary, no cron needed. vs fluent-bit: logforge writes files, not pipelines. it's the right size for the problem it solves.


## Exit codes

`0` rotation happened cleanly. `1` disk error during rotation — check permissions on the target directory. `2` config unparseable.

## Project layout

```
src/
  rotate.c    — size/schedule triggers and file cutting
  compress.c  — gzip of rotated files, prune policy
  config.c    — toml parsing and defaults
  main.c      — wiring
include/      — public header
```

## Project layout

```
src/
  rotate.c    — size/schedule triggers and file cutting
  compress.c  — gzip of rotated files, prune policy
  config.c    — toml parsing and defaults
  main.c      — wiring
include/      — public header
```
