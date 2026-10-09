# Work log

Design decisions, what was rejected, and what is still open. Measurements live
in `result/`; this file holds the reasoning.

## Why the campaign is a separate repository

`tprims-rs` had one tracked report per `(profile, suite)` under a results
directory. Each file was self-describing, but the set of them was not: a cell
that had not been re-measured kept its old file, and a reader saw a commit hash
and a table without being able to tell whether it reflected the current library.
Staleness was carried in prose in the README, which no check can fail.

That is the same class of mistake that produced a retracted performance claim
during this work: two sides of a comparison measured at effectively different
revisions, and no way to see it from the numbers.

## Decisions

**The harness is not moved.** `tprims-benchmark` builds `tcbench` out of a
pinned checkout of `tprims-rs` with `--manifest-path`, rather than owning a
crate. Two reasons, in order of weight:

1. A result's recorded commit has to describe *both* the library and the
   harness. Building the harness from the measured checkout makes that true by
   construction; a harness living here could be built against a different
   revision of the library than the one it was written for.
2. A path dependency on a package that belongs to another workspace does not
   resolve: Cargo applies `workspace = true` inheritance against the *consuming*
   workspace root, so `extern/tprims-rs/benchmarks` failed to load with
   `stub: dependency.strided-basic was not found in workspace.dependencies`.
   This was verified, not assumed.

**Revision pinning without published crates.** `extern/tprims-rs` is a symlink
produced by `setup_extern_deps.sh`; `build_for_tprims_rev.sh` re-points it and
builds into `target/tprims-rev/<rev12>[-dirty]` with `RUSTC_WRAPPER=` cleared.
Baseline and candidate can never share compiled library artifacts. This came
from a concrete failure: a measurement was once taken from a binary that did not
contain the change under test, because two source trees shared a target
directory.

**Pages are keyed by revision, not by cell.** `result/<profile>/<suite>/<rev>.md`.
Measuring a new commit adds a page; the previous one is not overwritten, so the
tree keeps the history the index links to. A dirty checkout gets its own page.

**`behind` counts invalidating commits.** Each suite declares `invalidated_by`
source paths and a `stale_after` threshold. A documentation change does not make
a kernel result stale, and a counting rule that could not tell the difference
would be ignored in practice.

**Coverage is a column, not an apology.** The campaign is not run in full on
every profile for every commit. A partial run is recorded, marked `partial`, and
never displaces a full-coverage page.

## Failures found and fixed while building this

**The index was not deterministic.** It stamped the wall clock, so a freshly
generated file never matched the committed one and `--check` could not be exact;
CI failed on it. It now records the newest *recorded run* timestamp.

**Manifests recorded the measuring host's path.** `tprims.path` was
`/home/shinaoka/...`, so a committed manifest could not be verified anywhere
else and CI rightly rejected it. A manifest that only validates on the machine
that produced it is not evidence. `tprims` now requires `url` and `commit`, and
treats the local path as informational `measured_path`; validation resolves the
commit in a checkout that exists *here*, with a negative control that an
unresolvable commit fails.

**A partial run could look as good as a full one.** The first version of the
index showed commit/date/status but not what the run had covered. Found by
recording a smoke run and noticing it was indistinguishable from the full one.

## Open, not done

- **A corpus derived from application shape logs.** `tenferro-benchmark` already
  produces one (`TPRIMS_SHAPE_LOG` plus its `scripts/tprims_shape_corpus.py`,
  keeping shape groups up to a 95% time share plus the most frequent others).
  Re-implementing that consumer here would duplicate a tool owned by the
  repository that produces the logs; the right move is to consume its output as
  another declared suite. Until then, the TCCG corpus is the only workload, and
  it has a known blind spot: all 49 cases have unit batch extent, so
  per-batch-element cost is invisible in it.
- **The campaign is one host again, deliberately.** `epyc-cpu` was declared from the
  first commit as the second profile, an old shared 64-core workstation used for spot
  checks, and it was never measured: the cell would cost a full run on a machine whose
  load the campaign does not control. It is retired (2026-10-09) rather than left as a
  permanent `missing` row. A future machine is a new profile with its own name and its
  own L3 description, not a revival of this one.
- **`tprims.version` is recorded as null.** `tprims-rs` is unpublished; the field
  exists so a versioned project's pages are keyed by version as well as commit.
- **TBLIS is retired from the declaration.** It was the third-party reference arm,
  but it needs an external install (`TBLIS_ROOT`) and an unpublished local
  revision to say what it measured, which tied every cell to one host's
  installation. The `zen5-cpu` cell records `plan`, `packed` and `upstream`; the
  page that did measure TBLIS keeps its column, because evidence is immutable.
  The harness keeps the feature, so a cell can declare it again. tenferro-rs
  retired its own TBLIS extension in the same week (tenferro-rs#2004).

## A run discarded, and one rule tightened

A measurement was taken while `extern/tprims-rs` sat on the merged-PR head
`1e0bf3c`, not on `main` (the merge was a squash, so the head is not an ancestor
of `main`). Its page would have been `diverged` against the reference and failed
the index check for a required cell. The run and its page were discarded rather
than published, and the pin now points at `main`; the discarded revision is
recorded here because the fact that it happened is worth more than the file.

`invalidated_by` listed `benchmarks/**`, which made a README edit mark every
measurement stale. It now lists only paths whose change can alter a measured
result: the three library crates, the harness directory, the shared harness
library, and the two manifests that decide features and dependencies. A rule
that cannot tell a documentation change from a kernel change is a rule nobody
follows.

## Evidence is immutable, declarations are not

Adding the `tblis` arm to the declaration broke a manifest that had been correct
when it was written: `validate_run.py` recomputed `covers_declared_suite`
against the *current* declaration and disagreed with the recorded value. CI
caught it, and the fix is not to relax the check but to record what the manifest
was measured under.

`run.yaml` now carries `suite_sha256`, the declaration's hash at measurement
time. A manifest whose hash differs from today's declaration is checked for what
can be checked (schema, profile, suite, CPU sets, resolvable commit) and noted as
drifted; its declaration-derived claims are not re-judged, because the
declaration it was written against cannot be reconstructed. Manifests recorded
before the field existed carry the same notice.

`coverage` in the index now relates a page to the *current* declaration:
`full`, `partial`, or `declaration-changed` when the declaration moved after the
measurement. The older page for `0aeb77dd6728` shows the last of these, which is
the truth: it was measured against a three-arm declaration, and today's has four.
The newest page was re-measured after the declaration settled so that it is
`full`, not because the earlier number was wrong. Retiring the TBLIS arm moves
that newest page back to `declaration-changed` again, which is the same
statement about a different pair of declarations: four arms then, three now.

The same change fixed a smaller semantic bug: `harness.commit` had been
recording the *measured* checkout's commit, which merely duplicated
`tprims.commit`. It now records this repository's commit, which is what
distinguishes one reporting pipeline from another.

## The manifest stopped stating what the harness did not do

Two claims in every `run.yaml` were the recorder's own defaults rather than the
run's report: `minimum_untimed_priming_ms` and the guard's window, threshold and
attempt budget. They happened to be right, which is the worst kind of wrong — a
reader had no way to tell a stale record from a live one, and a `--prime-ms` or
`PINNED_*` override during a run would have made the manifest describe a policy
nobody applied. tprims-rs had the other half of the same gap: the campaign
recorded 500 ms of time-based priming while the harness did exactly one warm-up
call (tprims-rs#78), and the guard checked the declared CPUs without their SMT
siblings, so a busy sibling could share the measured physical core invisibly
(tprims-rs#79).

Both sides now meet in the middle:

- the measured checkout's harness prints what it applies (`N ms priming` is on
  `run`'s banner) and its guard echoes the policy it used (`pinned.sh: cpus=...
  idle_window=3s max_busy=0.05 retries=3`) together with the per-CPU report that
  names each SMT sibling it checked;
- the recorder passes `--prime-ms`, keeps each run's stdout as
  `run<N>-<size>m-<T>t.out`, reads the priming and the guard policy out of those
  two lines, requires every run in a cell to agree, and **refuses a measured
  checkout that reports neither** — that is the check that keeps the pin honest,
  because a checkout predating those banners cannot produce a trustworthy
  manifest;
- `guards` gained `outputs` (the retained stdout) and `notes` (the sibling
  coverage), both optional, so every previously recorded manifest still
  validates.

The pin moved to `e42f6af` and the `zen5-cpu`/`tcbench` cell was re-measured
under the three-arm declaration, so the cell is `full` and `current` again and
the first cell in this repository whose manifest's priming and guard are read
back from the run. What that cell does *not* establish: it is a single complete
set (`aa: 1`), so it carries no A/A, and the retired TBLIS column in the older
page stays as measured.

## 2026-10-09 the campaign loses its third arm, its third width and its second size

Four retirements, all of them about paying twice for the same answer.

- **TBLIS is retired** (`tcbench`'s fourth arm; the declaration change is the
  `2026-10-09` commit "declaration: retire the TBLIS arm", and the harness followed).
  It was the third-party reference, but it needed an external install and an
  unpublished local revision to say what it measured. It comes back pinned by release
  tag for the per-shape suite, where an independent reference earns its place, and not
  for `tcbench`.
- **The `upstream` arm (tensorprimitives-rs) is retired everywhere**, code and Cargo
  feature with it. It is the project this library was extracted from, so it is a
  lineage baseline rather than an independent one, and the measured cells say it
  nearly always loses: on the per-shape corpus `tprims [plan]` is ahead in 42 of 42
  rows, and on the TCCG corpus in 283 of 294. The exceptions are small and are recorded
  rather than hidden: `ij-ik-kj` at 1T, where the planner takes 1.26x the upstream time,
  and twelve more rows within 1.15x. Losing the arm loses the only external comparison
  `tcbench` had; the per-shape suite keeps TBLIS for that.
- **`tcbench` is measured at one size, two widths and two arms** (`tprims [plan]`,
  `tprims [packed]`). Its 49 rank-3-to-6 contractions are the only irregular-stride
  work in the campaign, so the corpus stays; the 8-thread width, the 1 MiB size and the
  third arm each cost about a third of a run to answer a question another row already
  answers. The first cell under the old declaration took 30 minutes
  (`20261009T080245Z`: 08:02:45 to 08:32:16), of which 7.4 minutes was priming and
  42 seconds one `verify` at 16 MiB; the reduced cell is a few minutes.
- **`lukas` is renamed `per-shape`.** The suite was named after the person whose figure
  it reconstructs, which is not what an identifier is for: the corpus's own property is
  that its cases *are* the shapes, one size each. The attribution stays where provenance
  belongs, in the suite's `corpus.source` field, `experiments/three-engine-contract/`
  and the harness's own documentation.

Engine columns are now labelled for a reader (`tprims [plan]`, `tprims [packed]`,
`tblis`) while the CSVs keep the machine-readable ids (`plan`, `packed`, `tblis`): a
suite declares the label, `report_run.py` prints it, and nothing about the data
changes. The old `lukas` page and its raw run are removed rather than orphaned — the
suite id no longer exists, so no index would reference them, and the commit that
created them keeps their history.
