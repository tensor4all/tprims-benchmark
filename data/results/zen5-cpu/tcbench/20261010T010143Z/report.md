# `tcbench` on `zen5-cpu`

- tprims-rs commit: `0ec98136c4c894c00013f25b3c99e4a46097e7e9`
- features: `tblis`
- harness commit: `3b0a8420d01453fbe5c72935e91e10ce80989deb`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-10T01:24:53.050561Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu tcbench --jobs 24`
- raw data: `data/results/zen5-cpu/tcbench/20261010T010143Z/`
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

## 16 MiB, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `abc-bk-akc` | 15.3572 | 15.3606 | 19.1723 | 0.801 ±8.2% |
| `abcijk-eiab-jkec` | 14.8371 | 14.8101 | 24.7297 | 0.600 ±8.2% |
| `abcijk-eiac-jkeb` | 14.0516 | 13.9931 | 34.4541 | 0.408 ±8.2% |
| `abcijk-eibc-jkea` | 13.6401 | 13.6814 | 17.0574 | 0.800 ±8.2% |
| `abcijk-ejab-ikec` | 14.7991 | 14.8089 | 21.0133 | 0.704 ±8.2% |
| `abcijk-ejac-ikeb` | 13.9979 | 13.9811 | 19.0833 | 0.734 ±8.2% |
| `abcijk-ejbc-ikea` | 13.7271 | 13.7302 | 17.1302 | 0.801 ±8.2% |
| `abcijk-ekab-ijec` | 14.8052 | 14.8300 | 18.1460 | 0.816 ±8.2% |
| `abcijk-ekac-ijeb` | 13.8934 | 13.8789 | 23.3337 | 0.595 ±8.2% |
| `abcijk-ekbc-ijea` | 13.7811 | 13.7642 | 16.9729 | 0.812 ±8.2% |
| `abcijk-ijma-mkbc` | 13.6035 | 13.6154 | 17.1115 | 0.795 ±8.2% |
| `abcijk-ijmb-mkac` | 13.9250 | 14.0103 | 23.2920 | 0.598 ±8.2% |
| `abcijk-ijmc-mkab` | 14.8233 | 14.7991 | 18.1244 | 0.818 ±8.2% |
| `abcijk-ikma-mjbc` | 13.7481 | 13.6782 | 17.1308 | 0.803 ±8.2% |
| `abcijk-ikmb-mjac` | 14.0249 | 13.9531 | 19.3415 | 0.725 ±8.2% |
| `abcijk-ikmc-mjab` | 14.8041 | 14.8627 | 21.4675 | 0.690 ±8.2% |
| `abcijk-jkma-mibc` | 13.6488 | 13.6446 | 17.0536 | 0.800 ±8.2% |
| `abcijk-jkmb-miac` | 13.9359 | 13.9818 | 34.3861 | 0.405 ±8.2% |
| `abcijk-jkmc-miab` | 14.8559 | 14.8758 | 24.1141 | 0.616 ±8.2% |
| `abcs-rc-abrs` | 9.1747 | 9.1794 | 14.1786 | 0.647 ±8.2% |
| `abj-bka-kj` | 20.0015 | 19.6554 | 28.9030 | 0.692 ±8.2% |
| `abjc-cbka-kj` | 35.8035 | 35.9017 | 25.7969 | 1.388 ±8.2% |
| `abjc-kbac-jk` | 12.6663 | 12.5797 | 20.3750 | 0.622 ±8.2% |
| `abjcd-dkbac-jk` | 17.2449 | 17.2873 | 21.4603 | 0.804 ±8.2% |
| `abrs-qb-aqrs` | 8.1858 | 8.1986 | 15.1880 | 0.539 ±8.2% |
| `adbjc-cbdka-kj` | 42.7210 | 42.8219 | 29.1269 | 1.467 ±8.2% |
| `ajb-kba-jk` | 18.1499 | 18.1628 | 20.1759 | 0.900 ±8.2% |
| `ajbc-ckba-jk` | 19.4579 | 19.4727 | 18.1291 | 1.073 ±8.2% |
| `ajbdc-ckbad-jk` | 16.7976 | 16.9241 | 20.4694 | 0.821 ±8.2% |
| `aqrs-pa-pqrs` | 7.6148 | 9.2649 | 15.1810 | 0.502 ±8.2% |
| `ij-ik-kj` | 124.8961 | 129.1628 | 133.7644 | 0.934 ±8.2% |
| `ij-ikl-ljk` | 17.6671 | 17.7096 | 24.6531 | 0.717 ±8.2% |
| `ij-kil-lkj` | 21.5841 | 21.6116 | 30.5604 | 0.706 ±8.2% |
| `ijk-ikl-lj` | 15.8999 | 15.9265 | 22.4180 | 0.709 ±8.2% |
| `ijk-il-jlk` | 17.4696 | 17.3221 | 18.7564 | 0.931 ±8.2% |
| `ijk-ilk-jl` | 15.0250 | 14.9988 | 19.2511 | 0.780 ±8.2% |
| `ijk-ilk-lj` | 15.0341 | 15.1191 | 20.3157 | 0.740 ±8.2% |
| `ijk-ilmk-mjl` | 7.2110 | 7.2053 | 13.9322 | 0.518 ±8.2% |
| `ijkl-imjn-lnkm` | 253.9812 | 254.5801 | 252.0134 | 1.008 ±8.2% |
| `ijkl-imjn-nlmk` | 252.7387 | 252.9281 | 259.1016 | 0.975 ±8.2% |
| `ijkl-imkn-jnlm` | 251.9590 | 251.9547 | 254.9540 | 0.988 ±8.2% |
| `ijkl-imkn-njml` | 251.3776 | 251.6860 | 259.3291 | 0.969 ±8.2% |
| `ijkl-imln-jnkm` | 250.9197 | 251.0092 | 256.5354 | 0.978 ±8.2% |
| `ijkl-imln-njmk` | 249.8986 | 249.6830 | 262.8400 | 0.951 ±8.2% |
| `ijkl-imnj-nlkm` | 252.5348 | 252.8034 | 256.1619 | 0.986 ±8.2% |
| `ijkl-imnk-njml` | 250.5837 | 250.6245 | 254.0723 | 0.986 ±8.2% |
| `ijkl-minj-nlmk` | 310.8980 | 311.0496 | 317.7085 | 0.979 ±8.2% |
| `ijkl-mink-jnlm` | 305.4422 | 305.3538 | 308.0968 | 0.991 ±8.2% |
| `ijkl-minl-njmk` | 305.3548 | 305.0373 | 312.0599 | 0.979 ±8.2% |
| **geomean** | 29.8336 | 29.9727 | 38.1477 | 0.782 ±8.2% |

## 16 MiB, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `abc-bk-akc` | 4.0263 | 3.8923 | 5.5052 | 0.731 ±108.6% |
| `abcijk-eiab-jkec` | 5.1592 | 5.2082 | 8.7583 | 0.589 ±108.6% |
| `abcijk-eiac-jkeb` | 4.6458 | 4.6408 | 11.5895 | 0.401 ±108.6% |
| `abcijk-eibc-jkea` | 4.2930 | 4.2987 | 5.0756 | 0.846 ±108.6% |
| `abcijk-ejab-ikec` | 4.9220 | 4.9260 | 7.3499 | 0.670 ±108.6% |
| `abcijk-ejac-ikeb` | 4.6075 | 4.6266 | 6.4280 | 0.717 ±108.6% |
| `abcijk-ejbc-ikea` | 4.3396 | 4.2277 | 5.1712 | 0.839 ±108.6% |
| `abcijk-ekab-ijec` | 4.9026 | 4.8874 | 6.7492 | 0.726 ±108.6% |
| `abcijk-ekac-ijeb` | 4.6263 | 4.6258 | 9.0389 | 0.512 ±108.6% |
| `abcijk-ekbc-ijea` | 4.4983 | 4.2193 | 5.1947 | 0.866 ±108.6% |
| `abcijk-ijma-mkbc` | 4.3050 | 4.3053 | 5.1645 | 0.834 ±108.6% |
| `abcijk-ijmb-mkac` | 4.6125 | 4.6177 | 8.9127 | 0.518 ±108.6% |
| `abcijk-ijmc-mkab` | 4.9463 | 4.9045 | 6.8584 | 0.721 ±108.6% |
| `abcijk-ikma-mjbc` | 4.3019 | 4.2144 | 5.1991 | 0.827 ±108.6% |
| `abcijk-ikmb-mjac` | 4.6269 | 4.6278 | 6.4063 | 0.722 ±108.6% |
| `abcijk-ikmc-mjab` | 4.9200 | 4.9265 | 7.4764 | 0.658 ±108.6% |
| `abcijk-jkma-mibc` | 4.2175 | 4.1244 | 5.1077 | 0.826 ±108.6% |
| `abcijk-jkmb-miac` | 4.6441 | 4.6994 | 11.4374 | 0.406 ±108.6% |
| `abcijk-jkmc-miab` | 5.1389 | 5.1478 | 8.6745 | 0.592 ±108.6% |
| `abcs-rc-abrs` | 2.5207 | 2.5225 | 4.6547 | 0.542 ±108.6% |
| `abj-bka-kj` | 5.4811 | 5.5763 | 9.4460 | 0.580 ±108.6% |
| `abjc-cbka-kj` | 12.9256 | 12.7983 | 8.4809 | 1.524 ±108.6% |
| `abjc-kbac-jk` | 3.6475 | 3.7070 | 6.5659 | 0.556 ±108.6% |
| `abjcd-dkbac-jk` | 7.0588 | 7.0634 | 7.1388 | 0.989 ±108.6% |
| `abrs-qb-aqrs` | 2.2301 | 2.2045 | 4.3244 | 0.516 ±108.6% |
| `adbjc-cbdka-kj` | 15.5904 | 16.2514 | 13.4285 | 1.161 ±108.6% |
| `ajb-kba-jk` | 4.8423 | 5.1128 | 6.0907 | 0.795 ±108.6% |
| `ajbc-ckba-jk` | 8.0410 | 8.0998 | 5.5765 | 1.442 ±108.6% |
| `ajbdc-ckbad-jk` | 6.9227 | 6.9608 | 6.6565 | 1.040 ±108.6% |
| `aqrs-pa-pqrs` | 2.2092 | 2.7718 | 4.6210 | 0.478 ±108.6% |
| `ij-ik-kj` | 31.0132 | 35.4239 | 35.7742 | 0.867 ±108.6% |
| `ij-ikl-ljk` | 6.5991 | 6.5646 | 7.7514 | 0.851 ±108.6% |
| `ij-kil-lkj` | 7.8426 | 7.8364 | 9.5468 | 0.821 ±108.6% |
| `ijk-ikl-lj` | 4.2756 | 4.2581 | 6.0551 | 0.706 ±108.6% |
| `ijk-il-jlk` | 5.4379 | 5.4788 | 4.7801 | 1.138 ±108.6% |
| `ijk-ilk-jl` | 3.9225 | 3.8922 | 5.4566 | 0.719 ±108.6% |
| `ijk-ilk-lj` | 3.9370 | 3.9449 | 5.6686 | 0.695 ±108.6% |
| `ijk-ilmk-mjl` | 2.1079 | 2.1417 | 3.6755 | 0.574 ±108.6% |
| `ijkl-imjn-lnkm` | 66.8806 | 66.8335 | 66.3715 | 1.008 ±108.6% |
| `ijkl-imjn-nlmk` | 66.5056 | 66.4978 | 68.4151 | 0.972 ±108.6% |
| `ijkl-imkn-jnlm` | 64.7211 | 64.7733 | 65.3140 | 0.991 ±108.6% |
| `ijkl-imkn-njml` | 65.5290 | 65.4584 | 68.4413 | 0.957 ±108.6% |
| `ijkl-imln-jnkm` | 64.6011 | 64.4690 | 65.5412 | 0.986 ±108.6% |
| `ijkl-imln-njmk` | 65.0518 | 65.0946 | 67.7309 | 0.960 ±108.6% |
| `ijkl-imnj-nlkm` | 66.5480 | 66.6138 | 67.2131 | 0.990 ±108.6% |
| `ijkl-imnk-njml` | 65.4674 | 65.5181 | 67.2981 | 0.973 ±108.6% |
| `ijkl-minj-nlmk` | 80.8203 | 80.6575 | 82.6215 | 0.978 ±108.6% |
| `ijkl-mink-jnlm` | 78.3710 | 78.3237 | 80.4108 | 0.975 ±108.6% |
| `ijkl-minl-njmk` | 79.8221 | 79.8287 | 82.6612 | 0.966 ±108.6% |
| **geomean** | 9.0647 | 9.1275 | 11.6541 | 0.778 ±108.6% |

## 16 MiB, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `abc-bk-akc` | 57.1352 | 57.1909 | 68.7566 | 0.831 ±3.7% |
| `abcijk-eiab-jkec` | 54.1509 | 54.2783 | 64.3276 | 0.842 ±3.7% |
| `abcijk-eiac-jkeb` | 53.6196 | 53.6505 | 83.2134 | 0.644 ±3.7% |
| `abcijk-eibc-jkea` | 54.2849 | 54.1121 | 59.8590 | 0.907 ±3.7% |
| `abcijk-ejab-ikec` | 53.8971 | 53.9303 | 65.0882 | 0.828 ±3.7% |
| `abcijk-ejac-ikeb` | 53.5595 | 53.6008 | 65.4035 | 0.819 ±3.7% |
| `abcijk-ejbc-ikea` | 54.0881 | 54.2240 | 60.4628 | 0.895 ±3.7% |
| `abcijk-ekab-ijec` | 53.8469 | 53.9247 | 57.6743 | 0.934 ±3.7% |
| `abcijk-ekac-ijeb` | 53.5064 | 53.5860 | 64.5658 | 0.829 ±3.7% |
| `abcijk-ekbc-ijea` | 54.1498 | 54.1267 | 60.4434 | 0.896 ±3.7% |
| `abcijk-ijma-mkbc` | 54.1859 | 54.1240 | 60.4366 | 0.897 ±3.7% |
| `abcijk-ijmb-mkac` | 53.6335 | 53.6152 | 64.4535 | 0.832 ±3.7% |
| `abcijk-ijmc-mkab` | 53.8851 | 53.9057 | 56.7731 | 0.949 ±3.7% |
| `abcijk-ikma-mjbc` | 54.2363 | 54.1645 | 60.3909 | 0.898 ±3.7% |
| `abcijk-ikmb-mjac` | 53.6342 | 53.6526 | 65.6570 | 0.817 ±3.7% |
| `abcijk-ikmc-mjab` | 53.9218 | 53.9552 | 65.1626 | 0.827 ±3.7% |
| `abcijk-jkma-mibc` | 54.3308 | 54.3035 | 60.6478 | 0.896 ±3.7% |
| `abcijk-jkmb-miac` | 53.6856 | 53.6720 | 83.1928 | 0.645 ±3.7% |
| `abcijk-jkmc-miab` | 54.2608 | 54.2124 | 64.3316 | 0.843 ±3.7% |
| `abcs-rc-abrs` | 31.8532 | 31.9017 | 39.9475 | 0.797 ±3.7% |
| `abj-bka-kj` | 72.7386 | 72.6904 | 99.2025 | 0.733 ±3.7% |
| `abjc-cbka-kj` | 66.4119 | 66.4092 | 62.9873 | 1.054 ±3.7% |
| `abjc-kbac-jk` | 40.4987 | 40.4728 | 53.2401 | 0.761 ±3.7% |
| `abjcd-dkbac-jk` | 43.1675 | 43.0913 | 43.9120 | 0.983 ±3.7% |
| `abrs-qb-aqrs` | 33.5703 | 33.4638 | 40.2333 | 0.834 ±3.7% |
| `adbjc-cbdka-kj` | 69.8787 | 69.9547 | 49.3391 | 1.416 ±3.7% |
| `ajb-kba-jk` | 64.2785 | 64.2536 | 75.2668 | 0.854 ±3.7% |
| `ajbc-ckba-jk` | 49.0257 | 48.9593 | 42.2365 | 1.161 ±3.7% |
| `ajbdc-ckbad-jk` | 42.7626 | 42.8469 | 44.4116 | 0.963 ±3.7% |
| `aqrs-pa-pqrs` | 31.1117 | 31.1573 | 40.1481 | 0.775 ±3.7% |
| `ij-ik-kj` | 506.6998 | 506.5787 | 525.9975 | 0.963 ±3.7% |
| `ij-ikl-ljk` | 64.8226 | 64.8365 | 81.1857 | 0.798 ±3.7% |
| `ij-kil-lkj` | 76.3345 | 75.9794 | 99.3219 | 0.769 ±3.7% |
| `ijk-ikl-lj` | 59.5349 | 59.5746 | 74.4157 | 0.800 ±3.7% |
| `ijk-il-jlk` | 57.8080 | 57.7508 | 63.4518 | 0.911 ±3.7% |
| `ijk-ilk-jl` | 56.9942 | 56.9550 | 69.0886 | 0.825 ±3.7% |
| `ijk-ilk-lj` | 58.8603 | 58.8229 | 71.7657 | 0.820 ±3.7% |
| `ijk-ilmk-mjl` | 30.6584 | 30.6955 | 41.6569 | 0.736 ±3.7% |
| `ijkl-imjn-lnkm` | 972.1315 | 972.1239 | 1042.3505 | 0.933 ±3.7% |
| `ijkl-imjn-nlmk` | 975.6827 | 975.9961 | 1052.5834 | 0.927 ±3.7% |
| `ijkl-imkn-jnlm` | 976.9935 | 976.3168 | 1047.7491 | 0.932 ±3.7% |
| `ijkl-imkn-njml` | 980.6834 | 981.3833 | 1058.3132 | 0.927 ±3.7% |
| `ijkl-imln-jnkm` | 975.5633 | 975.7491 | 1047.4130 | 0.931 ±3.7% |
| `ijkl-imln-njmk` | 979.6745 | 979.8642 | 1049.2098 | 0.934 ±3.7% |
| `ijkl-imnj-nlkm` | 976.1116 | 976.0976 | 1047.8698 | 0.932 ±3.7% |
| `ijkl-imnk-njml` | 981.1176 | 981.2456 | 1050.3137 | 0.934 ±3.7% |
| `ijkl-minj-nlmk` | 1179.2921 | 1179.5094 | 1234.6733 | 0.955 ±3.7% |
| `ijkl-mink-jnlm` | 1178.5501 | 1178.9214 | 1246.5808 | 0.945 ±3.7% |
| `ijkl-minl-njmk` | 1183.7266 | 1183.8403 | 1230.5889 | 0.962 ±3.7% |
| **geomean** | 106.9899 | 106.9862 | 122.1243 | 0.876 ±3.7% |

## 16 MiB, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) | tblis (ms) | tprims [plan] / tblis |
|---|---|---|---|---|
| `abc-bk-akc` | 14.6026 | 14.9750 | 18.4749 | 0.790 ±98.1% |
| `abcijk-eiab-jkec` | 14.1689 | 14.2195 | 23.3507 | 0.607 ±98.1% |
| `abcijk-eiac-jkeb` | 13.8069 | 13.5905 | 27.8598 | 0.496 ±98.1% |
| `abcijk-eibc-jkea` | 13.9243 | 13.9590 | 15.7388 | 0.885 ±98.1% |
| `abcijk-ejab-ikec` | 13.9363 | 13.9155 | 18.6629 | 0.747 ±98.1% |
| `abcijk-ejac-ikeb` | 13.6863 | 13.5748 | 18.3380 | 0.746 ±98.1% |
| `abcijk-ejbc-ikea` | 13.8741 | 13.8656 | 15.7786 | 0.879 ±98.1% |
| `abcijk-ekab-ijec` | 13.9438 | 13.9044 | 15.5265 | 0.898 ±98.1% |
| `abcijk-ekac-ijeb` | 13.6160 | 13.4689 | 20.6269 | 0.660 ±98.1% |
| `abcijk-ekbc-ijea` | 13.8577 | 13.8636 | 15.7606 | 0.879 ±98.1% |
| `abcijk-ijma-mkbc` | 13.9655 | 13.9759 | 15.7146 | 0.889 ±98.1% |
| `abcijk-ijmb-mkac` | 13.5853 | 13.7080 | 20.6271 | 0.659 ±98.1% |
| `abcijk-ijmc-mkab` | 13.9123 | 13.9187 | 15.3248 | 0.908 ±98.1% |
| `abcijk-ikma-mjbc` | 13.9478 | 13.9063 | 15.7603 | 0.885 ±98.1% |
| `abcijk-ikmb-mjac` | 13.4710 | 13.5562 | 18.3633 | 0.734 ±98.1% |
| `abcijk-ikmc-mjab` | 13.9511 | 13.9462 | 18.7503 | 0.744 ±98.1% |
| `abcijk-jkma-mibc` | 13.9787 | 13.9514 | 15.7818 | 0.886 ±98.1% |
| `abcijk-jkmb-miac` | 13.5567 | 13.5743 | 27.9261 | 0.485 ±98.1% |
| `abcijk-jkmc-miab` | 14.1773 | 14.1833 | 23.7904 | 0.596 ±98.1% |
| `abcs-rc-abrs` | 8.3136 | 8.3959 | 12.2389 | 0.679 ±98.1% |
| `abj-bka-kj` | 19.0830 | 19.0104 | 26.8399 | 0.711 ±98.1% |
| `abjc-cbka-kj` | 20.2265 | 20.2617 | 19.7430 | 1.024 ±98.1% |
| `abjc-kbac-jk` | 10.7090 | 10.9319 | 17.9773 | 0.596 ±98.1% |
| `abjcd-dkbac-jk` | 13.3264 | 13.3943 | 13.5264 | 0.985 ±98.1% |
| `abrs-qb-aqrs` | 8.4720 | 8.4067 | 11.7117 | 0.723 ±98.1% |
| `adbjc-cbdka-kj` | 21.8444 | 22.3027 | 18.9142 | 1.155 ±98.1% |
| `ajb-kba-jk` | 16.4439 | 16.4295 | 19.9285 | 0.825 ±98.1% |
| `ajbc-ckba-jk` | 13.1489 | 13.4236 | 13.1658 | 0.999 ±98.1% |
| `ajbdc-ckbad-jk` | 12.8906 | 12.8776 | 13.1883 | 0.977 ±98.1% |
| `aqrs-pa-pqrs` | 8.1528 | 8.1634 | 10.5311 | 0.774 ±98.1% |
| `ij-ik-kj` | 128.7426 | 128.7010 | 134.8465 | 0.955 ±98.1% |
| `ij-ikl-ljk` | 22.9058 | 22.8998 | 23.3402 | 0.981 ±98.1% |
| `ij-kil-lkj` | 26.4901 | 26.4697 | 28.4786 | 0.930 ±98.1% |
| `ijk-ikl-lj` | 15.1426 | 15.1948 | 20.1127 | 0.753 ±98.1% |
| `ijk-il-jlk` | 19.7522 | 19.6539 | 16.1320 | 1.224 ±98.1% |
| `ijk-ilk-jl` | 14.5863 | 14.9576 | 18.3852 | 0.793 ±98.1% |
| `ijk-ilk-lj` | 15.0010 | 15.0448 | 18.9263 | 0.793 ±98.1% |
| `ijk-ilmk-mjl` | 8.3488 | 8.3613 | 10.9794 | 0.760 ±98.1% |
| `ijkl-imjn-lnkm` | 249.7510 | 250.7545 | 260.5340 | 0.959 ±98.1% |
| `ijkl-imjn-nlmk` | 248.6352 | 249.0003 | 261.4991 | 0.951 ±98.1% |
| `ijkl-imkn-jnlm` | 247.5923 | 247.6871 | 264.9591 | 0.934 ±98.1% |
| `ijkl-imkn-njml` | 248.9073 | 248.9105 | 263.8250 | 0.943 ±98.1% |
| `ijkl-imln-jnkm` | 247.2215 | 247.2620 | 264.6965 | 0.934 ±98.1% |
| `ijkl-imln-njmk` | 248.1779 | 248.1078 | 262.1417 | 0.947 ±98.1% |
| `ijkl-imnj-nlkm` | 248.8651 | 248.3106 | 262.5967 | 0.948 ±98.1% |
| `ijkl-imnk-njml` | 249.0229 | 249.2767 | 260.1385 | 0.957 ±98.1% |
| `ijkl-minj-nlmk` | 301.5618 | 301.5173 | 318.9874 | 0.945 ±98.1% |
| `ijkl-mink-jnlm` | 298.5019 | 298.5902 | 314.7239 | 0.948 ±98.1% |
| `ijkl-minl-njmk` | 300.6296 | 300.2436 | 318.3006 | 0.944 ±98.1% |
| **geomean** | 28.4123 | 28.4711 | 34.2080 | 0.831 ±98.1% |
