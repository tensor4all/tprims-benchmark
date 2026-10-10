# `per-shape` on `zen5-cpu`

- tprims-rs commit: `0df08df4651413c629903b378eae2c3685716bbd`
- features: `tblis`
- harness commit: `64b4455d2b924531a960d77f245ed0902de1af6d`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T15:24:54.513331Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu per-shape`
- raw data: `data/results/zen5-cpu/per-shape/20261010T152119Z/`
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

Every row below passed `lukbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over the timed repetitions (this run made a single complete set, so it carries no A/A) of the best wall time per engine.

Where the independent reference ran, the last column is `tprims [plan] / tblis`, a ratio of those two geomeans: above 1 means tprims took longer. The `±` after it is the largest scatter among the repetitions behind it (the harness's `spread`, `(max - min) / best`), so a row whose ratio is smaller than its own scatter is not separable from noise. The same number is in the CSV's `spread` column for every row.

`prepare (µs)` is what each side spends *before* the timed call - the plan for tprims, the operand descriptors for the reference. The timing policy excludes that work, which is why the harness can build a plan once and time only execution, and the reference has nothing comparable to hoist: its own analysis is inside the one call it exposes. On microsecond cases the preparation can exceed the whole timed call, so a ratio there compares a prepared path with a one-shot call rather than two kernels.

## fixed shapes, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0149 | 0.0289 | 1.6/0.6 | 0.360 ±169.6% |
| `ij_jk_kl_il_n64` | 0.0208 | 0.0297 | 0.0578 | 2.9/1.3 | 0.360 ±169.6% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0030 | 0.0096 | 1.7/0.4 | 0.058 ±169.6% |
| `ikb_knb_inb_n16_b16` | 0.0037 | 0.0093 | 0.0725 | 1.4/0.5 | 0.051 ±169.6% |
| `ikb_knb_inb_n16_b256` | 0.0604 | 0.1409 | 1.1201 | 1.6/0.5 | 0.054 ±169.6% |
| `ikb_knb_inb_n16_b64` | 0.0144 | 0.0348 | 0.2821 | 1.4/0.4 | 0.051 ±169.6% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0525 | 2.2/0.5 | 0.009 ±169.6% |
| `ikb_knb_inb_n2_b256` | 0.0048 | 0.0230 | 0.8021 | 1.5/0.5 | 0.006 ±169.6% |
| `ikb_knb_inb_n2_b64` | 0.0014 | 0.0061 | 0.2069 | 1.4/0.6 | 0.007 ±169.6% |
| `ikb_knb_inb_n4_b16` | 0.0006 | 0.0025 | 0.0535 | 1.4/0.5 | 0.012 ±169.6% |
| `ikb_knb_inb_n4_b256` | 0.0076 | 0.0321 | 0.8320 | 1.6/0.4 | 0.009 ±169.6% |
| `ikb_knb_inb_n4_b64` | 0.0020 | 0.0085 | 0.2077 | 1.6/0.4 | 0.010 ±169.6% |
| `ikb_knb_inb_n8_b16` | 0.0009 | 0.0039 | 0.0579 | 1.4/0.5 | 0.016 ±169.6% |
| `ikb_knb_inb_n8_b256` | 0.0120 | 0.0548 | 0.8899 | 1.8/0.4 | 0.013 ±169.6% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0142 | 0.2242 | 1.4/0.5 | 0.014 ±169.6% |
| **geomean** | 0.0038 | 0.0126 | 0.1476 | 1.6/0.5 | 0.026 ±169.6% |

## fixed shapes, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64` | 0.0104 | 0.0148 | 0.0194 | 2.0/0.7 | 0.538 ±21.9% |
| `ij_jk_kl_il_n64` | 0.0211 | 0.0297 | 0.0392 | 2.8/1.1 | 0.538 ±21.9% |
| `ijk_jkl_il_8x16x8` | 0.0006 | 0.0030 | 0.0131 | 1.8/0.6 | 0.044 ±21.9% |
| `ikb_knb_inb_n16_b16` | 0.0037 | 0.0098 | 0.1400 | 1.6/0.6 | 0.027 ±21.9% |
| `ikb_knb_inb_n16_b256` | 0.0180 | 0.0400 | 0.7208 | 1.5/0.6 | 0.025 ±21.9% |
| `ikb_knb_inb_n16_b64` | 0.0142 | 0.0362 | 0.5600 | 1.7/0.5 | 0.025 ±21.9% |
| `ikb_knb_inb_n2_b16` | 0.0005 | 0.0019 | 0.0178 | 2.7/0.6 | 0.027 ±21.9% |
| `ikb_knb_inb_n2_b256` | 0.0048 | 0.0228 | 0.2312 | 2.0/0.5 | 0.021 ±21.9% |
| `ikb_knb_inb_n2_b64` | 0.0014 | 0.0061 | 0.0620 | 1.5/0.6 | 0.022 ±21.9% |
| `ikb_knb_inb_n4_b16` | 0.0007 | 0.0025 | 0.0419 | 1.7/0.6 | 0.017 ±21.9% |
| `ikb_knb_inb_n4_b256` | 0.0082 | 0.0318 | 0.2345 | 1.9/0.5 | 0.035 ±21.9% |
| `ikb_knb_inb_n4_b64` | 0.0022 | 0.0083 | 0.0618 | 2.0/0.6 | 0.035 ±21.9% |
| `ikb_knb_inb_n8_b16` | 0.0010 | 0.0040 | 0.0997 | 1.7/0.6 | 0.010 ±21.9% |
| `ikb_knb_inb_n8_b256` | 0.0122 | 0.0553 | 0.2462 | 1.7/0.5 | 0.050 ±21.9% |
| `ikb_knb_inb_n8_b64` | 0.0032 | 0.0143 | 0.1625 | 2.1/0.5 | 0.020 ±21.9% |
| **geomean** | 0.0035 | 0.0117 | 0.0932 | 1.9/0.6 | 0.038 ±21.9% |

## fixed shapes, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0054 | 0.0080 | 0.0146 | 1.7/0.5 | 0.373 ±2.8% |
| `mps_chain_L32_chi16` | 0.1036 | 0.1857 | 0.5360 | 59.1/24.1 | 0.193 ±2.8% |
| `mps_chain_L32_chi32` | 0.7018 | 0.9519 | 1.5171 | 61.8/23.8 | 0.463 ±2.8% |
| `mps_chain_L32_chi4` | 0.0228 | 0.0494 | 0.3101 | 58.6/22.8 | 0.074 ±2.8% |
| `mps_chain_L32_chi64` | 6.8498 | 6.8381 | 8.9977 | 417.6/29.2 | 0.761 ±2.8% |
| `mps_chain_L32_chi8` | 0.0410 | 0.0770 | 0.3537 | 58.4/23.7 | 0.116 ±2.8% |
| **geomean** | 0.1168 | 0.1822 | 0.4766 | 45.3/12.7 | 0.245 ±2.8% |

## fixed shapes, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32` | 0.0055 | 0.0081 | 0.0134 | 2.4/0.6 | 0.412 ±28.0% |
| `mps_chain_L32_chi16` | 0.1067 | 0.1858 | 0.7665 | 60.0/24.2 | 0.139 ±28.0% |
| `mps_chain_L32_chi32` | 0.7038 | 0.9584 | 1.1473 | 60.9/23.9 | 0.613 ±28.0% |
| `mps_chain_L32_chi4` | 0.0228 | 0.0509 | 0.5458 | 60.5/23.1 | 0.042 ±28.0% |
| `mps_chain_L32_chi64` | 2.5738 | 2.4939 | 3.6030 | 422.4/27.0 | 0.714 ±28.0% |
| `mps_chain_L32_chi8` | 0.0405 | 0.0770 | 0.7308 | 60.2/23.8 | 0.055 ±28.0% |
| **geomean** | 0.0997 | 0.1553 | 0.5066 | 48.9/13.2 | 0.197 ±28.0% |
