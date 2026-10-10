# `per-shape` on `zen5-cpu`

- tprims-rs commit: `63d7aac1dce53271304fafa3f039726363ac3d05`
- features: `tblis`
- harness commit: `921ecf5e81757a49085b7570a0c9eb703bf0b599`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T03:56:45.097213Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu per-shape --jobs 24 --aa 2`
- raw data: `data/results/zen5-cpu/per-shape/20261010T034948Z/`
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

`prepare (µs)` is what each side spends *before* the timed call - the plan for tprims, the operand descriptors for the reference. The timing policy excludes that work, which is why the harness can build a plan once and time only execution, and the reference has nothing comparable to hoist: its own analysis is inside the one call it exposes. On microsecond cases the preparation can exceed the whole timed call, so a ratio there compares a prepared path with a one-shot call rather than two kernels.

## fixed shapes, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0291 | 1.7/0.5 | 0.358 ±6.4% |
| `ij_jk_kl_il_n64` | 0.0209 | 0.0298 | 0.0582 | 3.0/1.1 | 0.359 ±6.4% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0030 | 0.0096 | 1.5/0.4 | 0.058 ±6.4% |
| `ikb_knb_inb_n16_b16` | 0.0038 | 0.0095 | 0.0720 | 1.3/0.5 | 0.052 ±6.4% |
| `ikb_knb_inb_n16_b256` | 0.0605 | 0.1407 | 1.1197 | 1.6/0.4 | 0.054 ±6.4% |
| `ikb_knb_inb_n16_b64` | 0.0144 | 0.0359 | 0.2827 | 1.5/0.4 | 0.051 ±6.4% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0525 | 2.3/0.5 | 0.009 ±6.4% |
| `ikb_knb_inb_n2_b256` | 0.0050 | 0.0223 | 0.8142 | 1.5/0.4 | 0.006 ±6.4% |
| `ikb_knb_inb_n2_b64` | 0.0014 | 0.0061 | 0.2034 | 1.3/0.5 | 0.007 ±6.4% |
| `ikb_knb_inb_n4_b16` | 0.0007 | 0.0024 | 0.0538 | 1.3/0.5 | 0.012 ±6.4% |
| `ikb_knb_inb_n4_b256` | 0.0076 | 0.0318 | 0.8304 | 1.6/0.4 | 0.009 ±6.4% |
| `ikb_knb_inb_n4_b64` | 0.0020 | 0.0083 | 0.2095 | 1.3/0.5 | 0.010 ±6.4% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0039 | 0.0573 | 1.3/0.5 | 0.016 ±6.4% |
| `ikb_knb_inb_n8_b256` | 0.0116 | 0.0539 | 0.8899 | 1.6/0.5 | 0.013 ±6.4% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0141 | 0.2251 | 1.4/0.5 | 0.014 ±6.4% |
| **geomean** | 0.0038 | 0.0126 | 0.1476 | 1.6/0.5 | 0.026 ±6.4% |

## fixed shapes, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0190 | 1.9/0.5 | 0.551 ±51.7% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0298 | 0.0390 | 2.9/1.0 | 0.534 ±51.7% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0029 | 0.0127 | 1.5/0.6 | 0.044 ±51.7% |
| `ikb_knb_inb_n16_b16` | 0.0037 | 0.0092 | 0.1387 | 1.5/0.6 | 0.027 ±51.7% |
| `ikb_knb_inb_n16_b256` | 0.0176 | 0.0397 | 0.7270 | 1.9/0.6 | 0.024 ±51.7% |
| `ikb_knb_inb_n16_b64` | 0.0145 | 0.0349 | 0.5384 | 1.8/0.4 | 0.027 ±51.7% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0183 | 2.3/0.5 | 0.026 ±51.7% |
| `ikb_knb_inb_n2_b256` | 0.0050 | 0.0222 | 0.2311 | 2.3/0.4 | 0.022 ±51.7% |
| `ikb_knb_inb_n2_b64` | 0.0014 | 0.0060 | 0.0614 | 1.7/0.5 | 0.023 ±51.7% |
| `ikb_knb_inb_n4_b16` | 0.0006 | 0.0025 | 0.0415 | 1.6/0.6 | 0.016 ±51.7% |
| `ikb_knb_inb_n4_b256` | 0.0075 | 0.0317 | 0.2374 | 1.9/0.4 | 0.032 ±51.7% |
| `ikb_knb_inb_n4_b64` | 0.0020 | 0.0084 | 0.0625 | 1.6/0.5 | 0.032 ±51.7% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0038 | 0.0998 | 1.5/0.5 | 0.009 ±51.7% |
| `ikb_knb_inb_n8_b256` | 0.0115 | 0.0542 | 0.2479 | 1.7/0.4 | 0.047 ±51.7% |
| `ikb_knb_inb_n8_b64` | 0.0031 | 0.0140 | 0.1609 | 1.9/0.4 | 0.020 ±51.7% |
| **geomean** | 0.0035 | 0.0115 | 0.0928 | 1.8/0.5 | 0.037 ±51.7% |

## fixed shapes, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0054 | 0.0080 | 0.0147 | 1.6/0.5 | 0.370 ±7.5% |
| `mps_chain_L32_chi16` | 0.1044 | 0.1846 | 0.5384 | 58.4/24.2 | 0.194 ±7.5% |
| `mps_chain_L32_chi32` | 0.7023 | 0.9568 | 1.5253 | 61.2/24.2 | 0.460 ±7.5% |
| `mps_chain_L32_chi4` | 0.0228 | 0.0464 | 0.3119 | 58.5/22.9 | 0.073 ±7.5% |
| `mps_chain_L32_chi64` | 6.8099 | 6.8181 | 8.8711 | 419.8/26.3 | 0.768 ±7.5% |
| `mps_chain_L32_chi8` | 0.0402 | 0.0748 | 0.3567 | 60.2/24.3 | 0.113 ±7.5% |
| **geomean** | 0.1164 | 0.1796 | 0.4780 | 44.9/12.7 | 0.244 ±7.5% |

## fixed shapes, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0080 | 0.0137 | 2.0/0.7 | 0.399 ±20.1% |
| `mps_chain_L32_chi16` | 0.1041 | 0.1838 | 0.7846 | 61.6/24.2 | 0.133 ±20.1% |
| `mps_chain_L32_chi32` | 0.6985 | 0.9559 | 1.1619 | 60.8/24.2 | 0.601 ±20.1% |
| `mps_chain_L32_chi4` | 0.0221 | 0.0466 | 0.5630 | 57.9/22.8 | 0.039 ±20.1% |
| `mps_chain_L32_chi64` | 2.6156 | 2.5704 | 3.6565 | 420.0/27.9 | 0.715 ±20.1% |
| `mps_chain_L32_chi8` | 0.0395 | 0.0778 | 0.6927 | 61.4/24.4 | 0.057 ±20.1% |
| **geomean** | 0.0984 | 0.1536 | 0.5111 | 47.4/13.7 | 0.192 ±20.1% |
