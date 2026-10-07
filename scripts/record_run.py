#!/usr/bin/env python3
"""Record one (profile, suite) run: build at a revision, verify, measure, publish.

Order matters and is enforced here:

1. the harness is built out of the *measured checkout*, into a target directory
   keyed by its revision;
2. `tcbench verify` runs for every size/thread count before any timing, and a
   mismatch aborts the run (nothing is published from an unverified run);
3. each measurement goes through the pinned, idle-checked protocol script that
   belongs to the same revision;
4. the manifest is validated against its schema *before* it is written, and the
   recorded commit must resolve in the checkout it names.
"""
import argparse
import datetime
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def sh(cmd, **kw):
    print(f"+ {' '.join(str(c) for c in cmd)}", file=sys.stderr)
    return subprocess.run([str(c) for c in cmd], check=True, text=True,
                          capture_output=True, **kw)


def git(dir_, *args):
    return subprocess.run(["git", "-C", str(dir_), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def build(checkout):
    env_file = ROOT / "target/pin.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    sh([ROOT / "scripts/build_for_tprims_rev.sh", checkout, env_file, "tcbench"])
    pin = {}
    for line in env_file.read_text().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            pin[k] = v.strip().strip("'\"")
    return pin


def host_info(profile_name, profiles):
    profile = next(p for p in profiles if p["name"] == profile_name)
    lscpu = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
    logical = next((int(l.split(":")[1].strip()) for l in lscpu.splitlines()
                    if l.startswith("CPU(s):")), 0)
    l3 = next((l.split(":", 1)[1].strip() for l in lscpu.splitlines()
               if l.startswith("L3 cache:")), None)
    return {
        "hostname": platform.node(),
        "cpu": profile["cpu"],
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "logical_cpus": logical or profile["logical_cpus"],
        "l3": l3 or profile.get("l3"),
        "notes": profile.get("description"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile")
    ap.add_argument("suite_id")
    ap.add_argument("--checkout", default=str(ROOT / "extern/tprims-rs"))
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--aa", type=int, default=1, help="number of complete set repeats (>=2 gives A/A)")
    ap.add_argument("--sizes", default=None, help="override, comma separated MiB")
    ap.add_argument("--threads", default=None, help="override, comma separated")
    ap.add_argument("--dtypes", default=None)
    ap.add_argument("--engines", default=None)
    ap.add_argument("--label", default=None, help="suffix for the run directory")
    args = ap.parse_args()

    profiles = yaml.safe_load((ROOT / "benchmarks/profiles.yaml").read_text())["profiles"]
    suite = yaml.safe_load((ROOT / "benchmarks/suites" / f"{args.suite_id}.yaml").read_text())
    spec = suite["runs"][0]
    sizes = [float(s) for s in args.sizes.split(",")] if args.sizes else spec["sizes_mib"]
    threads = [int(t) for t in args.threads.split(",")] if args.threads else spec["threads"]
    dtypes = args.dtypes.split(",") if args.dtypes else spec["dtypes"]
    engines = args.engines.split(",") if args.engines else spec["engines"]
    cpu_sets = {str(t): spec["cpu_sets"][spec["threads"].index(t)] for t in threads}

    checkout = pathlib.Path(args.checkout)
    if (checkout / ".git").exists() and checkout.resolve() != (ROOT / "extern/tprims-rs").resolve():
        pass
    pin = build(checkout)
    rev, dirty = pin["TPRIMS_REV"], pin["TPRIMS_DIRTY"] == "true"
    if dirty:
        print("WARNING: the measured checkout is dirty; this cell will be marked dirty", file=sys.stderr)

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{args.label}" if args.label else stamp
    run_dir = ROOT / "data/results" / args.profile / args.suite_id / name
    run_dir.mkdir(parents=True, exist_ok=True)

    bin_dir = pathlib.Path(pin["BIN_DIR"])
    tcbench = bin_dir / "tcbench"
    pinned = checkout / "benchmarks/scripts/pinned.sh"
    idle = checkout / "benchmarks/scripts/idle_cpus.py"
    if not pinned.exists() or not idle.exists():
        sys.exit(f"ERROR: {pinned} or {idle} missing; the protocol scripts belong to the measured revision")

    env = dict(os.environ)
    env.setdefault("CARGO_BUILD_JOBS", str(max(1, (os.cpu_count() or 4) // 4)))
    env["PATH"] = f"{checkout / 'benchmarks/scripts'}:{env['PATH']}"
    if "TBLIS_ROOT" in env:
        env["LD_LIBRARY_PATH"] = f"{env['TBLIS_ROOT']}/lib:{env['TBLIS_ROOT']}/lib64:" + env.get("LD_LIBRARY_PATH", "")

    guards = []
    # 1. correctness first, at every budget, for the whole corpus.
    for size in sizes:
        for t in threads:
            out = run_dir / f"verify-{size:g}m-{t}t.txt"
            guard = run_dir / f"verify-{size:g}m-{t}t.guard"
            r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tcbench), "verify",
                                "--threads", str(t), "--size", str(size),
                                "--dtype", ",".join(dtypes)],
                               env=env, capture_output=True, text=True)
            out.write_text(r.stdout)
            guard.write_text(r.stderr)
            guards.append(str(guard.relative_to(run_dir)))
            if r.returncode != 0 or "MISMATCH" in r.stdout:
                sys.exit(f"ERROR: verify failed for {size} MiB {t}T (see {out}); nothing published")
            if "all comparisons within tolerance" not in r.stdout:
                sys.exit(f"ERROR: verify did not report a clean corpus for {size} MiB {t}T")

    # 2. timing, one CSV per (repeat, size, threads).
    csvs = []
    for rep in range(args.aa):
        for size in sizes:
            for t in threads:
                stem = run_dir / f"run{rep}-{size:g}m-{t}t"
                r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tcbench), "run",
                                    "--threads", str(t), "--size", str(size),
                                    "--dtype", ",".join(dtypes), "--engines", ",".join(engines),
                                    "--reps", str(args.reps), "--csv", str(stem) + ".csv"],
                                   env=env, capture_output=True, text=True)
                (run_dir / f"run{rep}-{size:g}m-{t}t.guard").write_text(r.stderr)
                guards.append(f"run{rep}-{size:g}m-{t}t.guard")
                if r.returncode != 0:
                    sys.exit(f"ERROR: run failed for {size} MiB {t}T (repeat {rep})")
                if not (pathlib.Path(str(stem) + ".csv")).exists():
                    sys.exit(f"ERROR: no CSV produced for {size} MiB {t}T")
                csvs.append(str(stem) + ".csv")

    manifest = {
        "schema_version": 1,
        "target_profile": args.profile,
        "suite_id": args.suite_id,
        "suite_file": f"benchmarks/suites/{args.suite_id}.yaml",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": " ".join(sys.argv),
        "tprims": {
            "url": "https://github.com/tensor4all/tprims-rs",
            "commit": rev,
            "dirty": dirty,
            "features": [f for f in pin["BUILD_FEATURES"].split(",") if f],
            "measured_path": pin["TPRIMS_DIR"],
        },
        "harness": {
            "commit": git(checkout, "rev-parse", "HEAD"),
            "dirty": bool(git(checkout, "status", "--porcelain", "--untracked-files=no")),
        },
        "host": host_info(args.profile, profiles),
        "threads": {
            "counts": threads,
            "cpu_sets": cpu_sets,
            "env": {k: os.environ.get(k) for k in
                    ["OMP_NUM_THREADS", "RAYON_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                     "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"]},
        },
        "timing_policy": {
            "version": 1,
            "minimum_untimed_priming_ms": 500,
            "statistic": "best",
            "repetitions": args.reps,
            "notes": "priming is time-based, not a call count: after an idle gate this host "
                     "reports up to 25% low for the first 1-2 s of sustained work",
        },
        "guard": None,
        "guards": {
            "idle_window_seconds": 3,
            "max_busy_percent": 5,
            "attempts": 3,
            "logs": sorted(set(guards)),
        },
        "providers": [
            {"name": "openblas", "version": None, "commit": None, "path": None,
             "note": "arm present only when the pinned harness was built with the tblis/blas feature"},
            {"name": "tblis", "version": os.environ.get("TBLIS_ROOT"), "commit": None,
             "path": os.environ.get("TBLIS_ROOT"), "note": "2.x ABI; startup self-check in the harness"},
            {"name": "upstream-tensorprimitives", "version": None,
             "commit": "8cda75e11ed26f46c0c22f9629004c84dbabc8e5",
             "path": None, "note": "lkdvos/tensorprimitives-rs, called as a baseline"},
        ],
        "invalidated_by": suite["invalidated_by"],
        "result_files": [str(pathlib.Path(c).relative_to(run_dir)) for c in csvs],
        "run_spec": {"sizes_mib": sizes, "dtypes": dtypes, "engines": engines, "aa": args.aa,
                      "covers_declared_suite": (sizes == spec["sizes_mib"]
                                                and threads == spec["threads"]
                                                and dtypes == spec["dtypes"]
                                                and engines == spec["engines"])},
    }
    del manifest["guard"]

    manifest_path = run_dir / "run.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    v = subprocess.run([sys.executable, str(ROOT / "scripts/validate_run.py"), str(manifest_path)],
                       capture_output=True, text=True)
    print(v.stdout + v.stderr, file=sys.stderr)
    if v.returncode != 0:
        sys.exit("ERROR: run.yaml does not validate; nothing published")

    subprocess.run([sys.executable, str(ROOT / "scripts/report_run.py"), "--run-dir", str(run_dir)], check=True)

    subprocess.run([sys.executable, str(ROOT / "scripts/publish_report.py"), str(run_dir)], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_index.py"), "--write"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
