<!-- generated from data/results/zen5-cpu/tcbench/20261010T035657Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tcbench` on `zen5-cpu`

- tprims-rs commit: `63d7aac1dce53271304fafa3f039726363ac3d05`
- features: `tblis`
- harness commit: `921ecf5e81757a49085b7570a0c9eb703bf0b599`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T04:20:08.444419Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu tcbench --jobs 24`
- raw data: `data/results/zen5-cpu/tcbench/20261010T035657Z/`
## What was measured

- **Corpus `TCCG`** — One contraction per case, from coupled-cluster (CCSD, CCSD(T)), AO-to-MO integral transformation and tensor-times-matrix workloads. Each case is a full tensor contraction, not a matrix multiply.
  Source: Springer & Bientinesi, "Design of a High-Performance GEMM-like Tensor-Tensor Multiplication" (arXiv:1607.00145), and the accompanying HPAC/tccg benchmark.py. Shapes are rescaled from one nominal tensor size by TCCG's sizing rule, so the extents are a function of that knob rather than physical dimensions.
  Known blind spot: Every case has unit batch extent, so a cost proportional to batch elements is invisible here.
  Known blind spot: Stride-1 extents are rounded up to a multiple of 24, so the corpus is regular by construction.
- **Engines** — one row per engine in every table below:
  - `tprims [plan]` — This library, with its planner choosing the route per case: the packed driver, or the copy-free faer path, or the elementwise path for an all-batch case.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `tprims [packed]` — This library with the packed driver forced instead of chosen. A diagnostic arm: it shows what the planner's non-packed routes buy or cost on the same inputs.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `tblis` — Actual C++ TBLIS through the direct FFI adapter, as the independent third-party reference implementation. Pinned by release tag, not by a local revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout builds it from the tag and writes the PROVENANCE this repository records.
    Identity (as measured): tblis, version 2.0, commit `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` — TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/opt/tblis-v2.0-beta2-zen3 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 407b4f6fef7f4ede
    Caveat: Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, so the prefix cannot be made inside a bare checkout. The page repeats the tag, commit, bundled BLIS revision and artifact hash the manifest recorded.
- **Sizes** — the nominal tensor size per case in MiB. TCCG's sizing rule scales
  every extent of a case from it, so the same case at 1 MiB and 16 MiB has the
  same shape structure at different magnitudes.
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

Every row below passed `tcbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over the timed repetitions (this run made a single complete set, so it carries no A/A) of the best wall time per engine.

Where the independent reference ran, the last column is `tprims [plan] / tblis`, a ratio of those two geomeans: above 1 means tprims took longer. The `±` after it is the largest scatter among the repetitions behind it (the harness's `spread`, `(max - min) / best`), so a row whose ratio is smaller than its own scatter is not separable from noise. The same number is in the CSV's `spread` column for every row.

`prepare (µs)` is what each side spends *before* the timed call - the plan for tprims, the operand descriptors for the reference. The timing policy excludes that work, which is why the harness can build a plan once and time only execution, and the reference has nothing comparable to hoist: its own analysis is inside the one call it exposes. On microsecond cases the preparation can exceed the whole timed call, so a ratio there compares a prepared path with a one-shot call rather than two kernels.

## 16 MiB, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `abc-bk-akc` | 14.8912 | 14.9105 | 18.9157 | 109.0/0.2 | 0.787 ±14.6% |
| `abcijk-eiab-jkec` | 14.8439 | 14.8269 | 24.6559 | 44.1/0.2 | 0.602 ±14.6% |
| `abcijk-eiac-jkeb` | 13.8887 | 13.9613 | 35.0772 | 47.3/0.2 | 0.396 ±14.6% |
| `abcijk-eibc-jkea` | 13.6206 | 13.6358 | 17.0154 | 61.4/0.1 | 0.800 ±14.6% |
| `abcijk-ejab-ikec` | 14.8333 | 14.7899 | 21.6014 | 44.8/0.2 | 0.687 ±14.6% |
| `abcijk-ejac-ikeb` | 14.0644 | 14.0738 | 19.2670 | 49.8/0.2 | 0.730 ±14.6% |
| `abcijk-ejbc-ikea` | 13.8061 | 13.8204 | 17.0885 | 61.1/0.2 | 0.808 ±14.6% |
| `abcijk-ekab-ijec` | 14.7782 | 14.7532 | 18.1816 | 47.3/0.1 | 0.813 ±14.6% |
| `abcijk-ekac-ijeb` | 13.9530 | 13.9456 | 23.3617 | 47.2/0.1 | 0.597 ±14.6% |
| `abcijk-ekbc-ijea` | 13.7516 | 13.7447 | 16.9621 | 62.0/0.2 | 0.811 ±14.6% |
| `abcijk-ijma-mkbc` | 13.6980 | 13.6890 | 16.9305 | 62.7/0.2 | 0.809 ±14.6% |
| `abcijk-ijmb-mkac` | 13.9367 | 13.8758 | 23.4094 | 47.0/0.2 | 0.595 ±14.6% |
| `abcijk-ijmc-mkab` | 14.7759 | 14.7577 | 18.1388 | 44.4/0.2 | 0.815 ±14.6% |
| `abcijk-ikma-mjbc` | 13.7508 | 13.7324 | 17.0912 | 63.7/0.2 | 0.805 ±14.6% |
| `abcijk-ikmb-mjac` | 13.9818 | 14.0154 | 19.0462 | 47.5/0.1 | 0.734 ±14.6% |
| `abcijk-ikmc-mjab` | 14.7666 | 14.7590 | 21.8598 | 44.8/0.2 | 0.676 ±14.6% |
| `abcijk-jkma-mibc` | 13.6362 | 13.6354 | 16.9919 | 63.3/0.2 | 0.803 ±14.6% |
| `abcijk-jkmb-miac` | 13.9997 | 13.9564 | 34.6268 | 48.0/0.1 | 0.404 ±14.6% |
| `abcijk-jkmc-miab` | 14.7612 | 14.7911 | 25.0813 | 43.6/0.1 | 0.589 ±14.6% |
| `abcs-rc-abrs` | 9.5429 | 9.5336 | 15.6805 | 410.1/0.3 | 0.609 ±14.6% |
| `abj-bka-kj` | 19.7568 | 19.5713 | 29.2723 | 133.3/0.3 | 0.675 ±14.6% |
| `abjc-cbka-kj` | 37.9543 | 37.8838 | 25.9373 | 722.4/0.2 | 1.463 ±14.6% |
| `abjc-kbac-jk` | 12.4993 | 12.4269 | 20.2960 | 598.7/0.2 | 0.616 ±14.6% |
| `abjcd-dkbac-jk` | 17.3350 | 17.3798 | 21.2481 | 1573.3/0.3 | 0.816 ±14.6% |
| `abrs-qb-aqrs` | 8.6332 | 8.6237 | 15.9775 | 539.1/0.2 | 0.540 ±14.6% |
| `adbjc-cbdka-kj` | 46.8958 | 46.7230 | 40.9174 | 1554.8/0.3 | 1.146 ±14.6% |
| `ajb-kba-jk` | 18.1356 | 18.1295 | 20.5142 | 109.2/0.2 | 0.884 ±14.6% |
| `ajbc-ckba-jk` | 20.9146 | 20.9671 | 18.2351 | 704.0/0.2 | 1.147 ±14.6% |
| `ajbdc-ckbad-jk` | 17.0100 | 17.0376 | 20.4618 | 1538.3/0.2 | 0.831 ±14.6% |
| `aqrs-pa-pqrs` | 7.7532 | 9.5589 | 15.6859 | 0.5/0.3 | 0.494 ±14.6% |
| `ij-ik-kj` | 124.0321 | 129.8921 | 133.3772 | 0.7/0.3 | 0.930 ±14.6% |
| `ij-ikl-ljk` | 17.5958 | 17.6300 | 25.0337 | 50.8/0.2 | 0.703 ±14.6% |
| `ij-kil-lkj` | 21.5233 | 21.5284 | 31.7542 | 50.5/0.3 | 0.678 ±14.6% |
| `ijk-ikl-lj` | 15.5788 | 15.5690 | 20.2373 | 109.6/0.2 | 0.770 ±14.6% |
| `ijk-il-jlk` | 15.9147 | 15.8579 | 18.6874 | 116.8/0.3 | 0.852 ±14.6% |
| `ijk-ilk-jl` | 14.7970 | 14.8137 | 19.2024 | 111.7/0.3 | 0.771 ±14.6% |
| `ijk-ilk-lj` | 14.9222 | 14.9176 | 20.3795 | 111.2/0.3 | 0.732 ±14.6% |
| `ijk-ilmk-mjl` | 7.4606 | 7.4569 | 13.6570 | 26.4/0.2 | 0.546 ±14.6% |
| `ijkl-imjn-lnkm` | 254.8039 | 254.4938 | 252.8654 | 42.5/0.2 | 1.008 ±14.6% |
| `ijkl-imjn-nlmk` | 255.4792 | 255.4920 | 254.8970 | 39.6/0.2 | 1.002 ±14.6% |
| `ijkl-imkn-jnlm` | 254.0920 | 254.1733 | 253.1856 | 43.0/0.2 | 1.004 ±14.6% |
| `ijkl-imkn-njml` | 251.3353 | 251.0396 | 258.4204 | 38.4/0.1 | 0.973 ±14.6% |
| `ijkl-imln-jnkm` | 250.0448 | 250.0785 | 258.3999 | 41.1/0.2 | 0.968 ±14.6% |
| `ijkl-imln-njmk` | 249.4578 | 249.6132 | 256.2569 | 38.8/0.2 | 0.973 ±14.6% |
| `ijkl-imnj-nlkm` | 254.0821 | 253.8493 | 253.1655 | 39.8/0.2 | 1.004 ±14.6% |
| `ijkl-imnk-njml` | 249.9479 | 249.8969 | 254.4539 | 39.7/0.2 | 0.982 ±14.6% |
| `ijkl-minj-nlmk` | 310.0003 | 310.0123 | 314.6013 | 42.3/0.2 | 0.985 ±14.6% |
| `ijkl-mink-jnlm` | 303.5464 | 303.3714 | 307.2673 | 41.9/0.2 | 0.988 ±14.6% |
| `ijkl-minl-njmk` | 300.8089 | 300.5577 | 307.3006 | 40.5/0.1 | 0.979 ±14.6% |
| **geomean** | 29.9385 | 30.0790 | 38.5157 | 70.7/0.2 | 0.777 ±14.6% |

## 16 MiB, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `abc-bk-akc` | 3.8749 | 3.9820 | 5.4562 | 112.9/0.3 | 0.710 ±78.3% |
| `abcijk-eiab-jkec` | 5.2677 | 5.1828 | 8.9349 | 44.8/0.2 | 0.590 ±78.3% |
| `abcijk-eiac-jkeb` | 4.6645 | 4.6495 | 11.8495 | 49.1/0.2 | 0.394 ±78.3% |
| `abcijk-eibc-jkea` | 4.3209 | 4.5922 | 5.1566 | 65.2/0.2 | 0.838 ±78.3% |
| `abcijk-ejab-ikec` | 4.9472 | 4.9573 | 7.3074 | 45.3/0.2 | 0.677 ±78.3% |
| `abcijk-ejac-ikeb` | 4.6640 | 4.6166 | 6.3791 | 48.2/0.2 | 0.731 ±78.3% |
| `abcijk-ejbc-ikea` | 4.2040 | 4.2177 | 5.2108 | 60.8/0.2 | 0.807 ±78.3% |
| `abcijk-ekab-ijec` | 4.9526 | 4.9484 | 6.8240 | 45.0/0.2 | 0.726 ±78.3% |
| `abcijk-ekac-ijeb` | 4.6282 | 4.6288 | 9.0622 | 50.6/0.2 | 0.511 ±78.3% |
| `abcijk-ekbc-ijea` | 4.2781 | 4.2495 | 5.2691 | 63.2/0.2 | 0.812 ±78.3% |
| `abcijk-ijma-mkbc` | 4.3419 | 4.3421 | 5.2381 | 63.8/0.2 | 0.829 ±78.3% |
| `abcijk-ijmb-mkac` | 4.6114 | 4.6123 | 8.7468 | 48.5/0.2 | 0.527 ±78.3% |
| `abcijk-ijmc-mkab` | 4.9587 | 4.9398 | 6.7859 | 48.7/0.2 | 0.731 ±78.3% |
| `abcijk-ikma-mjbc` | 4.3101 | 4.2463 | 5.2296 | 65.2/0.2 | 0.824 ±78.3% |
| `abcijk-ikmb-mjac` | 4.6298 | 4.6331 | 6.3459 | 47.8/0.2 | 0.730 ±78.3% |
| `abcijk-ikmc-mjab` | 4.9341 | 4.9480 | 7.4179 | 45.9/0.2 | 0.665 ±78.3% |
| `abcijk-jkma-mibc` | 4.2525 | 4.3043 | 5.1388 | 63.9/0.2 | 0.828 ±78.3% |
| `abcijk-jkmb-miac` | 4.6209 | 4.6474 | 11.5969 | 49.8/0.2 | 0.398 ±78.3% |
| `abcijk-jkmc-miab` | 5.1914 | 5.1937 | 8.9645 | 43.9/0.2 | 0.579 ±78.3% |
| `abcs-rc-abrs` | 2.7259 | 2.7306 | 5.2831 | 411.9/0.2 | 0.516 ±78.3% |
| `abj-bka-kj` | 5.5175 | 5.4787 | 9.6636 | 136.2/0.3 | 0.571 ±78.3% |
| `abjc-cbka-kj` | 13.1204 | 12.5517 | 8.1200 | 706.7/0.2 | 1.616 ±78.3% |
| `abjc-kbac-jk` | 3.6537 | 3.6392 | 6.4660 | 589.8/0.3 | 0.565 ±78.3% |
| `abjcd-dkbac-jk` | 7.0979 | 7.0789 | 7.2103 | 1560.0/0.2 | 0.984 ±78.3% |
| `abrs-qb-aqrs` | 2.3094 | 2.3290 | 4.3623 | 526.1/0.4 | 0.529 ±78.3% |
| `adbjc-cbdka-kj` | 14.5480 | 14.6770 | 12.8433 | 1580.8/0.2 | 1.133 ±78.3% |
| `ajb-kba-jk` | 4.8658 | 4.7678 | 6.0459 | 111.2/0.3 | 0.805 ±78.3% |
| `ajbc-ckba-jk` | 7.8551 | 7.9559 | 5.4161 | 707.6/0.2 | 1.450 ±78.3% |
| `ajbdc-ckbad-jk` | 6.9043 | 6.9340 | 6.6871 | 1536.2/0.2 | 1.032 ±78.3% |
| `aqrs-pa-pqrs` | 2.4170 | 2.7159 | 4.6925 | 0.5/0.3 | 0.515 ±78.3% |
| `ij-ik-kj` | 31.1190 | 35.2435 | 35.8875 | 1.0/0.5 | 0.867 ±78.3% |
| `ij-ikl-ljk` | 6.6174 | 6.5895 | 7.7442 | 50.6/0.3 | 0.855 ±78.3% |
| `ij-kil-lkj` | 7.9254 | 7.8943 | 9.5885 | 51.1/0.3 | 0.827 ±78.3% |
| `ijk-ikl-lj` | 4.1516 | 4.6234 | 6.4339 | 109.2/0.3 | 0.645 ±78.3% |
| `ijk-il-jlk` | 5.8877 | 5.9551 | 4.7816 | 121.9/0.3 | 1.231 ±78.3% |
| `ijk-ilk-jl` | 3.9967 | 3.9051 | 5.4337 | 127.2/0.4 | 0.736 ±78.3% |
| `ijk-ilk-lj` | 3.9764 | 3.9545 | 5.7078 | 114.7/0.2 | 0.697 ±78.3% |
| `ijk-ilmk-mjl` | 2.1591 | 2.1812 | 3.6360 | 26.1/0.2 | 0.594 ±78.3% |
| `ijkl-imjn-lnkm` | 66.8392 | 66.8545 | 66.9359 | 45.4/0.2 | 0.999 ±78.3% |
| `ijkl-imjn-nlmk` | 67.4180 | 67.4526 | 67.3199 | 41.1/0.2 | 1.001 ±78.3% |
| `ijkl-imkn-jnlm` | 65.8629 | 65.7688 | 68.0613 | 40.3/0.1 | 0.968 ±78.3% |
| `ijkl-imkn-njml` | 65.6918 | 65.7963 | 68.3033 | 39.0/0.1 | 0.962 ±78.3% |
| `ijkl-imln-jnkm` | 64.7661 | 64.7399 | 68.5391 | 40.6/0.1 | 0.945 ±78.3% |
| `ijkl-imln-njmk` | 65.2405 | 65.3070 | 67.8061 | 38.9/0.2 | 0.962 ±78.3% |
| `ijkl-imnj-nlkm` | 66.7707 | 66.8165 | 67.7680 | 40.1/0.2 | 0.985 ±78.3% |
| `ijkl-imnk-njml` | 65.6106 | 65.5417 | 67.5987 | 39.7/0.2 | 0.971 ±78.3% |
| `ijkl-minj-nlmk` | 80.5427 | 80.6073 | 82.8422 | 41.7/0.2 | 0.972 ±78.3% |
| `ijkl-mink-jnlm` | 78.4780 | 78.3601 | 80.1272 | 39.8/0.2 | 0.979 ±78.3% |
| `ijkl-minl-njmk` | 78.1375 | 78.2393 | 80.3832 | 40.8/0.2 | 0.972 ±78.3% |
| **geomean** | 9.1110 | 9.1768 | 11.7175 | 72.1/0.2 | 0.778 ±78.3% |

## 16 MiB, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `abc-bk-akc` | 57.0088 | 57.0414 | 69.2114 | 112.3/0.2 | 0.824 ±2.9% |
| `abcijk-eiab-jkec` | 54.2691 | 54.3236 | 65.6680 | 47.0/0.2 | 0.826 ±2.9% |
| `abcijk-eiac-jkeb` | 53.5528 | 53.5068 | 83.8403 | 52.4/0.2 | 0.639 ±2.9% |
| `abcijk-eibc-jkea` | 54.3598 | 54.3612 | 60.0547 | 68.1/0.2 | 0.905 ±2.9% |
| `abcijk-ejab-ikec` | 53.9767 | 53.9549 | 65.2593 | 48.2/0.2 | 0.827 ±2.9% |
| `abcijk-ejac-ikeb` | 53.4618 | 53.4725 | 65.8144 | 52.7/0.2 | 0.812 ±2.9% |
| `abcijk-ejbc-ikea` | 54.3971 | 54.2593 | 60.4400 | 65.3/0.2 | 0.900 ±2.9% |
| `abcijk-ekab-ijec` | 53.8426 | 53.8521 | 56.7815 | 49.1/0.2 | 0.948 ±2.9% |
| `abcijk-ekac-ijeb` | 53.5014 | 53.4866 | 64.3923 | 52.2/0.2 | 0.831 ±2.9% |
| `abcijk-ekbc-ijea` | 54.2198 | 54.3224 | 60.4154 | 65.1/0.1 | 0.897 ±2.9% |
| `abcijk-ijma-mkbc` | 54.3094 | 54.2761 | 60.4140 | 65.6/0.2 | 0.899 ±2.9% |
| `abcijk-ijmb-mkac` | 53.4606 | 53.4580 | 64.6871 | 51.8/0.2 | 0.826 ±2.9% |
| `abcijk-ijmc-mkab` | 53.9385 | 53.9386 | 57.2267 | 48.2/0.2 | 0.943 ±2.9% |
| `abcijk-ikma-mjbc` | 54.3984 | 54.3325 | 60.3057 | 68.3/0.2 | 0.902 ±2.9% |
| `abcijk-ikmb-mjac` | 53.4833 | 53.4888 | 65.7746 | 53.5/0.2 | 0.813 ±2.9% |
| `abcijk-ikmc-mjab` | 53.9674 | 53.9534 | 65.1292 | 50.2/0.4 | 0.829 ±2.9% |
| `abcijk-jkma-mibc` | 54.3633 | 54.3377 | 60.6130 | 68.1/0.2 | 0.897 ±2.9% |
| `abcijk-jkmb-miac` | 53.5172 | 53.5713 | 83.5420 | 53.9/0.2 | 0.641 ±2.9% |
| `abcijk-jkmc-miab` | 54.3139 | 54.3843 | 64.8542 | 47.0/0.2 | 0.837 ±2.9% |
| `abcs-rc-abrs` | 31.7505 | 31.8331 | 40.0971 | 420.5/0.3 | 0.792 ±2.9% |
| `abj-bka-kj` | 72.3865 | 72.4046 | 97.0970 | 135.1/0.3 | 0.746 ±2.9% |
| `abjc-cbka-kj` | 66.1473 | 66.1355 | 62.3187 | 723.1/0.2 | 1.061 ±2.9% |
| `abjc-kbac-jk` | 39.8413 | 39.9336 | 52.6819 | 596.9/0.2 | 0.756 ±2.9% |
| `abjcd-dkbac-jk` | 43.1868 | 43.2008 | 45.2097 | 1585.3/0.2 | 0.955 ±2.9% |
| `abrs-qb-aqrs` | 33.4247 | 33.4193 | 43.8062 | 545.6/0.2 | 0.763 ±2.9% |
| `adbjc-cbdka-kj` | 69.3320 | 69.4613 | 48.0107 | 1577.9/0.2 | 1.444 ±2.9% |
| `ajb-kba-jk` | 64.2716 | 64.1685 | 75.1960 | 116.5/0.2 | 0.855 ±2.9% |
| `ajbc-ckba-jk` | 48.8249 | 48.8567 | 43.6095 | 707.5/0.2 | 1.120 ±2.9% |
| `ajbdc-ckbad-jk` | 42.8506 | 42.8273 | 44.1369 | 1608.9/0.2 | 0.971 ±2.9% |
| `aqrs-pa-pqrs` | 31.1144 | 31.1866 | 41.1169 | 229.5/0.2 | 0.757 ±2.9% |
| `ij-ik-kj` | 506.0036 | 505.8254 | 524.4928 | 18.0/0.2 | 0.965 ±2.9% |
| `ij-ikl-ljk` | 64.8158 | 64.8464 | 81.3209 | 51.5/0.3 | 0.797 ±2.9% |
| `ij-kil-lkj` | 76.1724 | 76.2197 | 98.6569 | 52.7/0.3 | 0.772 ±2.9% |
| `ijk-ikl-lj` | 59.5333 | 59.5458 | 73.5765 | 116.5/0.2 | 0.809 ±2.9% |
| `ijk-il-jlk` | 57.8189 | 57.8145 | 63.6845 | 120.7/0.3 | 0.908 ±2.9% |
| `ijk-ilk-jl` | 57.2316 | 57.2412 | 69.2436 | 111.7/0.2 | 0.827 ±2.9% |
| `ijk-ilk-lj` | 59.0048 | 58.9970 | 71.5025 | 112.9/0.3 | 0.825 ±2.9% |
| `ijk-ilmk-mjl` | 30.6383 | 30.6548 | 41.7011 | 29.0/0.2 | 0.735 ±2.9% |
| `ijkl-imjn-lnkm` | 970.8916 | 972.1491 | 1024.9934 | 44.6/0.2 | 0.947 ±2.9% |
| `ijkl-imjn-nlmk` | 974.0555 | 973.9266 | 1036.3316 | 42.6/0.2 | 0.940 ±2.9% |
| `ijkl-imkn-jnlm` | 978.1497 | 977.5796 | 1042.2422 | 42.9/0.2 | 0.939 ±2.9% |
| `ijkl-imkn-njml` | 980.8624 | 980.8747 | 1047.5253 | 42.7/0.1 | 0.936 ±2.9% |
| `ijkl-imln-jnkm` | 976.1656 | 976.8332 | 1042.4880 | 43.6/0.1 | 0.936 ±2.9% |
| `ijkl-imln-njmk` | 978.9845 | 979.1682 | 1042.0030 | 40.5/0.2 | 0.940 ±2.9% |
| `ijkl-imnj-nlkm` | 975.1945 | 974.9955 | 1040.3541 | 41.4/0.2 | 0.937 ±2.9% |
| `ijkl-imnk-njml` | 980.3157 | 980.0317 | 1041.3249 | 42.1/0.2 | 0.941 ±2.9% |
| `ijkl-minj-nlmk` | 1179.1154 | 1177.5412 | 1249.5699 | 44.2/0.2 | 0.944 ±2.9% |
| `ijkl-mink-jnlm` | 1178.3528 | 1178.7450 | 1232.7154 | 45.8/0.2 | 0.956 ±2.9% |
| `ijkl-minl-njmk` | 1181.6934 | 1181.7904 | 1247.0236 | 43.5/0.2 | 0.948 ±2.9% |
| **geomean** | 106.9044 | 106.9238 | 122.2990 | 90.3/0.2 | 0.874 ±2.9% |

## 16 MiB, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | prepare (µs) | tprims [plan] / tblis |
|---|---|---|---|---|---|
| `abc-bk-akc` | 14.9016 | 14.5007 | 18.4824 | 115.8/0.2 | 0.806 ±57.0% |
| `abcijk-eiab-jkec` | 14.1571 | 14.1759 | 23.4907 | 47.3/0.2 | 0.603 ±57.0% |
| `abcijk-eiac-jkeb` | 13.6606 | 13.5661 | 27.9389 | 52.9/0.2 | 0.489 ±57.0% |
| `abcijk-eibc-jkea` | 13.8618 | 13.8588 | 15.8343 | 71.0/0.2 | 0.875 ±57.0% |
| `abcijk-ejab-ikec` | 13.8934 | 13.8452 | 18.6910 | 49.5/0.2 | 0.743 ±57.0% |
| `abcijk-ejac-ikeb` | 13.6478 | 13.5390 | 18.3927 | 53.6/0.2 | 0.742 ±57.0% |
| `abcijk-ejbc-ikea` | 13.9343 | 13.8822 | 15.8423 | 65.9/0.2 | 0.880 ±57.0% |
| `abcijk-ekab-ijec` | 13.8970 | 13.8563 | 15.3462 | 50.0/0.2 | 0.906 ±57.0% |
| `abcijk-ekac-ijeb` | 13.6088 | 13.5681 | 20.4743 | 52.7/0.2 | 0.665 ±57.0% |
| `abcijk-ekbc-ijea` | 13.9342 | 13.9415 | 15.8220 | 66.3/0.2 | 0.881 ±57.0% |
| `abcijk-ijma-mkbc` | 13.8230 | 13.8157 | 15.8150 | 71.1/0.2 | 0.874 ±57.0% |
| `abcijk-ijmb-mkac` | 13.7118 | 13.4608 | 20.5941 | 53.4/0.2 | 0.666 ±57.0% |
| `abcijk-ijmc-mkab` | 13.8723 | 13.8776 | 15.4852 | 50.5/0.2 | 0.896 ±57.0% |
| `abcijk-ikma-mjbc` | 13.8048 | 13.8244 | 15.7911 | 68.6/0.2 | 0.874 ±57.0% |
| `abcijk-ikmb-mjac` | 13.6032 | 13.4691 | 18.3594 | 55.6/0.2 | 0.741 ±57.0% |
| `abcijk-ikmc-mjab` | 13.9349 | 13.9179 | 18.7185 | 48.5/0.2 | 0.744 ±57.0% |
| `abcijk-jkma-mibc` | 13.7931 | 13.7854 | 15.8362 | 68.4/0.2 | 0.871 ±57.0% |
| `abcijk-jkmb-miac` | 13.5440 | 13.6800 | 27.7226 | 55.0/0.2 | 0.489 ±57.0% |
| `abcijk-jkmc-miab` | 14.1645 | 14.1623 | 23.1936 | 47.3/0.1 | 0.611 ±57.0% |
| `abcs-rc-abrs` | 8.3724 | 8.2329 | 12.2315 | 404.5/0.2 | 0.684 ±57.0% |
| `abj-bka-kj` | 19.0815 | 19.0972 | 26.7813 | 134.4/0.3 | 0.712 ±57.0% |
| `abjc-cbka-kj` | 20.3244 | 20.0023 | 20.2067 | 736.5/0.2 | 1.006 ±57.0% |
| `abjc-kbac-jk` | 10.5377 | 10.6836 | 17.3290 | 622.2/0.2 | 0.608 ±57.0% |
| `abjcd-dkbac-jk` | 13.4217 | 13.3786 | 12.6621 | 1588.2/0.2 | 1.060 ±57.0% |
| `abrs-qb-aqrs` | 8.5314 | 8.5317 | 12.5752 | 590.2/0.3 | 0.678 ±57.0% |
| `adbjc-cbdka-kj` | 21.1202 | 21.7634 | 18.4385 | 1590.4/0.2 | 1.145 ±57.0% |
| `ajb-kba-jk` | 16.4442 | 16.4844 | 19.9281 | 118.3/0.4 | 0.825 ±57.0% |
| `ajbc-ckba-jk` | 13.6277 | 13.5389 | 13.6398 | 720.4/0.2 | 0.999 ±57.0% |
| `ajbdc-ckbad-jk` | 12.7838 | 12.9197 | 13.0540 | 1601.6/0.2 | 0.979 ±57.0% |
| `aqrs-pa-pqrs` | 8.1026 | 8.1641 | 10.6644 | 228.4/0.3 | 0.760 ±57.0% |
| `ij-ik-kj` | 128.6695 | 128.7208 | 133.4762 | 18.7/0.3 | 0.964 ±57.0% |
| `ij-ikl-ljk` | 22.8491 | 22.8813 | 23.3396 | 62.0/0.3 | 0.979 ±57.0% |
| `ij-kil-lkj` | 26.4825 | 26.5830 | 28.5276 | 60.6/0.3 | 0.928 ±57.0% |
| `ijk-ikl-lj` | 15.3681 | 15.2622 | 20.2842 | 112.1/0.3 | 0.758 ±57.0% |
| `ijk-il-jlk` | 19.7118 | 19.7254 | 16.1547 | 123.4/0.3 | 1.220 ±57.0% |
| `ijk-ilk-jl` | 14.6060 | 14.6902 | 18.3611 | 116.0/0.3 | 0.795 ±57.0% |
| `ijk-ilk-lj` | 15.6431 | 15.1042 | 19.0262 | 115.6/0.3 | 0.822 ±57.0% |
| `ijk-ilmk-mjl` | 8.3312 | 8.3794 | 10.8890 | 29.4/0.2 | 0.765 ±57.0% |
| `ijkl-imjn-lnkm` | 249.2038 | 250.2075 | 263.5435 | 48.6/0.1 | 0.946 ±57.0% |
| `ijkl-imjn-nlmk` | 248.7627 | 248.8241 | 262.8471 | 43.5/0.2 | 0.946 ±57.0% |
| `ijkl-imkn-jnlm` | 247.9667 | 248.0454 | 265.8015 | 42.7/0.2 | 0.933 ±57.0% |
| `ijkl-imkn-njml` | 248.8323 | 248.9111 | 265.3746 | 41.6/0.2 | 0.938 ±57.0% |
| `ijkl-imln-jnkm` | 247.6543 | 247.5355 | 264.2861 | 44.8/0.2 | 0.937 ±57.0% |
| `ijkl-imln-njmk` | 248.6976 | 248.5149 | 264.1862 | 42.4/0.1 | 0.941 ±57.0% |
| `ijkl-imnj-nlkm` | 248.3115 | 248.6625 | 260.5574 | 42.0/0.1 | 0.953 ±57.0% |
| `ijkl-imnk-njml` | 249.2045 | 248.8531 | 260.9749 | 41.6/0.2 | 0.955 ±57.0% |
| `ijkl-minj-nlmk` | 300.5340 | 300.4661 | 318.9619 | 43.9/0.2 | 0.942 ±57.0% |
| `ijkl-mink-jnlm` | 298.7100 | 298.4987 | 316.2564 | 43.4/0.1 | 0.945 ±57.0% |
| `ijkl-minl-njmk` | 299.6431 | 299.9628 | 319.3559 | 44.0/0.1 | 0.938 ±57.0% |
| **geomean** | 28.4281 | 28.3872 | 34.2275 | 92.2/0.2 | 0.831 ±57.0% |
