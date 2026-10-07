#!/usr/bin/env python3
"""Publish one recorded run as the cell's report, then regenerate the index.

This is the only place the publish rule lives, so `record_run.py` and a manual
re-publish after a report-format change cannot disagree:

* a run that did not cover the suite's declared spec never displaces the
  published report;
* the published file is a copy of the run's own report, so the report and the
  raw data it came from cannot drift apart.
"""
import argparse
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def publish(run_dir):
    manifest = yaml.safe_load((run_dir / "run.yaml").read_text())
    report = ROOT / "result" / manifest["target_profile"] / f"{manifest['suite_id']}.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    covers = manifest["run_spec"]["covers_declared_suite"]
    header = (f"<!-- generated from {run_dir.relative_to(ROOT)}/report.md "
              f"by scripts/publish_report.py; the report below is the source of truth -->\n\n")
    if covers or not report.exists():
        report.write_text(header + (run_dir / "report.md").read_text())
        print(f"published {report.relative_to(ROOT)} from {run_dir.relative_to(ROOT)} "
              f"(coverage={'full' if covers else 'partial'})")
    else:
        print(f"recorded {run_dir.relative_to(ROOT)} without replacing the published report "
              f"(partial run, and a published report already exists)")
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_index.py"), "--write"], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    publish(pathlib.Path(args.run_dir).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
