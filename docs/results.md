# Result layout

`suite_id` identifies the workload; `target_profile` identifies the machine
(`benchmarks/profiles.yaml`). They are the two axes of every cell.

```text
data/results/<profile>/<suite>/<timestamp>/   raw: run.yaml, verify-*.txt, run*.csv, *.guard, report.md
result/<profile>/<suite>.md                   the latest full-coverage report for the cell
result/INDEX.md                               generated: commit, date, coverage, status per cell
```

## run.yaml

Validated against `schemas/benchmark-run.schema.json` before it is written.
It records:

- the profile, suite, suite file, timestamp and the exact command;
- `tprims`: path, commit, dirty state, features of the checkout that was
  measured and that the harness was built from;
- `harness`: commit and dirty state;
- `host`: CPU, logical CPU count, OS, arch, L3 geometry;
- `threads`: the counts, the CPU set used for each, and the thread environment
  variables in force;
- `timing_policy`: version, priming, statistic, repetitions;
- `providers`: what was compared against, with versions or commits;
- `guards`: the idle window, the busy threshold, the attempt budget, the log files;
- `run_spec`: what this run covered, and whether that is the whole declaration.

## Index and staleness

`result/INDEX.md` is generated. Its point is that reports are self-describing
but the *set* of them was not: with one tracked file per cell, a cell that has
not been re-measured keeps an old file, and a reader sees a commit hash and a
table without being able to tell whether that cell reflects the current library.

`status` is computed against `pins/tprims-rs.rev`:

| status | meaning |
|---|---|
| `missing` | no run recorded for this cell |
| `current` | measured at the reference revision, or at a descendant |
| `N behind` | N commits touching the suite's `invalidated_by` paths lie between the measured revision and the reference |
| `stale` | as `behind`, but N exceeds the suite's `stale_after` |
| `dirty` | the measured checkout had uncommitted changes; never comparable |
| `diverged` | the measured revision is not an ancestor of the reference |

`behind` counts *invalidating* commits, not raw distance: a suite declaring only
`crates/` is not out of date because a document changed. `coverage` is `full`
when the cell was measured over the suite's whole declared spec and `partial`
otherwise; a partial run never displaces a full one.
