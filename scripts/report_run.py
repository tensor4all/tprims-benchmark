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


def render(manifest, suite, rows, run_dir):
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
        f"- host: `{manifest['host']['cpu']}` ({manifest['host']['logical_cpus']} logical)",
        f"- timestamp: `{manifest['timestamp']}`",
        f"- timing policy: v{manifest['timing_policy']['version']}, "
        f"{manifest['timing_policy']['statistic']} of {manifest['timing_policy']['repetitions']} reps, "
        f"priming {manifest['timing_policy']['minimum_untimed_priming_ms']} ms",
        f"- command: `{manifest['command']}`",
        f"- raw data: `{run_dir}/`",
        "",
        "Every row below passed `tcbench verify` (known values and full-output residual "
        "<= 1e-10) before timing. Values are the geometric mean over repetitions and "
        "A/A repeats of the best wall time per engine.",
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
    run_dir = pathlib.Path(args.run_dir)
    manifest = yaml.safe_load((run_dir / "run.yaml").read_text())
    suite = yaml.safe_load((pathlib.Path(__file__).resolve().parent.parent
                            / "benchmarks/suites" / f"{manifest['suite_id']}.yaml").read_text())
    rows = read_rows(sorted(run_dir.glob("*.csv")))
    text = render(manifest, suite, rows, run_dir)
    (run_dir / "report.md").write_text(text)
    print(f"wrote {run_dir}/report.md from {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
