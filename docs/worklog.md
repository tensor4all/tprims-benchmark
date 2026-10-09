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
- **Only one profile has been measured.** `zen5-cpu`. `epyc-cpu` is declared as
  optional and shows as `missing`, which is the intended presentation.
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
