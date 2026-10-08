#!/usr/bin/env python3
"""Turn one run's tcbench CSVs into the tracked report for a (profile, suite) cell.

Only the numbers that came from a verified run are published: every row here
was gated by `tcbench verify` (known values and full-output residuals) before
the timing pass started. The report repeats the run's provenance in its own
header, because a table that is copied into a discussion without its commit is
the thing this repository exists to stop.
"""
import argparse
import csv
import math
import pathlib
import statistics
import sys

import yaml


def read_rows(csv_paths):
    """Rows from the run CSVs, with the tensor size recovered from the filename.

    tcbench's rows carry the case, dtype, engine and thread count but not the
    nominal size; the file is named `<repeat>-<size>m-<threads>t.csv`, which is
    where the size comes from.
    """
    rows = []
    for p in csv_paths:
        stem = pathlib.Path(p).stem  # run0-16m-8t
        try:
            parts = stem.split("-")
            size_mib = float(parts[-2].rstrip("m"))
        except (ValueError, IndexError):
            raise SystemExit(f"cannot read the nominal size from {p}")
        with open(p) as f:
            body = [line for line in f if not line.startswith("#")]
        for row in csv.DictReader(body):
            row["size_mib"] = size_mib
            rows.append(row)
    return rows


def render(manifest, suite, rows, run_dir, root, providers):
    size_mib = manifest.get("run_spec", {}).get("sizes_mib", [])
    counts = manifest["threads"]["counts"]
    dtypes = manifest.get("run_spec", {}).get("dtypes", [])
    engines = manifest.get("run_spec", {}).get("engines", [])
    out = [
        f"# `{manifest['suite_id']}` on `{manifest['target_profile']}`",
        "",
        f"- tprims-rs commit: `{manifest['tprims']['commit']}`"
        + (" **(dirty)**" if manifest["tprims"]["dirty"] else ""),
        f"- features: `{', '.join(manifest['tprims']['features']) or 'default'}`",
        f"- harness commit: `{manifest['harness']['commit']}`",
        f"- hardware profile: `{manifest['target_profile']}`",
        f"- timestamp: `{manifest['timestamp']}`",
        f"- timing policy: v{manifest['timing_policy']['version']}, "
        f"{manifest['timing_policy']['statistic']} of {manifest['timing_policy']['repetitions']} reps, "
        f"priming {manifest['timing_policy']['minimum_untimed_priming_ms']} ms",
        f"- command: `{manifest['command']}`",
        f"- raw data: `{run_dir.relative_to(root)}/`",
        "## What was measured",
        "",
        f"- **Corpus `{suite['corpus']['name']}`** — {suite['corpus']['description']}",
        f"  Source: {suite['corpus']['source']}",
    ]
    for spot in suite["corpus"].get("known_blind_spots", []):
        out.append(f"  Known blind spot: {spot}")
    out += [
        f"- **Engines** — one row per engine in every table below:",
    ]
    for engine in engines:
        doc = suite["engines_doc"].get(engine)
        if doc is None:
            out.append(f"  - `{engine}` — (undocumented in the suite declaration)")
            continue
        out.append(f"  - `{engine}` — {doc['summary']}")
        # Prefer the identity recorded in *this run's* manifest over the suite's
        # generic sentence: a page should state what it actually measured.
        prov = providers.get(doc.get("provider"))
        if prov:
            bits = [prov["name"]]
            if prov.get("version"):
                bits.append(f"version {prov['version']}")
            if prov.get("commit"):
                bits.append(f"commit `{prov['commit']}`")
            line = ", ".join(bits)
            if prov.get("note"):
                line += f" — {prov['note']}"
            out.append(f"    Identity (as measured): {line}")
        else:
            out.append(f"    Identity: {doc['identity']}")
        if doc.get("caveat"):
            out.append(f"    Caveat: {doc['caveat']}")
    out += [
        f"- **Sizes** — the nominal tensor size per case in MiB. TCCG's sizing rule scales",
        f"  every extent of a case from it, so the same case at 1 MiB and 16 MiB has the",
        f"  same shape structure at different magnitudes.",
        f"- **dtypes** — `f64` is a real double, `c64` a complex double. The complex rows",
        f"  are the harder case for this library and are never likelier to look good.",
        f"- **Numbers** — milliseconds, best wall time per case and engine. See the timing",
        f"  policy for what is inside and outside the timed region.",
        "",
        "## Hardware",
        "",
        f"- CPU: `{manifest['host']['cpu']}`",
        f"- logical CPUs: `{manifest['host']['logical_cpus']}`",
        f"- L3: `{manifest['host']['l3']}`",
        f"- L3 domains: `{manifest['host'].get('l3_domains') or manifest['host']['l3']}`",
        f"- OS / arch: `{manifest['host']['os']}` / `{manifest['host']['arch']}`",
        f"- hostname: `{manifest['host']['hostname']}`",
        f"- CPU sets: " + ", ".join(f"{t}T -> `{c}`"
                                    for t, c in sorted(manifest["threads"]["cpu_sets"].items())),
        "",
        "Every row below passed `tcbench verify` (known values and full-output residual "
        "<= 1e-10) before timing. Values are the geometric mean over "
        + (f"{manifest['run_spec']['aa']} complete set repeats" if manifest['run_spec']['aa'] > 1
           else "the timed repetitions (this run made a single complete set, so it carries no A/A)")
        + " of the best wall time per engine.",
        "",
    ]
    for size in size_mib:
        for dtype in dtypes:
            for threads in counts:
                group = [r for r in rows
                         if float(r["size_mib"]) == float(size)
                         and r["dtype"] == dtype and int(r["threads"]) == threads]
                if not group:
                    continue
                out.append(f"## {size} MiB, {dtype}, {threads}T "
                           f"(CPU {manifest['threads']['cpu_sets'].get(str(threads), '?')})")
                out.append("")
                header = "| case | " + " | ".join(f"{e} (ms)" for e in engines) + " |"
                out.append(header)
                out.append("|" + "---|" * (len(engines) + 1))
                for case in sorted({r["case"] for r in group}):
                    cells = []
                    for e in engines:
                        s = [float(r["seconds"]) for r in group if r["case"] == case and r["engine"] == e]
                        cells.append(f"{statistics.geometric_mean(s) * 1e3:.4f}" if s else "-")
                    out.append(f"| `{case}` | " + " | ".join(cells) + " |")
                summary = []
                for e in engines:
                    s = [float(r["seconds"]) for r in group if r["engine"] == e]
                    summary.append(f"{statistics.geometric_mean(s) * 1e3:.4f}" if s else "-")
                out.append(f"| **geomean** | " + " | ".join(summary) + " |")
                out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = pathlib.Path(args.run_dir).resolve()
    manifest = yaml.safe_load((run_dir / "run.yaml").read_text())
    suite = yaml.safe_load((pathlib.Path(__file__).resolve().parent.parent
                            / "benchmarks/suites" / f"{manifest['suite_id']}.yaml").read_text())
    rows = read_rows(sorted(run_dir.glob("*.csv")))
    providers = {p["name"]: p for p in manifest.get("providers", [])}
    text = render(manifest, suite, rows, run_dir, pathlib.Path(__file__).resolve().parent.parent,
                  providers)
    (run_dir / "report.md").write_text(text)
    print(f"wrote {run_dir}/report.md from {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
