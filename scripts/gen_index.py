#!/usr/bin/env python3
"""Generate result/INDEX.md: which commit each published cell was measured at.

The failure this exists to prevent: with one tracked report per
(profile, suite), a cell that has not been re-measured keeps its old file, and
a reader -- human or agent -- sees a commit hash and a table and cannot tell
whether that cell reflects the current library or something weeks old. Reports
are self-describing; the *set* of them was not, so staleness leaked into prose
in the README.

So the index makes it structural and machine-checkable:

  status      meaning
  ----------  ---------------------------------------------------------------
  missing     no run recorded for this cell
  current     measured at the reference revision, or at a descendant
  N behind    N commits touching the suite's `invalidated_by` paths lie between
              the measured revision and pins/tprims-rs.rev
  stale       as `behind`, but N exceeds the suite's `stale_after`
  dirty       the measured checkout had uncommitted changes; never comparable
  diverged    the measured revision is not an ancestor of the reference

`behind` counts invalidating commits, not raw distance: a suite that only
touches `crates/` is not out of date because a doc changed.
"""
import argparse
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "result/INDEX.md"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def git(checkout, *args):
    out = subprocess.run(["git", "-C", checkout, *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {checkout}: {out.stderr.strip()}")
    return out.stdout.strip()


def reference_rev():
    return (ROOT / "pins/tprims-rs.rev").read_text().strip()


def invalidating_distance(checkout, measured, reference, paths):
    """Commits touching `paths` that are in `reference` but not in `measured`."""
    if measured == reference:
        return 0
    try:
        git(checkout, "merge-base", "--is-ancestor", measured, reference)
    except RuntimeError:
        return None
    out = git(checkout, "rev-list", "--count", f"{measured}..{reference}", "--", *paths)
    return int(out or 0)


def collect():
    profiles = [p["name"] for p in load(ROOT / "benchmarks/profiles.yaml")["profiles"]]
    suites = [load(f) for f in sorted((ROOT / "benchmarks/suites").glob("*.yaml"))]
    reference = reference_rev()
    checkout = ROOT / "extern/tprims-rs"
    have_checkout = (checkout / ".git").exists()
    rows = []
    for suite in suites:
        wanted = list(suite["required_profiles"]) + [p for p in suite.get("optional_profiles", [])]
        for profile in wanted:
            cell = ROOT / "data/results" / profile / suite["id"]
            manifests = sorted(cell.glob("*/run.yaml")) if cell.is_dir() else []
            # Publish the newest run that covered the declared suite; a partial
            # run is still recorded, but it must not displace a full one, and
            # either way the coverage is stated rather than implied.
            full = []
            for m in manifests:
                data = load(m)
                if data.get("run_spec", {}).get("covers_declared_suite"):
                    full.append(m)
            coverage = "full" if full else ("partial" if manifests else "-")
            if full:
                manifests = full
            if not manifests:
                rows.append(dict(suite=suite["id"], profile=profile, commit=None, date=None,
                                 status="missing", report=None, coverage="-",
                                 required=profile in suite["required_profiles"]))
                continue
            run_dir = manifests[-1].parent
            m = load(manifests[-1])
            commit = m["tprims"]["commit"]
            report = ROOT / "result" / profile / f"{suite['id']}.md"
            status, distance = "unknown", None
            if m["tprims"]["dirty"]:
                status = "dirty"
            elif have_checkout:
                distance = invalidating_distance(checkout, commit, reference, suite["invalidated_by"])
                if distance is None:
                    status = "diverged"
                elif distance == 0:
                    status = "current"
                elif distance > suite["stale_after"]:
                    status = "stale"
                else:
                    status = f"{distance} behind"
            rows.append(dict(suite=suite["id"], profile=profile, commit=commit[:12],
                             timestamp=m["timestamp"],
                             date=m["timestamp"][:10], status=status if distance is None else status,
                             report=str(report.relative_to(ROOT)) if report.exists() else None,
                             coverage=coverage,
                             required=profile in suite["required_profiles"],
                             behind=distance, stale_after=suite["stale_after"]))
    return rows, reference, profiles, [s["id"] for s in suites], have_checkout


def render(rows, reference, generated):
    """The text of the index.

    `generated` is the newest *recorded* run's timestamp, not the wall clock:
    a generated file that changes on every invocation cannot be checked in and
    verified by CI, and the interesting fact is when the data was collected,
    not when the file was rendered.
    """
    out = [
        "# Result index",
        "",
        "Generated by `scripts/gen_index.py`. **Do not edit by hand**; CI checks that",
        "this file is what the generator produces.",
        "",
        f"- Reference revision (`pins/tprims-rs.rev`): `{reference}`",
        f"- Newest recorded run: `{generated}`",
        "- `behind` counts commits touching the suite's `invalidated_by` paths, not raw distance.",
        "",
        "| suite | profile | commit | date | coverage | status | report |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        mark = "" if r.get("required") else " (optional)"
        link = f"[{r['report']}]({r['report'].replace('result/', '')})" if r["report"] else "-"
        out.append(f"| `{r['suite']}` | `{r['profile']}`{mark} | `{r['commit'] or '-'}` | "
                   f"{r['date'] or '-'} | {r['coverage']} | {r['status']} | {link} |")
    out.append("")
    out.append("`missing` is a normal cell, not an error: the campaign is not run on")
    out.append("every profile for every commit. It becomes an error only for a profile a")
    out.append("suite lists as `required`.")
    out.append("")
    out.append("`coverage` is `full` when the cell was measured over the suite's whole")
    out.append("declared spec, `partial` when it was a subset. A partial run never displaces")
    out.append("a full one: the index prefers the newest full-coverage run for the cell.")
    out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if the committed file differs, or a required cell is missing/stale")
    ap.add_argument("--fail-on-stale", action="store_true",
                    help="also fail when a required cell is stale")
    ap.add_argument("--write", action="store_true", help="write result/INDEX.md")
    args = ap.parse_args()

    rows, reference, _profiles, _suites, have_checkout = collect()
    stamps = [r["timestamp"] for r in rows if r.get("timestamp")]
    generated = max(stamps) if stamps else "none"
    text = render(rows, reference, generated)

    problems = []
    if not have_checkout:
        problems.append("extern/tprims-rs is absent, so currency cannot be computed (run scripts/setup_extern_deps.sh)")
    for r in rows:
        if not r.get("required"):
            continue
        if r["status"] == "missing":
            problems.append(f"required cell {r['suite']}/{r['profile']} has no run")
        elif r["status"] == "dirty":
            problems.append(f"required cell {r['suite']}/{r['profile']} was measured from a dirty checkout")
        elif r["status"] == "diverged":
            problems.append(f"required cell {r['suite']}/{r['profile']} is not an ancestor of the reference")
        elif r["status"] == "stale" and args.fail_on_stale:
            problems.append(f"required cell {r['suite']}/{r['profile']} is stale ({r['behind']} invalidating commits > {r['stale_after']})")

    if args.write:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(text)
        print(f"wrote {INDEX.relative_to(ROOT)}")
        return 0

    if args.check:
        if not INDEX.exists() or INDEX.read_text() != text:
            problems.append("result/INDEX.md is out of date; run scripts/gen_index.py --write")
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        return 1 if problems else 0

    print(text)
    for p in problems:
        print(f"note: {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
