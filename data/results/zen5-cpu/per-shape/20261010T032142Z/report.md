# `per-shape` on `zen5-cpu`

- tprims-rs commit: `0ec98136c4c894c00013f25b3c99e4a46097e7e9`
- features: `tblis`
- harness commit: `921ecf5e81757a49085b7570a0c9eb703bf0b599`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T03:28:39.253080Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu per-shape --jobs 24 --aa 2`
- raw data: `data/results/zen5-cpu/per-shape/20261010T032142Z/`
## What was measured

- **Corpus `per-shape contraction set`** — Twenty-one cases in four families: `ikb,knb->inb` f64 with i = k = n in {2,4,8,16} and batch in {16,64,256}; `ijk,jkl->il` f64 8x16x8x8; `ij,jk->ik` c64 n = 32 and f64 n = 64; `ij,jk,kl->il` f64 n = 64 in the fixed pairwise order ((ij,jk),kl); and a c64 MPS chain of 32 sites at uniform bond dimension chi in {4,8,16,32,64}, two steps per site and one timed call per whole chain. They range from an overhead-dominated 0.9 us to a 4.8 ms chain, which is the point of the set: the ranking of engines changes across it.
  Source: Reconstructed from the transcribed figure of tprims-rs#61, which Lukas Devos measured on Rusty worker5252 (exclusive node, 2026-09-23, single-threaded, median of three repeat arms). His script is not in any public tree, so the case definitions are the working assumptions recorded in experiments/three-engine-contract/README.md and carried by lukbench's corpus, not a copy of his measurement.
  Known blind spot: One size per case: a ratio here says nothing about a neighbouring size, and the set is not a sweep.
  Known blind spot: An MPS chain is one timed call per whole chain, so a per-step cost is a derived quantity, not a measurement.
  Known blind spot: The corpus is regular by construction: contiguous column-major operands, one batch axis at most, no strided or transposed layouts.
  Known blind spot: The ratio against the reference compares a prepared plan with a one-shot library call. TBLIS 2.0 exposes no prepared-contraction entry point (`tblis.h` has `tblis_tensor_mult` and C++ view wrappers, nothing to hoist), so its own contraction analysis runs inside the timed call, while tprims's `Plan` is constructed outside it by the timing policy. Measured on this host, the reference pays a fixed 3.2-4.5 us per contraction at 1T - the same for a 2x2x2 batch element as for a 16x16x16 one - against 0.02-0.23 us for the prepared path, so on the smallest cases this column reports setup, not kernel efficiency: the ratio's median is 0.016 for cases under 1 us and 0.75 above 1 ms, where compute finally dominates.
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

Every row below passed `lukbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over 2 complete set repeats of the best wall time per engine.

Where the independent reference ran, the last column is `tprims [plan] / tblis`, a ratio of those two geomeans: above 1 means tprims took longer. The `±` after it is the largest scatter among the repetitions behind it (the harness's `spread`, `(max - min) / best`), so a row whose ratio is smaller than its own scatter is not separable from noise. The same number is in the CSV's `spread` column for every row.

## fixed shapes, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0289 | 0.361 ±8.5% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0298 | 0.0579 | 0.360 ±8.5% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0029 | 0.0095 | 0.058 ±8.5% |
| `ikb_knb_inb_n16_b16` | 0.0038 | 0.0093 | 0.0721 | 0.052 ±8.5% |
| `ikb_knb_inb_n16_b256` | 0.0600 | 0.1420 | 1.1126 | 0.054 ±8.5% |
| `ikb_knb_inb_n16_b64` | 0.0144 | 0.0356 | 0.2804 | 0.051 ±8.5% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0528 | 0.009 ±8.5% |
| `ikb_knb_inb_n2_b256` | 0.0048 | 0.0230 | 0.8048 | 0.006 ±8.5% |
| `ikb_knb_inb_n2_b64` | 0.0013 | 0.0062 | 0.2031 | 0.007 ±8.5% |
| `ikb_knb_inb_n4_b16` | 0.0007 | 0.0025 | 0.0539 | 0.012 ±8.5% |
| `ikb_knb_inb_n4_b256` | 0.0077 | 0.0335 | 0.8248 | 0.009 ±8.5% |
| `ikb_knb_inb_n4_b64` | 0.0020 | 0.0086 | 0.2101 | 0.010 ±8.5% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0040 | 0.0584 | 0.016 ±8.5% |
| `ikb_knb_inb_n8_b256` | 0.0116 | 0.0569 | 0.8855 | 0.013 ±8.5% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0140 | 0.2225 | 0.014 ±8.5% |
| **geomean** | 0.0037 | 0.0127 | 0.1472 | 0.025 ±8.5% |

## fixed shapes, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0197 | 0.531 ±22.6% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0299 | 0.0382 | 0.546 ±22.6% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0029 | 0.0121 | 0.046 ±22.6% |
| `ikb_knb_inb_n16_b16` | 0.0038 | 0.0093 | 0.1270 | 0.030 ±22.6% |
| `ikb_knb_inb_n16_b256` | 0.0182 | 0.0396 | 0.7214 | 0.025 ±22.6% |
| `ikb_knb_inb_n16_b64` | 0.0144 | 0.0356 | 0.5455 | 0.026 ±22.6% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0184 | 0.026 ±22.6% |
| `ikb_knb_inb_n2_b256` | 0.0050 | 0.0234 | 0.2272 | 0.022 ±22.6% |
| `ikb_knb_inb_n2_b64` | 0.0014 | 0.0062 | 0.0608 | 0.023 ±22.6% |
| `ikb_knb_inb_n4_b16` | 0.0007 | 0.0025 | 0.0417 | 0.016 ±22.6% |
| `ikb_knb_inb_n4_b256` | 0.0076 | 0.0320 | 0.2346 | 0.032 ±22.6% |
| `ikb_knb_inb_n4_b64` | 0.0021 | 0.0085 | 0.0617 | 0.033 ±22.6% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0039 | 0.1018 | 0.009 ±22.6% |
| `ikb_knb_inb_n8_b256` | 0.0117 | 0.0560 | 0.2478 | 0.047 ±22.6% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0145 | 0.1639 | 0.019 ±22.6% |
| **geomean** | 0.0035 | 0.0117 | 0.0920 | 0.038 ±22.6% |

## fixed shapes, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0079 | 0.0147 | 0.372 ±3.6% |
| `mps_chain_L32_chi16` | 0.1038 | 0.1816 | 0.5361 | 0.194 ±3.6% |
| `mps_chain_L32_chi32` | 0.7013 | 0.9510 | 1.5197 | 0.461 ±3.6% |
| `mps_chain_L32_chi4` | 0.0228 | 0.0454 | 0.3095 | 0.074 ±3.6% |
| `mps_chain_L32_chi64` | 6.8075 | 6.7888 | 8.7954 | 0.774 ±3.6% |
| `mps_chain_L32_chi8` | 0.0403 | 0.0718 | 0.3538 | 0.114 ±3.6% |
| **geomean** | 0.1164 | 0.1765 | 0.4751 | 0.245 ±3.6% |

## fixed shapes, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0081 | 0.0134 | 0.407 ±28.1% |
| `mps_chain_L32_chi16` | 0.1043 | 0.1833 | 0.7996 | 0.131 ±28.1% |
| `mps_chain_L32_chi32` | 0.6996 | 0.9501 | 1.1092 | 0.631 ±28.1% |
| `mps_chain_L32_chi4` | 0.0222 | 0.0457 | 0.5902 | 0.038 ±28.1% |
| `mps_chain_L32_chi64` | 2.5732 | 2.5882 | 3.6501 | 0.705 ±28.1% |
| `mps_chain_L32_chi8` | 0.0394 | 0.0728 | 0.7225 | 0.055 ±28.1% |
| **geomean** | 0.0983 | 0.1516 | 0.5145 | 0.191 ±28.1% |
