# `per-shape` on `zen5-cpu`

- tprims-rs commit: `0ec98136c4c894c00013f25b3c99e4a46097e7e9`
- features: `tblis`
- harness commit: `3b0a8420d01453fbe5c72935e91e10ce80989deb`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T01:01:08.690179Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu per-shape --jobs 24`
- raw data: `data/results/zen5-cpu/per-shape/20261010T005733Z/`
## What was measured

- **Corpus `per-shape contraction set`** — Twenty-one cases in four families: `ikb,knb->inb` f64 with i = k = n in {2,4,8,16} and batch in {16,64,256}; `ijk,jkl->il` f64 8x16x8x8; `ij,jk->ik` c64 n = 32 and f64 n = 64; `ij,jk,kl->il` f64 n = 64 in the fixed pairwise order ((ij,jk),kl); and a c64 MPS chain of 32 sites at uniform bond dimension chi in {4,8,16,32,64}, two steps per site and one timed call per whole chain. They range from an overhead-dominated 0.9 us to a 4.8 ms chain, which is the point of the set: the ranking of engines changes across it.
  Source: Reconstructed from the transcribed figure of tprims-rs#61, which Lukas Devos measured on Rusty worker5252 (exclusive node, 2026-09-23, single-threaded, median of three repeat arms). His script is not in any public tree, so the case definitions are the working assumptions recorded in experiments/three-engine-contract/README.md and carried by lukbench's corpus, not a copy of his measurement.
  Known blind spot: One size per case: a ratio here says nothing about a neighbouring size, and the set is not a sweep.
  Known blind spot: An MPS chain is one timed call per whole chain, so a per-step cost is a derived quantity, not a measurement.
  Known blind spot: The corpus is regular by construction: contiguous column-major operands, one batch axis at most, no strided or transposed layouts.
- **Engines** — one row per engine in every table below:
  - `tprims [plan]` — This library with its planner choosing the route per case: the packed driver, or the copy-free faer path, or the elementwise pass for an all-batch case.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `tprims [packed]` — This library with the packed driver forced. A diagnostic arm: it shows what the planner's other routes buy or cost on the same inputs.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `tblis` — Actual C++ TBLIS through the direct FFI adapter, as the independent third-party reference implementation. Pinned by release tag, not by a local revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout builds it from the tag and writes the PROVENANCE this repository records.
    Identity (as measured): tblis, version 2.0, commit `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` — TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/opt/tblis-v2.0-beta2-zen3 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 407b4f6fef7f4ede
    Caveat: Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, so the prefix cannot be made inside a bare checkout. The page repeats the tag, commit, bundled BLIS revision and artifact hash the manifest recorded.
- **Shapes** — the corpus has fixed shapes, so there is no nominal-size knob and the runner is given no `--size`; each table below is one dtype and thread count over the whole corpus.
- **dtypes** — `f64` is a real double, `c64` a complex double. The complex rows
  are the harder case for this library and are never likelier to look good.
- **Numbers** — milliseconds, best wall time per case and engine. See the timing
  policy for what is inside and outside the timed region.

## Hardware

- CPU: `AMD Ryzen AI 9 HX 470`
- logical CPUs: `24`
- L3: `24 MiB (2 instances)`
- L3 domains: `0-3: 16 MiB shared; 4-11: 8 MiB shared`
- OS / arch: `Linux 7.0.0-38-generic` / `x86_64`
- hostname: `shinaoka-EVO-X1Pro`
- CPU sets: 1T -> `4`, 4T -> `4-7`

Every row below passed `lukbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over the timed repetitions (this run made a single complete set, so it carries no A/A) of the best wall time per engine.

Where the independent reference ran, the last column is `tprims [plan] / tblis`, a ratio of those two geomeans: above 1 means tprims took longer. The `±` after it is the largest scatter among the repetitions behind it (the harness's `spread`, `(max - min) / best`), so a row whose ratio is smaller than its own scatter is not separable from noise. The same number is in the CSV's `spread` column for every row.

## fixed shapes, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0290 | 0.358 ±6.0% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0297 | 0.0580 | 0.360 ±6.0% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0031 | 0.0095 | 0.058 ±6.0% |
| `ikb_knb_inb_n16_b16` | 0.0037 | 0.0093 | 0.0725 | 0.052 ±6.0% |
| `ikb_knb_inb_n16_b256` | 0.0591 | 0.1458 | 1.1083 | 0.053 ±6.0% |
| `ikb_knb_inb_n16_b64` | 0.0144 | 0.0371 | 0.2849 | 0.050 ±6.0% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0532 | 0.009 ±6.0% |
| `ikb_knb_inb_n2_b256` | 0.0050 | 0.0224 | 0.8125 | 0.006 ±6.0% |
| `ikb_knb_inb_n2_b64` | 0.0013 | 0.0063 | 0.2048 | 0.007 ±6.0% |
| `ikb_knb_inb_n4_b16` | 0.0007 | 0.0026 | 0.0542 | 0.012 ±6.0% |
| `ikb_knb_inb_n4_b256` | 0.0077 | 0.0322 | 0.8307 | 0.009 ±6.0% |
| `ikb_knb_inb_n4_b64` | 0.0021 | 0.0091 | 0.2115 | 0.010 ±6.0% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0041 | 0.0580 | 0.016 ±6.0% |
| `ikb_knb_inb_n8_b256` | 0.0115 | 0.0611 | 0.8948 | 0.013 ±6.0% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0149 | 0.2271 | 0.014 ±6.0% |
| **geomean** | 0.0038 | 0.0130 | 0.1481 | 0.025 ±6.0% |

## fixed shapes, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0148 | 0.0208 | 0.501 ±54.8% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0297 | 0.0397 | 0.524 ±54.8% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0031 | 0.0119 | 0.047 ±54.8% |
| `ikb_knb_inb_n16_b16` | 0.0037 | 0.0094 | 0.1305 | 0.029 ±54.8% |
| `ikb_knb_inb_n16_b256` | 0.0182 | 0.0395 | 0.7188 | 0.025 ±54.8% |
| `ikb_knb_inb_n16_b64` | 0.0141 | 0.0351 | 0.5409 | 0.026 ±54.8% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0180 | 0.026 ±54.8% |
| `ikb_knb_inb_n2_b256` | 0.0048 | 0.0228 | 0.2388 | 0.020 ±54.8% |
| `ikb_knb_inb_n2_b64` | 0.0013 | 0.0066 | 0.0606 | 0.022 ±54.8% |
| `ikb_knb_inb_n4_b16` | 0.0006 | 0.0025 | 0.0413 | 0.016 ±54.8% |
| `ikb_knb_inb_n4_b256` | 0.0073 | 0.0326 | 0.2363 | 0.031 ±54.8% |
| `ikb_knb_inb_n4_b64` | 0.0020 | 0.0087 | 0.0623 | 0.032 ±54.8% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0040 | 0.1016 | 0.009 ±54.8% |
| `ikb_knb_inb_n8_b256` | 0.0112 | 0.0544 | 0.2479 | 0.045 ±54.8% |
| `ikb_knb_inb_n8_b64` | 0.0030 | 0.0140 | 0.1582 | 0.019 ±54.8% |
| **geomean** | 0.0034 | 0.0117 | 0.0926 | 0.037 ±54.8% |

## fixed shapes, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0081 | 0.0147 | 0.371 ±12.1% |
| `mps_chain_L32_chi16` | 0.1041 | 0.1819 | 0.5370 | 0.194 ±12.1% |
| `mps_chain_L32_chi32` | 0.6985 | 0.9535 | 1.5316 | 0.456 ±12.1% |
| `mps_chain_L32_chi4` | 0.0227 | 0.0455 | 0.3080 | 0.074 ±12.1% |
| `mps_chain_L32_chi64` | 6.7555 | 6.7231 | 8.8413 | 0.764 ±12.1% |
| `mps_chain_L32_chi8` | 0.0404 | 0.0718 | 0.3522 | 0.115 ±12.1% |
| **geomean** | 0.1161 | 0.1770 | 0.4757 | 0.244 ±12.1% |

## fixed shapes, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0080 | 0.0148 | 0.369 ±14.9% |
| `mps_chain_L32_chi16` | 0.1039 | 0.1809 | 0.7739 | 0.134 ±14.9% |
| `mps_chain_L32_chi32` | 0.6980 | 0.9482 | 1.0887 | 0.641 ±14.9% |
| `mps_chain_L32_chi4` | 0.0224 | 0.0451 | 0.5783 | 0.039 ±14.9% |
| `mps_chain_L32_chi64` | 2.5866 | 2.6071 | 3.6857 | 0.702 ±14.9% |
| `mps_chain_L32_chi8` | 0.0392 | 0.0708 | 0.7575 | 0.052 ±14.9% |
| **geomean** | 0.0983 | 0.1501 | 0.5219 | 0.188 ±14.9% |
