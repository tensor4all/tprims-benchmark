# Timing policy, version 1

Recorded in every `run.yaml` as `timing_policy`. A run carries the version in
force when it was taken; do not compare ratios across versions, and do not use
an earlier version's numbers to assess a later library revision.

## What is timed

Steady-state operation execution. Inputs, layouts, plans, pools and provider
handles are prepared before the clock starts. The clock stops after the
operation and its completion synchronisation, with outputs still alive.

## Priming

At least 0.5 s of untimed, time-based priming per arm, and the same amount on
every arm. A fixed call count is not equivalent: after an idle gate this host
reads up to 25% low for the first 1-2 s of sustained AVX-512 work (measured:
39.8 GFLOP/s for a kernel that reads 52.6 once warm). A count-based warm-up also
biases a ratio when the two arms have different durations.

## Statistic and repetitions

`best` wall time per engine and case, over 5 repetitions, with the complete set
repeated for A/A when a comparison is being made. A scan flags suspects; only a
complete paired run makes a performance claim.

## Guarding the host

Every measurement runs through `benchmarks/scripts/pinned.sh` of the measured
checkout: `taskset` to the declared CPU set, a 3-second `/proc/stat` idle window,
at most 5% busy before and after, 3 attempts. A spoiled run is discarded, not
published.

## What a report may and may not claim

A report states the revision, the host, the coverage and the guards, and it is a
claim about *that* cell. It is not evidence about a population the run did not
contain: a corpus whose cases all have unit batch extent says nothing about
per-batch-element cost, and the index's `coverage` column is the mechanism that
keeps that visible.
