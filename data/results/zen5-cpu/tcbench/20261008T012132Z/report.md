# `tcbench` on `zen5-cpu`

- tprims-rs commit: `c743ccf6d6de11ed328e79ac3d0b78492c8d61b1`
- features: `upstream\, tblis`
- harness commit: `c743ccf6d6de11ed328e79ac3d0b78492c8d61b1`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-08T01:37:23.789008Z`
- timing policy: v1, best of 5 reps, priming 500 ms
- command: `scripts/record_run.py zen5-cpu tcbench`
- raw data: `data/results/zen5-cpu/tcbench/20261008T012132Z/`
## What was measured

- **Corpus `TCCG`** — One contraction per case, from coupled-cluster (CCSD, CCSD(T)), AO-to-MO integral transformation and tensor-times-matrix workloads. Each case is a full tensor contraction, not a matrix multiply.
  Source: Springer & Bientinesi, "Design of a High-Performance GEMM-like Tensor-Tensor Multiplication" (arXiv:1607.00145), and the accompanying HPAC/tccg benchmark.py. Shapes are rescaled from one nominal tensor size by TCCG's sizing rule, so the extents are a function of that knob rather than physical dimensions.
  Known blind spot: Every case has unit batch extent, so a cost proportional to batch elements is invisible here.
  Known blind spot: Stride-1 extents are rounded up to a multiple of 24, so the corpus is regular by construction.
- **Engines** — one row per engine in every table below:
  - `plan` — This library, with its planner choosing the route per case: the packed driver, or the copy-free faer path, or the elementwise path for an all-batch case.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `packed` — This library with the packed driver forced instead of chosen. A diagnostic arm: it shows what the planner's non-packed routes buy or cost on the same inputs.
    Identity (as measured): tprims — the measured revision itself; see tprims above
  - `upstream` — The original tensorprimitives-rs, called as a separate library through a Cargo git dependency; no source copied. It is the project this library was imported from, and it runs its own planner and its own thread policy.
    Identity (as measured): upstream-tensorprimitives, commit `8cda75e11ed26f46c0c22f9629004c84dbabc8e5` — lkdvos/tensorprimitives-rs, called through a Cargo git dependency
    Caveat: Thread construction differs: this arm builds its own scoped workers after an explicit with_threads(N), while the tprims arms borrow a host pool. Pool creation is outside the timed region, but the policies are not identical.
  - `tblis` — Actual C++ TBLIS through the existing direct FFI adapter, as the third-party reference implementation.
    Identity (as measured): tblis, version 2.0, commit `20cc0bcdb13ddf9fbf619138b6081a16e9e48b7f` — TBLIS 2.0, configuration zen3 (explicit; auto detection selected a generic configuration); bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0
    Caveat: Needs an external install, so it is an arm only for cells whose declaration lists it.
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
- CPU sets: 1T -> `4`, 4T -> `4-7`, 8T -> `4-11`

Every row below passed `tcbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over the timed repetitions (this run made a single complete set, so it carries no A/A) of the best wall time per engine.

## 1 MiB, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.6166 | 0.6173 | 0.6604 | 0.9103 |
| `abcijk-eiab-jkec` | 2.9784 | 2.9394 | 3.0664 | 3.7992 |
| `abcijk-eiac-jkeb` | 2.7518 | 2.7393 | 2.9813 | 5.1764 |
| `abcijk-eibc-jkea` | 2.8735 | 2.8772 | 3.1467 | 3.6553 |
| `abcijk-ejab-ikec` | 2.9225 | 2.8931 | 3.0725 | 3.9990 |
| `abcijk-ejac-ikeb` | 2.7475 | 2.7218 | 2.9657 | 4.0678 |
| `abcijk-ejbc-ikea` | 2.8975 | 2.8683 | 3.1484 | 4.0824 |
| `abcijk-ekab-ijec` | 2.9115 | 2.9081 | 3.0609 | 3.5460 |
| `abcijk-ekac-ijeb` | 2.7514 | 2.7524 | 2.9583 | 4.2545 |
| `abcijk-ekbc-ijea` | 2.8585 | 2.8581 | 3.1422 | 4.0987 |
| `abcijk-ijma-mkbc` | 2.8523 | 2.8521 | 3.1163 | 4.0948 |
| `abcijk-ijmb-mkac` | 2.7843 | 2.6997 | 2.9616 | 4.3862 |
| `abcijk-ijmc-mkab` | 2.9319 | 2.8922 | 3.0685 | 3.4969 |
| `abcijk-ikma-mjbc` | 2.8855 | 2.8629 | 3.1386 | 4.1042 |
| `abcijk-ikmb-mjac` | 2.7406 | 2.7251 | 2.9460 | 3.9093 |
| `abcijk-ikmc-mjab` | 2.9318 | 2.9221 | 3.0790 | 3.9412 |
| `abcijk-jkma-mibc` | 2.8690 | 2.8878 | 3.1300 | 3.6532 |
| `abcijk-jkmb-miac` | 2.7655 | 2.7231 | 2.9602 | 5.1541 |
| `abcijk-jkmc-miab` | 2.9655 | 2.9126 | 3.0372 | 3.8134 |
| `abcs-rc-abrs` | 0.2956 | 0.2945 | 0.3356 | 0.6929 |
| `abj-bka-kj` | 1.1360 | 1.1399 | 1.1916 | 1.7019 |
| `abjc-cbka-kj` | 0.5513 | 0.5485 | 0.5890 | 0.8380 |
| `abjc-kbac-jk` | 0.3269 | 0.3261 | 0.3699 | 0.6939 |
| `abjcd-dkbac-jk` | 3.2454 | 3.2090 | 3.3438 | 5.9922 |
| `abrs-qb-aqrs` | 0.2899 | 0.2889 | 0.3301 | 0.6911 |
| `adbjc-cbdka-kj` | 8.3997 | 8.4315 | 8.6357 | 6.1665 |
| `ajb-kba-jk` | 0.9106 | 0.8732 | 0.9322 | 1.3060 |
| `ajbc-ckba-jk` | 0.4438 | 0.4417 | 0.4839 | 0.7565 |
| `ajbdc-ckbad-jk` | 3.0193 | 2.9223 | 3.4271 | 5.4476 |
| `aqrs-pa-pqrs` | 0.1873 | 0.2828 | 0.3360 | 0.6494 |
| `ij-ik-kj` | 2.8907 | 3.0751 | 3.1942 | 3.6178 |
| `ij-ikl-ljk` | 0.7385 | 0.7369 | 0.7989 | 1.2839 |
| `ij-kil-lkj` | 1.1192 | 1.1132 | 1.1864 | 1.8336 |
| `ijk-ikl-lj` | 0.6616 | 0.6611 | 0.7039 | 1.0674 |
| `ijk-il-jlk` | 0.6538 | 0.6477 | 0.7147 | 0.9482 |
| `ijk-ilk-jl` | 0.6175 | 0.6172 | 0.6612 | 0.9056 |
| `ijk-ilk-lj` | 0.6608 | 0.6592 | 0.7031 | 1.0365 |
| `ijk-ilmk-mjl` | 0.2596 | 0.2593 | 0.2760 | 0.5727 |
| `ijkl-imjn-lnkm` | 3.7790 | 3.7821 | 3.9063 | 4.5144 |
| `ijkl-imjn-nlmk` | 3.7750 | 3.7727 | 3.8822 | 4.5387 |
| `ijkl-imkn-jnlm` | 3.8042 | 3.7469 | 3.8507 | 4.3638 |
| `ijkl-imkn-njml` | 3.7546 | 3.7395 | 3.8523 | 4.5319 |
| `ijkl-imln-jnkm` | 3.7706 | 3.7640 | 3.8262 | 4.3407 |
| `ijkl-imln-njmk` | 3.7688 | 3.7681 | 3.8560 | 4.4776 |
| `ijkl-imnj-nlkm` | 3.7520 | 3.7463 | 3.8477 | 4.4541 |
| `ijkl-imnk-njml` | 3.7512 | 3.7483 | 3.8436 | 4.3757 |
| `ijkl-minj-nlmk` | 4.6496 | 4.6442 | 4.8032 | 5.4582 |
| `ijkl-mink-jnlm` | 4.5404 | 4.5269 | 4.6575 | 5.3623 |
| `ijkl-minl-njmk` | 4.6305 | 4.6267 | 4.7541 | 5.2725 |
| **geomean** | 1.8138 | 1.8209 | 1.9480 | 2.6466 |

## 1 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.1691 | 0.1656 | 0.2333 | 0.2584 |
| `abcijk-eiab-jkec` | 0.9054 | 0.8959 | 0.9461 | 1.4805 |
| `abcijk-eiac-jkeb` | 0.9394 | 0.9474 | 0.8733 | 1.8414 |
| `abcijk-eibc-jkea` | 0.8340 | 0.8826 | 0.9543 | 1.0248 |
| `abcijk-ejab-ikec` | 0.9721 | 0.8478 | 0.9397 | 1.3760 |
| `abcijk-ejac-ikeb` | 0.8207 | 0.7496 | 1.0483 | 1.1888 |
| `abcijk-ejbc-ikea` | 1.0607 | 1.0166 | 0.9827 | 1.1428 |
| `abcijk-ekab-ijec` | 0.9252 | 0.8578 | 0.9401 | 1.1938 |
| `abcijk-ekac-ijeb` | 1.0424 | 0.8171 | 0.9792 | 1.7408 |
| `abcijk-ekbc-ijea` | 1.0826 | 0.8575 | 0.9575 | 1.1397 |
| `abcijk-ijma-mkbc` | 0.8646 | 0.9038 | 0.9991 | 1.1373 |
| `abcijk-ijmb-mkac` | 0.8126 | 0.8200 | 0.9206 | 1.8061 |
| `abcijk-ijmc-mkab` | 0.9073 | 0.8882 | 0.9696 | 1.1532 |
| `abcijk-ikma-mjbc` | 0.9108 | 0.8275 | 0.9644 | 1.1252 |
| `abcijk-ikmb-mjac` | 0.8640 | 0.7649 | 0.9256 | 1.1409 |
| `abcijk-ikmc-mjab` | 1.0739 | 1.0331 | 0.9340 | 1.3422 |
| `abcijk-jkma-mibc` | 1.3300 | 0.8494 | 0.9335 | 1.0287 |
| `abcijk-jkmb-miac` | 0.8248 | 0.8207 | 0.9437 | 1.8766 |
| `abcijk-jkmc-miab` | 0.9603 | 0.8918 | 0.9309 | 1.3407 |
| `abcs-rc-abrs` | 0.0878 | 0.0876 | 0.1412 | 0.2302 |
| `abj-bka-kj` | 0.3007 | 0.2989 | 0.3707 | 0.4641 |
| `abjc-cbka-kj` | 0.1687 | 0.1652 | 0.2391 | 0.2880 |
| `abjc-kbac-jk` | 0.1004 | 0.0961 | 0.1607 | 0.2349 |
| `abjcd-dkbac-jk` | 1.3716 | 1.2595 | 1.3922 | 2.0685 |
| `abrs-qb-aqrs` | 0.0874 | 0.0873 | 0.1454 | 0.2343 |
| `adbjc-cbdka-kj` | 5.2387 | 5.2845 | 5.5967 | 2.5533 |
| `ajb-kba-jk` | 0.2331 | 0.2315 | 0.2964 | 0.3466 |
| `ajbc-ckba-jk` | 0.1358 | 0.1328 | 0.2052 | 0.2566 |
| `ajbdc-ckbad-jk` | 1.2109 | 1.2092 | 1.4260 | 1.9908 |
| `aqrs-pa-pqrs` | 0.1603 | 0.0971 | 0.1730 | 0.2148 |
| `ij-ik-kj` | 0.7383 | 0.7965 | 0.9042 | 1.0246 |
| `ij-ikl-ljk` | 0.4390 | 0.4381 | 0.5308 | 0.7371 |
| `ij-kil-lkj` | 0.6397 | 0.6334 | 0.7638 | 1.0132 |
| `ijk-ikl-lj` | 0.2515 | 0.2483 | 0.3378 | 0.4018 |
| `ijk-il-jlk` | 0.4715 | 0.2400 | 0.3097 | 0.3670 |
| `ijk-ilk-jl` | 0.2271 | 0.2246 | 0.3059 | 0.3386 |
| `ijk-ilk-lj` | 0.2094 | 0.2045 | 0.2845 | 0.3278 |
| `ijk-ilmk-mjl` | 0.0785 | 0.0786 | 0.1310 | 0.1728 |
| `ijkl-imjn-lnkm` | 0.9815 | 0.9791 | 1.0874 | 1.2626 |
| `ijkl-imjn-nlmk` | 0.9591 | 0.9553 | 1.0637 | 1.2267 |
| `ijkl-imkn-jnlm` | 0.9589 | 0.9726 | 1.0496 | 1.2083 |
| `ijkl-imkn-njml` | 0.9716 | 0.9483 | 1.0392 | 1.2178 |
| `ijkl-imln-jnkm` | 0.9609 | 0.9658 | 1.0482 | 1.2057 |
| `ijkl-imln-njmk` | 0.9597 | 0.9549 | 1.0389 | 1.1950 |
| `ijkl-imnj-nlkm` | 0.9572 | 0.9499 | 1.0478 | 1.2040 |
| `ijkl-imnk-njml` | 0.9640 | 0.9488 | 1.0434 | 1.2095 |
| `ijkl-minj-nlmk` | 1.1756 | 1.1763 | 1.3140 | 1.4885 |
| `ijkl-mink-jnlm` | 1.1615 | 1.1613 | 1.2791 | 1.4633 |
| `ijkl-minl-njmk` | 1.1773 | 1.1742 | 1.2842 | 1.4520 |
| **geomean** | 0.5980 | 0.5634 | 0.6760 | 0.8513 |

## 1 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.1046 | 0.0961 | 0.2702 | 0.1556 |
| `abcijk-eiab-jkec` | 0.6313 | 0.5581 | 0.6894 | 0.9110 |
| `abcijk-eiac-jkeb` | 0.5749 | 0.4964 | 0.6544 | 1.0913 |
| `abcijk-eibc-jkea` | 0.5730 | 0.5390 | 0.8286 | 0.6495 |
| `abcijk-ejab-ikec` | 0.5478 | 0.4986 | 0.6748 | 1.0045 |
| `abcijk-ejac-ikeb` | 0.5184 | 0.4985 | 0.6561 | 0.7301 |
| `abcijk-ejbc-ikea` | 0.5956 | 0.5077 | 0.8175 | 0.6722 |
| `abcijk-ekab-ijec` | 0.6091 | 0.4990 | 0.6907 | 0.8635 |
| `abcijk-ekac-ijeb` | 0.5266 | 0.4612 | 0.6350 | 1.0944 |
| `abcijk-ekbc-ijea` | 0.6040 | 0.4980 | 0.8355 | 0.6864 |
| `abcijk-ijma-mkbc` | 0.5607 | 0.4959 | 0.8144 | 0.6720 |
| `abcijk-ijmb-mkac` | 0.5838 | 0.4984 | 0.5944 | 1.0808 |
| `abcijk-ijmc-mkab` | 0.5885 | 0.5074 | 0.6976 | 0.8685 |
| `abcijk-ikma-mjbc` | 0.6328 | 0.5446 | 0.8489 | 0.6902 |
| `abcijk-ikmb-mjac` | 0.5864 | 0.5100 | 0.6395 | 0.7028 |
| `abcijk-ikmc-mjab` | 0.5494 | 0.5169 | 0.7146 | 1.0202 |
| `abcijk-jkma-mibc` | 0.6125 | 0.5086 | 0.8198 | 0.6380 |
| `abcijk-jkmb-miac` | 0.5173 | 0.4991 | 0.6267 | 1.0872 |
| `abcijk-jkmc-miab` | 0.6259 | 0.5879 | 0.6787 | 0.9593 |
| `abcs-rc-abrs` | 0.0562 | 0.0554 | 0.1599 | 0.1600 |
| `abj-bka-kj` | 0.1648 | 0.1592 | 0.2872 | 0.2583 |
| `abjc-cbka-kj` | 0.1184 | 0.1074 | 0.2179 | 0.1908 |
| `abjc-kbac-jk` | 0.0626 | 0.0601 | 0.1632 | 0.1625 |
| `abjcd-dkbac-jk` | 1.0841 | 0.9705 | 1.1643 | 1.5187 |
| `abrs-qb-aqrs` | 0.0561 | 0.0538 | 0.1703 | 0.1615 |
| `adbjc-cbdka-kj` | 3.0704 | 3.0182 | 3.3892 | 2.1045 |
| `ajb-kba-jk` | 0.1287 | 0.1274 | 0.2273 | 0.1976 |
| `ajbc-ckba-jk` | 0.0905 | 0.0913 | 0.2095 | 0.1778 |
| `ajbdc-ckbad-jk` | 0.9671 | 0.9640 | 1.2218 | 1.4749 |
| `aqrs-pa-pqrs` | 0.0423 | 0.0536 | 0.1263 | 0.1484 |
| `ij-ik-kj` | 0.4197 | 0.4231 | 0.5718 | 0.6013 |
| `ij-ikl-ljk` | 0.3111 | 0.3074 | 0.4329 | 0.5816 |
| `ij-kil-lkj` | 0.4489 | 0.4458 | 0.5714 | 0.7959 |
| `ijk-ikl-lj` | 0.1394 | 0.1396 | 0.2456 | 0.2325 |
| `ijk-il-jlk` | 0.1313 | 0.1288 | 0.2291 | 0.2188 |
| `ijk-ilk-jl` | 0.1352 | 0.1312 | 0.3630 | 0.2178 |
| `ijk-ilk-lj` | 0.1419 | 0.1430 | 0.2554 | 0.2328 |
| `ijk-ilmk-mjl` | 0.0760 | 0.0774 | 0.2047 | 0.1602 |
| `ijkl-imjn-lnkm` | 0.8483 | 0.8424 | 0.9832 | 1.0264 |
| `ijkl-imjn-nlmk` | 0.8291 | 0.8361 | 0.9642 | 0.9456 |
| `ijkl-imkn-jnlm` | 0.6001 | 0.5967 | 0.7184 | 0.8586 |
| `ijkl-imkn-njml` | 0.5930 | 0.5886 | 0.6990 | 0.7034 |
| `ijkl-imln-jnkm` | 0.6027 | 0.5948 | 0.7131 | 0.7150 |
| `ijkl-imln-njmk` | 0.6014 | 0.5853 | 0.7003 | 0.6935 |
| `ijkl-imnj-nlkm` | 0.6012 | 0.6017 | 0.7043 | 0.7055 |
| `ijkl-imnk-njml` | 0.6149 | 0.5937 | 0.7002 | 0.6980 |
| `ijkl-minj-nlmk` | 0.7372 | 0.7420 | 0.8652 | 0.8619 |
| `ijkl-mink-jnlm` | 0.7249 | 0.7218 | 0.8271 | 0.8504 |
| `ijkl-minl-njmk` | 0.7247 | 0.7165 | 0.8384 | 0.8447 |
| **geomean** | 0.3699 | 0.3512 | 0.5358 | 0.5568 |

## 1 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 2.4649 | 2.5126 | 2.5481 | 3.0561 |
| `abcijk-eiab-jkec` | 10.9327 | 10.8958 | 11.1866 | 12.5869 |
| `abcijk-eiac-jkeb` | 10.6717 | 10.6710 | 10.8284 | 15.0835 |
| `abcijk-eibc-jkea` | 10.9904 | 10.9069 | 11.2957 | 12.7330 |
| `abcijk-ejab-ikec` | 10.8206 | 10.8099 | 11.0850 | 13.0255 |
| `abcijk-ejac-ikeb` | 10.6775 | 10.6795 | 10.8587 | 13.2016 |
| `abcijk-ejbc-ikea` | 10.9188 | 10.9494 | 11.3174 | 13.8743 |
| `abcijk-ekab-ijec` | 10.8071 | 10.8151 | 11.0830 | 12.1102 |
| `abcijk-ekac-ijeb` | 10.6590 | 10.6645 | 10.8138 | 13.8361 |
| `abcijk-ekbc-ijea` | 10.9017 | 10.9226 | 11.2464 | 13.9699 |
| `abcijk-ijma-mkbc` | 11.0368 | 10.8949 | 11.1941 | 13.8276 |
| `abcijk-ijmb-mkac` | 10.6754 | 10.6687 | 10.8277 | 13.7692 |
| `abcijk-ijmc-mkab` | 10.7779 | 10.8103 | 11.0683 | 11.9700 |
| `abcijk-ikma-mjbc` | 10.9189 | 10.9979 | 11.3088 | 13.9141 |
| `abcijk-ikmb-mjac` | 10.6960 | 10.6820 | 10.8550 | 13.4016 |
| `abcijk-ikmc-mjab` | 10.7715 | 10.7787 | 11.0795 | 12.6700 |
| `abcijk-jkma-mibc` | 10.9029 | 10.8862 | 11.3109 | 12.7371 |
| `abcijk-jkmb-miac` | 10.6703 | 10.6661 | 10.8610 | 15.1466 |
| `abcijk-jkmc-miab` | 10.9339 | 10.9115 | 11.2037 | 12.5188 |
| `abcs-rc-abrs` | 1.1573 | 1.1748 | 1.1622 | 1.5084 |
| `abj-bka-kj` | 3.9788 | 3.9181 | 3.9802 | 5.4643 |
| `abjc-cbka-kj` | 1.8491 | 1.8485 | 1.7969 | 1.8664 |
| `abjc-kbac-jk` | 1.2284 | 1.2542 | 1.2959 | 1.7771 |
| `abjcd-dkbac-jk` | 8.6001 | 8.6600 | 9.0406 | 12.1592 |
| `abrs-qb-aqrs` | 0.9859 | 0.9897 | 1.0289 | 1.5630 |
| `adbjc-cbdka-kj` | 20.2656 | 20.3356 | 20.6280 | 13.0560 |
| `ajb-kba-jk` | 3.4856 | 3.6174 | 3.6276 | 4.7155 |
| `ajbc-ckba-jk` | 1.4422 | 1.4835 | 1.5782 | 1.9220 |
| `ajbdc-ckbad-jk` | 8.4090 | 8.4198 | 8.9135 | 12.2101 |
| `aqrs-pa-pqrs` | 1.2554 | 1.2573 | 1.3126 | 1.4313 |
| `ij-ik-kj` | 12.2989 | 12.2987 | 12.4221 | 10.6233 |
| `ij-ikl-ljk` | 3.0340 | 3.0294 | 3.0863 | 3.6704 |
| `ij-kil-lkj` | 4.7896 | 4.7729 | 4.8879 | 5.2774 |
| `ijk-ikl-lj` | 2.6313 | 2.6299 | 2.6245 | 3.7211 |
| `ijk-il-jlk` | 2.7447 | 2.7699 | 2.8137 | 2.9633 |
| `ijk-ilk-jl` | 2.4614 | 2.5207 | 2.5675 | 3.1166 |
| `ijk-ilk-lj` | 2.6049 | 2.6173 | 2.6501 | 3.4679 |
| `ijk-ilmk-mjl` | 0.9851 | 0.9837 | 1.0057 | 1.2377 |
| `ijkl-imjn-lnkm` | 15.2340 | 15.2229 | 15.4521 | 16.4645 |
| `ijkl-imjn-nlmk` | 15.2364 | 15.2330 | 15.4350 | 16.9645 |
| `ijkl-imkn-jnlm` | 15.2474 | 15.2115 | 15.4445 | 16.3123 |
| `ijkl-imkn-njml` | 15.2114 | 15.2102 | 15.4459 | 16.8496 |
| `ijkl-imln-jnkm` | 15.1756 | 15.1739 | 15.4351 | 16.3734 |
| `ijkl-imln-njmk` | 15.2323 | 15.2090 | 15.4378 | 16.4916 |
| `ijkl-imnj-nlkm` | 15.1254 | 15.1154 | 15.3046 | 16.5215 |
| `ijkl-imnk-njml` | 15.1452 | 15.1407 | 15.3683 | 16.4314 |
| `ijkl-minj-nlmk` | 18.7896 | 18.8213 | 19.1389 | 20.7004 |
| `ijkl-mink-jnlm` | 18.4112 | 18.3322 | 18.6077 | 19.9026 |
| `ijkl-minl-njmk` | 18.7701 | 18.7708 | 19.1737 | 20.3416 |
| **geomean** | 6.9202 | 6.9385 | 7.0834 | 8.2540 |

## 1 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.6334 | 0.6301 | 0.6984 | 0.7938 |
| `abcijk-eiab-jkec` | 2.8805 | 2.8824 | 3.5165 | 3.6570 |
| `abcijk-eiac-jkeb` | 2.6994 | 2.7653 | 2.8856 | 4.4956 |
| `abcijk-eibc-jkea` | 2.8573 | 2.8814 | 3.0414 | 3.3393 |
| `abcijk-ejab-ikec` | 2.8022 | 2.8469 | 2.9634 | 3.5804 |
| `abcijk-ejac-ikeb` | 2.6950 | 2.7305 | 2.8548 | 3.7485 |
| `abcijk-ejbc-ikea` | 2.8574 | 2.9058 | 3.0416 | 3.6677 |
| `abcijk-ekab-ijec` | 2.7745 | 2.7683 | 2.9763 | 3.3338 |
| `abcijk-ekac-ijeb` | 2.7224 | 2.7305 | 2.8795 | 4.1878 |
| `abcijk-ekbc-ijea` | 2.8706 | 3.3969 | 3.0425 | 3.6725 |
| `abcijk-ijma-mkbc` | 2.8063 | 2.8932 | 3.0447 | 3.6558 |
| `abcijk-ijmb-mkac` | 2.7090 | 2.7548 | 2.9299 | 4.1057 |
| `abcijk-ijmc-mkab` | 2.7556 | 2.8236 | 2.9181 | 3.3972 |
| `abcijk-ikma-mjbc` | 2.8798 | 2.9033 | 3.0536 | 3.6389 |
| `abcijk-ikmb-mjac` | 2.7086 | 2.7301 | 2.8850 | 3.7367 |
| `abcijk-ikmc-mjab` | 2.7857 | 2.8306 | 2.9416 | 3.5666 |
| `abcijk-jkma-mibc` | 3.2815 | 2.9244 | 3.0752 | 3.3522 |
| `abcijk-jkmb-miac` | 2.7376 | 3.2950 | 2.9180 | 4.4095 |
| `abcijk-jkmc-miab` | 2.8274 | 2.8444 | 3.0357 | 3.6130 |
| `abcs-rc-abrs` | 0.2992 | 0.2990 | 0.3640 | 0.4427 |
| `abj-bka-kj` | 1.0374 | 1.0306 | 1.1174 | 1.6037 |
| `abjc-cbka-kj` | 0.4890 | 0.5003 | 0.5894 | 0.5927 |
| `abjc-kbac-jk` | 0.3119 | 0.3139 | 0.3846 | 0.5277 |
| `abjcd-dkbac-jk` | 3.1540 | 3.1051 | 3.3257 | 4.0521 |
| `abrs-qb-aqrs` | 0.2561 | 0.2585 | 0.3262 | 0.4693 |
| `adbjc-cbdka-kj` | 6.5582 | 7.0487 | 6.8755 | 5.7332 |
| `ajb-kba-jk` | 0.9099 | 0.9039 | 0.9869 | 1.2098 |
| `ajbc-ckba-jk` | 0.3754 | 0.3801 | 0.4517 | 0.6108 |
| `ajbdc-ckbad-jk` | 3.0439 | 3.0723 | 3.2336 | 3.9963 |
| `aqrs-pa-pqrs` | 0.3732 | 0.3802 | 0.4304 | 0.4042 |
| `ij-ik-kj` | 3.1435 | 3.1279 | 3.2727 | 3.4249 |
| `ij-ikl-ljk` | 1.7540 | 1.7440 | 1.8877 | 1.4657 |
| `ij-kil-lkj` | 2.7203 | 2.6625 | 2.7503 | 2.0576 |
| `ijk-ikl-lj` | 0.9414 | 0.9070 | 0.9824 | 1.2158 |
| `ijk-il-jlk` | 1.6886 | 1.7714 | 1.6862 | 1.0151 |
| `ijk-ilk-jl` | 0.8310 | 0.8126 | 0.8758 | 0.9359 |
| `ijk-ilk-lj` | 0.7361 | 0.7279 | 0.7781 | 0.9166 |
| `ijk-ilmk-mjl` | 0.2803 | 0.2796 | 0.3308 | 0.3334 |
| `ijkl-imjn-lnkm` | 4.2640 | 4.2462 | 4.3731 | 4.4155 |
| `ijkl-imjn-nlmk` | 4.1813 | 4.1919 | 4.2824 | 4.4841 |
| `ijkl-imkn-jnlm` | 4.4750 | 4.2181 | 4.3477 | 4.4108 |
| `ijkl-imkn-njml` | 4.1790 | 4.1645 | 4.2777 | 4.4212 |
| `ijkl-imln-jnkm` | 4.1492 | 4.1759 | 4.3194 | 4.4080 |
| `ijkl-imln-njmk` | 4.1988 | 4.1462 | 4.2867 | 4.3459 |
| `ijkl-imnj-nlkm` | 4.1932 | 4.1556 | 4.2786 | 4.3312 |
| `ijkl-imnk-njml` | 4.1583 | 4.1765 | 4.2539 | 4.3006 |
| `ijkl-minj-nlmk` | 5.2594 | 5.1662 | 5.3211 | 5.4408 |
| `ijkl-mink-jnlm` | 5.1784 | 5.0608 | 5.1757 | 5.3388 |
| `ijkl-minl-njmk` | 5.1646 | 5.2357 | 5.3017 | 5.2870 |
| **geomean** | 1.9892 | 2.0048 | 2.1300 | 2.3865 |

## 1 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.3345 | 0.3317 | 0.6185 | 0.3965 |
| `abcijk-eiab-jkec` | 1.7368 | 1.6646 | 1.9334 | 2.2981 |
| `abcijk-eiac-jkeb` | 1.6699 | 1.6060 | 1.9016 | 2.8661 |
| `abcijk-eibc-jkea` | 1.6631 | 1.6238 | 2.9053 | 2.0482 |
| `abcijk-ejab-ikec` | 1.6857 | 1.6594 | 1.8743 | 2.5324 |
| `abcijk-ejac-ikeb` | 1.6318 | 1.5580 | 1.9722 | 2.4193 |
| `abcijk-ejbc-ikea` | 1.6385 | 1.6284 | 3.0316 | 2.1828 |
| `abcijk-ekab-ijec` | 1.7038 | 1.7050 | 1.9343 | 2.0660 |
| `abcijk-ekac-ijeb` | 1.6338 | 1.6142 | 1.9402 | 2.7411 |
| `abcijk-ekbc-ijea` | 1.6577 | 1.6264 | 3.0255 | 2.1959 |
| `abcijk-ijma-mkbc` | 1.6201 | 1.6347 | 2.7577 | 2.1743 |
| `abcijk-ijmb-mkac` | 1.6518 | 1.6799 | 1.8766 | 2.7109 |
| `abcijk-ijmc-mkab` | 1.6891 | 1.8014 | 1.8361 | 2.1038 |
| `abcijk-ikma-mjbc` | 1.6332 | 1.7061 | 2.7787 | 2.2041 |
| `abcijk-ikmb-mjac` | 1.5821 | 1.5370 | 1.8626 | 2.4440 |
| `abcijk-ikmc-mjab` | 1.7566 | 1.6713 | 1.8648 | 2.5633 |
| `abcijk-jkma-mibc` | 1.5932 | 1.6390 | 2.8397 | 2.0790 |
| `abcijk-jkmb-miac` | 1.6087 | 1.5704 | 1.9095 | 2.8753 |
| `abcijk-jkmc-miab` | 1.7093 | 1.6318 | 1.8990 | 2.3089 |
| `abcs-rc-abrs` | 0.1603 | 0.1563 | 0.2561 | 0.2616 |
| `abj-bka-kj` | 0.5331 | 0.5484 | 0.6609 | 0.8499 |
| `abjc-cbka-kj` | 0.2837 | 0.2610 | 0.4213 | 0.3553 |
| `abjc-kbac-jk` | 0.1728 | 0.1645 | 0.3224 | 0.2776 |
| `abjcd-dkbac-jk` | 2.2463 | 2.2697 | 2.4657 | 2.9847 |
| `abrs-qb-aqrs` | 0.1400 | 0.1394 | 0.2558 | 0.2635 |
| `adbjc-cbdka-kj` | 4.1147 | 4.1193 | 4.3410 | 4.5203 |
| `ajb-kba-jk` | 0.4574 | 0.4578 | 0.5783 | 0.5905 |
| `ajbc-ckba-jk` | 0.2164 | 0.2155 | 0.8603 | 0.3566 |
| `ajbdc-ckbad-jk` | 2.2198 | 2.2078 | 4.1874 | 2.7640 |
| `aqrs-pa-pqrs` | 0.2219 | 0.2150 | 0.2931 | 0.2427 |
| `ij-ik-kj` | 1.5963 | 1.5964 | 1.8224 | 1.8150 |
| `ij-ikl-ljk` | 0.9834 | 0.9664 | 1.1288 | 0.9603 |
| `ij-kil-lkj` | 1.4855 | 1.4747 | 1.6507 | 1.3960 |
| `ijk-ikl-lj` | 0.4816 | 0.4721 | 0.5948 | 0.6150 |
| `ijk-il-jlk` | 0.5040 | 0.5056 | 0.6111 | 0.5493 |
| `ijk-ilk-jl` | 0.4842 | 0.4569 | 0.8366 | 0.5487 |
| `ijk-ilk-lj` | 0.4783 | 0.4856 | 0.5986 | 0.5934 |
| `ijk-ilmk-mjl` | 0.2170 | 0.2160 | 0.3374 | 0.2625 |
| `ijkl-imjn-lnkm` | 3.0182 | 3.0148 | 3.2078 | 3.3871 |
| `ijkl-imjn-nlmk` | 2.6379 | 2.6198 | 2.7491 | 2.5248 |
| `ijkl-imkn-jnlm` | 2.2293 | 2.1260 | 2.3455 | 2.4848 |
| `ijkl-imkn-njml` | 2.1373 | 2.1354 | 2.2842 | 2.3938 |
| `ijkl-imln-jnkm` | 2.1634 | 2.1548 | 2.3280 | 2.4687 |
| `ijkl-imln-njmk` | 2.1250 | 2.1417 | 2.2696 | 2.3415 |
| `ijkl-imnj-nlkm` | 2.1671 | 2.1433 | 2.2965 | 2.3407 |
| `ijkl-imnk-njml` | 2.1312 | 2.1414 | 2.2736 | 2.3125 |
| `ijkl-minj-nlmk` | 2.6667 | 2.6940 | 2.8345 | 2.9476 |
| `ijkl-mink-jnlm` | 2.5725 | 2.5757 | 2.7720 | 2.9815 |
| `ijkl-minl-njmk` | 2.6196 | 2.6359 | 2.8043 | 2.8683 |
| **geomean** | 1.1255 | 1.1143 | 1.4744 | 1.4437 |

## 16 MiB, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 14.8813 | 14.9184 | 15.4143 | 18.5420 |
| `abcijk-eiab-jkec` | 14.7865 | 14.8285 | 15.6017 | 25.9939 |
| `abcijk-eiac-jkeb` | 13.9397 | 13.9704 | 15.8472 | 35.5780 |
| `abcijk-eibc-jkea` | 13.6503 | 13.6384 | 15.2697 | 17.1881 |
| `abcijk-ejab-ikec` | 14.7373 | 14.8141 | 15.5236 | 21.6986 |
| `abcijk-ejac-ikeb` | 13.9642 | 14.0278 | 15.8867 | 19.3477 |
| `abcijk-ejbc-ikea` | 13.7668 | 13.7354 | 15.4104 | 17.2859 |
| `abcijk-ekab-ijec` | 14.7545 | 14.7590 | 15.5100 | 18.0593 |
| `abcijk-ekac-ijeb` | 13.8573 | 13.9034 | 15.8420 | 23.7054 |
| `abcijk-ekbc-ijea` | 13.6946 | 13.6998 | 15.3916 | 17.1046 |
| `abcijk-ijma-mkbc` | 13.7102 | 13.7019 | 15.1826 | 17.0821 |
| `abcijk-ijmb-mkac` | 13.9049 | 13.8812 | 15.8537 | 23.6501 |
| `abcijk-ijmc-mkab` | 14.7961 | 14.7829 | 15.4907 | 18.1464 |
| `abcijk-ikma-mjbc` | 13.7640 | 13.7592 | 15.5680 | 17.1672 |
| `abcijk-ikmb-mjac` | 14.1092 | 14.0307 | 15.9373 | 19.7191 |
| `abcijk-ikmc-mjab` | 14.7749 | 14.7929 | 15.5263 | 21.6227 |
| `abcijk-jkma-mibc` | 13.6585 | 13.6752 | 15.2466 | 17.2623 |
| `abcijk-jkmb-miac` | 13.9014 | 14.0128 | 15.7695 | 35.3758 |
| `abcijk-jkmc-miab` | 14.8675 | 14.8746 | 15.5503 | 25.6660 |
| `abcs-rc-abrs` | 9.3365 | 9.3430 | 9.7589 | 14.7077 |
| `abj-bka-kj` | 19.5059 | 19.5011 | 20.0597 | 29.1629 |
| `abjc-cbka-kj` | 35.8546 | 35.8837 | 36.9218 | 25.5915 |
| `abjc-kbac-jk` | 13.0326 | 13.1494 | 13.0351 | 19.6896 |
| `abjcd-dkbac-jk` | 17.1210 | 17.1878 | 19.4979 | 21.9848 |
| `abrs-qb-aqrs` | 8.5031 | 8.4012 | 8.6405 | 15.9257 |
| `adbjc-cbdka-kj` | 43.1960 | 43.2868 | 45.2116 | 29.2801 |
| `ajb-kba-jk` | 18.1340 | 18.0988 | 18.6130 | 20.3066 |
| `ajbc-ckba-jk` | 19.4681 | 19.4200 | 21.1935 | 18.0778 |
| `ajbdc-ckbad-jk` | 16.8617 | 16.9096 | 19.8113 | 20.6628 |
| `aqrs-pa-pqrs` | 7.3757 | 9.2730 | 10.7337 | 15.7287 |
| `ij-ik-kj` | 157.3991 | 130.1909 | 131.9813 | 134.6146 |
| `ij-ikl-ljk` | 17.6402 | 17.6398 | 18.4481 | 24.1529 |
| `ij-kil-lkj` | 21.5629 | 21.5819 | 22.9669 | 30.4261 |
| `ijk-ikl-lj` | 16.1000 | 16.0940 | 16.1369 | 19.3472 |
| `ijk-il-jlk` | 16.0245 | 15.9115 | 18.7280 | 18.3962 |
| `ijk-ilk-jl` | 14.7952 | 14.8033 | 15.3490 | 18.6459 |
| `ijk-ilk-lj` | 14.9320 | 14.9259 | 15.4581 | 19.8206 |
| `ijk-ilmk-mjl` | 7.2934 | 7.1825 | 7.5271 | 13.3561 |
| `ijkl-imjn-lnkm` | 255.1421 | 254.9252 | 254.1482 | 252.6587 |
| `ijkl-imjn-nlmk` | 254.8669 | 254.4917 | 255.8324 | 255.3151 |
| `ijkl-imkn-jnlm` | 251.3104 | 251.4983 | 259.8075 | 249.9454 |
| `ijkl-imkn-njml` | 252.1963 | 251.2640 | 260.8051 | 257.8934 |
| `ijkl-imln-jnkm` | 249.3807 | 248.7796 | 258.8905 | 252.4648 |
| `ijkl-imln-njmk` | 249.9325 | 248.3322 | 259.9121 | 255.2833 |
| `ijkl-imnj-nlkm` | 254.0279 | 253.4374 | 255.5342 | 256.9018 |
| `ijkl-imnk-njml` | 251.2351 | 249.7019 | 259.3424 | 254.0863 |
| `ijkl-minj-nlmk` | 308.3192 | 309.2407 | 312.9823 | 310.8255 |
| `ijkl-mink-jnlm` | 304.6368 | 304.2094 | 314.0328 | 306.9203 |
| `ijkl-minl-njmk` | 304.1591 | 304.1730 | 314.7978 | 312.4086 |
| **geomean** | 29.9138 | 29.9253 | 31.9147 | 38.1604 |

## 16 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 4.0569 | 3.9526 | 4.1124 | 5.4120 |
| `abcijk-eiab-jkec` | 5.3312 | 5.1987 | 4.8959 | 9.4669 |
| `abcijk-eiac-jkeb` | 5.0145 | 4.6076 | 4.9615 | 11.7018 |
| `abcijk-eibc-jkea` | 4.3520 | 4.2822 | 4.7539 | 5.1440 |
| `abcijk-ejab-ikec` | 4.9892 | 4.9979 | 4.9433 | 7.1195 |
| `abcijk-ejac-ikeb` | 4.6202 | 4.6330 | 5.0439 | 6.5695 |
| `abcijk-ejbc-ikea` | 4.2883 | 4.3141 | 4.7935 | 5.2610 |
| `abcijk-ekab-ijec` | 4.9254 | 4.9689 | 4.8814 | 6.8006 |
| `abcijk-ekac-ijeb` | 4.6194 | 4.6389 | 4.9702 | 8.6761 |
| `abcijk-ekbc-ijea` | 4.3023 | 4.3294 | 4.7784 | 5.2395 |
| `abcijk-ijma-mkbc` | 4.3408 | 4.2764 | 4.7624 | 5.2227 |
| `abcijk-ijmb-mkac` | 4.6187 | 4.6061 | 5.0297 | 9.1934 |
| `abcijk-ijmc-mkab` | 4.9753 | 4.9566 | 4.9000 | 6.8430 |
| `abcijk-ikma-mjbc` | 4.3641 | 4.1908 | 4.7851 | 5.2010 |
| `abcijk-ikmb-mjac` | 4.6429 | 4.6237 | 5.0260 | 6.4929 |
| `abcijk-ikmc-mjab` | 4.9740 | 4.9612 | 4.8716 | 7.3375 |
| `abcijk-jkma-mibc` | 4.3034 | 4.2268 | 4.7755 | 5.1092 |
| `abcijk-jkmb-miac` | 4.6893 | 4.6510 | 5.0834 | 11.8750 |
| `abcijk-jkmc-miab` | 5.1630 | 5.1718 | 4.9053 | 9.1973 |
| `abcs-rc-abrs` | 2.7414 | 2.6282 | 2.6205 | 4.7214 |
| `abj-bka-kj` | 5.6626 | 5.6105 | 5.8511 | 9.0873 |
| `abjc-cbka-kj` | 12.8751 | 12.5975 | 13.7229 | 8.7564 |
| `abjc-kbac-jk` | 3.7547 | 3.4045 | 3.5665 | 6.4515 |
| `abjcd-dkbac-jk` | 7.1266 | 7.1245 | 7.4857 | 7.3591 |
| `abrs-qb-aqrs` | 2.2997 | 2.2249 | 2.3393 | 4.3449 |
| `adbjc-cbdka-kj` | 14.4690 | 14.7885 | 15.4985 | 14.7514 |
| `ajb-kba-jk` | 4.7880 | 4.7341 | 4.9793 | 6.0379 |
| `ajbc-ckba-jk` | 7.9999 | 7.9857 | 8.6763 | 5.6496 |
| `ajbdc-ckbad-jk` | 7.0026 | 7.0157 | 7.6577 | 6.8292 |
| `aqrs-pa-pqrs` | 2.2884 | 2.7440 | 3.3202 | 4.7925 |
| `ij-ik-kj` | 43.0207 | 47.9565 | 35.8900 | 35.6919 |
| `ij-ikl-ljk` | 6.5483 | 6.3910 | 6.7861 | 7.5820 |
| `ij-kil-lkj` | 7.5871 | 7.8632 | 8.0159 | 9.4077 |
| `ijk-ikl-lj` | 4.2540 | 4.1911 | 4.4629 | 6.3322 |
| `ijk-il-jlk` | 5.8235 | 5.7383 | 6.4353 | 4.8181 |
| `ijk-ilk-jl` | 4.0488 | 4.0305 | 4.1387 | 5.3793 |
| `ijk-ilk-lj` | 4.3870 | 4.0058 | 4.2033 | 5.7386 |
| `ijk-ilmk-mjl` | 2.3755 | 2.3147 | 2.2276 | 3.5256 |
| `ijkl-imjn-lnkm` | 67.4800 | 67.1860 | 67.5630 | 65.9668 |
| `ijkl-imjn-nlmk` | 66.1783 | 66.2324 | 66.4149 | 68.1326 |
| `ijkl-imkn-jnlm` | 65.1981 | 65.1296 | 67.3851 | 65.6440 |
| `ijkl-imkn-njml` | 65.5683 | 65.5003 | 67.8430 | 67.7855 |
| `ijkl-imln-jnkm` | 64.8510 | 64.7176 | 67.2017 | 66.0852 |
| `ijkl-imln-njmk` | 65.1924 | 65.1552 | 67.5382 | 67.4300 |
| `ijkl-imnj-nlkm` | 66.5233 | 66.5780 | 67.2677 | 67.4799 |
| `ijkl-imnk-njml` | 65.1888 | 65.2981 | 67.5136 | 67.2960 |
| `ijkl-minj-nlmk` | 80.7430 | 80.8656 | 81.5479 | 83.8094 |
| `ijkl-mink-jnlm` | 78.2717 | 78.3366 | 81.2745 | 79.5849 |
| `ijkl-minl-njmk` | 79.5491 | 79.7071 | 82.3192 | 81.7506 |
| **geomean** | 9.2377 | 9.1888 | 9.5779 | 11.7349 |

## 16 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 2.2011 | 2.4731 | 2.3214 | 3.4574 |
| `abcijk-eiab-jkec` | 3.9062 | 3.9915 | 3.8000 | 6.7253 |
| `abcijk-eiac-jkeb` | 3.6383 | 3.6019 | 3.8485 | 7.3539 |
| `abcijk-eibc-jkea` | 3.7675 | 3.7647 | 3.7944 | 3.7122 |
| `abcijk-ejab-ikec` | 3.9014 | 3.9339 | 3.7840 | 5.3411 |
| `abcijk-ejac-ikeb` | 3.6417 | 3.6629 | 3.8521 | 4.7550 |
| `abcijk-ejbc-ikea` | 3.8039 | 3.7779 | 3.8199 | 3.9451 |
| `abcijk-ekab-ijec` | 3.8639 | 3.9500 | 3.7500 | 5.3430 |
| `abcijk-ekac-ijeb` | 3.6337 | 3.6339 | 3.8562 | 6.8344 |
| `abcijk-ekbc-ijea` | 3.7502 | 3.7342 | 3.8334 | 3.9028 |
| `abcijk-ijma-mkbc` | 3.7443 | 3.7299 | 3.8410 | 3.8963 |
| `abcijk-ijmb-mkac` | 3.5656 | 3.6162 | 3.8551 | 6.8913 |
| `abcijk-ijmc-mkab` | 3.8139 | 3.9537 | 3.7833 | 5.3807 |
| `abcijk-ikma-mjbc` | 3.7494 | 3.7443 | 3.8063 | 3.8837 |
| `abcijk-ikmb-mjac` | 3.7167 | 3.6177 | 3.8660 | 4.7989 |
| `abcijk-ikmc-mjab` | 3.9073 | 3.9595 | 3.8451 | 5.3127 |
| `abcijk-jkma-mibc` | 3.7352 | 3.7060 | 3.7902 | 3.8244 |
| `abcijk-jkmb-miac` | 3.6275 | 3.6007 | 3.8511 | 7.3618 |
| `abcijk-jkmc-miab` | 3.8896 | 3.9895 | 3.7701 | 6.7331 |
| `abcs-rc-abrs` | 2.0067 | 2.0596 | 2.0839 | 4.1525 |
| `abj-bka-kj` | 4.1899 | 4.2863 | 4.4144 | 6.6517 |
| `abjc-cbka-kj` | 8.4872 | 8.2021 | 8.3583 | 6.0756 |
| `abjc-kbac-jk` | 2.4182 | 2.3882 | 2.5486 | 4.7199 |
| `abjcd-dkbac-jk` | 4.4967 | 4.5041 | 4.7567 | 5.1573 |
| `abrs-qb-aqrs` | 1.8252 | 1.5379 | 1.6147 | 2.7720 |
| `adbjc-cbdka-kj` | 8.3093 | 8.3754 | 8.5756 | 8.9711 |
| `ajb-kba-jk` | 2.6558 | 2.6353 | 2.8373 | 3.8019 |
| `ajbc-ckba-jk` | 5.0416 | 5.0796 | 5.4188 | 4.0901 |
| `ajbdc-ckbad-jk` | 4.4013 | 4.4234 | 4.9751 | 4.7012 |
| `aqrs-pa-pqrs` | 1.5190 | 1.7044 | 1.9691 | 2.7369 |
| `ij-ik-kj` | 21.9382 | 24.4553 | 25.2176 | 19.4322 |
| `ij-ikl-ljk` | 3.5304 | 3.3008 | 3.4706 | 5.0718 |
| `ij-kil-lkj` | 4.4562 | 4.4330 | 4.6931 | 6.4569 |
| `ijk-ikl-lj` | 2.4591 | 2.3806 | 2.6658 | 4.1360 |
| `ijk-il-jlk` | 2.3069 | 2.2856 | 2.7515 | 2.5756 |
| `ijk-ilk-jl` | 2.1829 | 2.1610 | 2.3041 | 3.4651 |
| `ijk-ilk-lj` | 2.1933 | 2.2090 | 2.3314 | 3.6416 |
| `ijk-ilmk-mjl` | 1.7224 | 1.3454 | 1.5189 | 1.9421 |
| `ijkl-imjn-lnkm` | 35.8451 | 35.8131 | 36.7239 | 35.8478 |
| `ijkl-imjn-nlmk` | 36.1523 | 36.2222 | 36.8499 | 36.1851 |
| `ijkl-imkn-jnlm` | 33.8145 | 33.7689 | 35.3957 | 36.6128 |
| `ijkl-imkn-njml` | 34.2725 | 34.3233 | 35.2459 | 36.4002 |
| `ijkl-imln-jnkm` | 33.6016 | 33.4016 | 35.2466 | 36.7961 |
| `ijkl-imln-njmk` | 33.6966 | 34.1379 | 35.2753 | 36.2041 |
| `ijkl-imnj-nlkm` | 36.2023 | 36.3201 | 37.0905 | 35.4024 |
| `ijkl-imnk-njml` | 34.2595 | 34.4651 | 35.3473 | 35.6163 |
| `ijkl-minj-nlmk` | 43.4967 | 43.3302 | 44.4065 | 44.1798 |
| `ijkl-mink-jnlm` | 40.8001 | 40.8067 | 42.3730 | 43.7499 |
| `ijkl-minl-njmk` | 41.5686 | 41.5112 | 41.7985 | 44.9326 |
| **geomean** | 5.9953 | 5.9844 | 6.2083 | 7.6577 |

## 16 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 57.3430 | 57.3481 | 57.6483 | 69.6628 |
| `abcijk-eiab-jkec` | 54.4336 | 54.4767 | 56.2950 | 65.4095 |
| `abcijk-eiac-jkeb` | 53.8567 | 53.8320 | 54.6012 | 81.8365 |
| `abcijk-eibc-jkea` | 54.5841 | 54.5657 | 55.5312 | 61.0853 |
| `abcijk-ejab-ikec` | 54.0873 | 54.1184 | 55.7242 | 64.7434 |
| `abcijk-ejac-ikeb` | 53.7932 | 53.8386 | 54.6319 | 66.3122 |
| `abcijk-ejbc-ikea` | 54.5679 | 54.5990 | 55.6729 | 61.3361 |
| `abcijk-ekab-ijec` | 54.1149 | 54.1280 | 55.4285 | 58.2644 |
| `abcijk-ekac-ijeb` | 53.8050 | 53.8054 | 54.5547 | 69.1911 |
| `abcijk-ekbc-ijea` | 54.5634 | 54.5619 | 55.6696 | 61.2795 |
| `abcijk-ijma-mkbc` | 54.4788 | 54.4048 | 55.5731 | 61.0009 |
| `abcijk-ijmb-mkac` | 53.8639 | 53.7929 | 54.4870 | 69.3941 |
| `abcijk-ijmc-mkab` | 54.0521 | 54.1000 | 55.3391 | 58.2564 |
| `abcijk-ikma-mjbc` | 54.5900 | 54.6119 | 55.5271 | 61.2456 |
| `abcijk-ikmb-mjac` | 53.7034 | 53.8022 | 54.5936 | 66.0267 |
| `abcijk-ikmc-mjab` | 54.1411 | 54.1333 | 55.4787 | 64.4303 |
| `abcijk-jkma-mibc` | 54.5550 | 54.5571 | 55.5161 | 61.0939 |
| `abcijk-jkmb-miac` | 53.8072 | 53.8639 | 54.5961 | 81.9048 |
| `abcijk-jkmc-miab` | 54.4202 | 54.4325 | 56.3504 | 65.7272 |
| `abcs-rc-abrs` | 31.9345 | 31.7596 | 31.0501 | 40.3049 |
| `abj-bka-kj` | 73.0886 | 73.1155 | 73.8606 | 97.9466 |
| `abjc-cbka-kj` | 66.6097 | 66.6780 | 67.6679 | 62.9602 |
| `abjc-kbac-jk` | 39.7972 | 39.9544 | 39.2851 | 52.8176 |
| `abjcd-dkbac-jk` | 43.0295 | 43.0721 | 44.6371 | 44.1983 |
| `abrs-qb-aqrs` | 33.3650 | 33.4680 | 32.8879 | 40.3431 |
| `adbjc-cbdka-kj` | 69.9210 | 70.0352 | 71.1667 | 49.3904 |
| `ajb-kba-jk` | 64.3961 | 64.3085 | 64.7461 | 75.5321 |
| `ajbc-ckba-jk` | 48.9132 | 48.9428 | 50.3250 | 42.7645 |
| `ajbdc-ckbad-jk` | 42.8666 | 42.8502 | 43.9780 | 44.1507 |
| `aqrs-pa-pqrs` | 31.1044 | 31.2152 | 32.8901 | 39.3461 |
| `ij-ik-kj` | 507.9267 | 507.7650 | 519.2209 | 529.9715 |
| `ij-ikl-ljk` | 64.9498 | 64.8814 | 67.0212 | 80.3761 |
| `ij-kil-lkj` | 76.1616 | 76.1976 | 78.9966 | 98.7254 |
| `ijk-ikl-lj` | 59.7017 | 59.6527 | 59.9891 | 73.9370 |
| `ijk-il-jlk` | 57.9029 | 57.8980 | 58.5512 | 63.2747 |
| `ijk-ilk-jl` | 57.3579 | 57.5204 | 57.4191 | 69.9403 |
| `ijk-ilk-lj` | 59.2039 | 59.1597 | 59.6853 | 71.9134 |
| `ijk-ilmk-mjl` | 30.7355 | 30.7351 | 30.3109 | 41.7863 |
| `ijkl-imjn-lnkm` | 972.6833 | 974.0458 | 992.9670 | 1037.3145 |
| `ijkl-imjn-nlmk` | 975.7933 | 976.4617 | 993.8115 | 1047.8284 |
| `ijkl-imkn-jnlm` | 978.1406 | 977.4614 | 987.8083 | 1044.5410 |
| `ijkl-imkn-njml` | 981.3900 | 981.2699 | 989.8128 | 1042.5123 |
| `ijkl-imln-jnkm` | 976.9047 | 976.8198 | 984.3419 | 1033.6300 |
| `ijkl-imln-njmk` | 979.7154 | 979.9618 | 987.6386 | 1034.2591 |
| `ijkl-imnj-nlkm` | 975.7824 | 975.1246 | 995.6816 | 1040.8214 |
| `ijkl-imnk-njml` | 981.3687 | 981.6380 | 991.1940 | 1044.2814 |
| `ijkl-minj-nlmk` | 1178.7434 | 1178.2780 | 1203.0900 | 1255.7637 |
| `ijkl-mink-jnlm` | 1178.5621 | 1177.6750 | 1191.0885 | 1255.1288 |
| `ijkl-minl-njmk` | 1183.3935 | 1182.9157 | 1193.6115 | 1248.7982 |
| **geomean** | 107.2036 | 107.2290 | 108.8727 | 122.7195 |

## 16 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 14.5900 | 14.5452 | 14.7352 | 18.6212 |
| `abcijk-eiab-jkec` | 14.1566 | 14.1376 | 14.7337 | 22.6317 |
| `abcijk-eiac-jkeb` | 13.6005 | 13.5692 | 14.0321 | 27.0486 |
| `abcijk-eibc-jkea` | 13.9185 | 13.8826 | 14.2484 | 15.9448 |
| `abcijk-ejab-ikec` | 14.0236 | 13.9170 | 14.2972 | 18.4084 |
| `abcijk-ejac-ikeb` | 13.6693 | 13.6670 | 13.9599 | 17.9980 |
| `abcijk-ejbc-ikea` | 13.9784 | 13.8762 | 14.2396 | 16.0724 |
| `abcijk-ekab-ijec` | 13.8736 | 13.9002 | 14.2689 | 16.3981 |
| `abcijk-ekac-ijeb` | 13.6788 | 13.6194 | 15.0913 | 21.2628 |
| `abcijk-ekbc-ijea` | 13.8701 | 13.9051 | 14.2301 | 16.0119 |
| `abcijk-ijma-mkbc` | 13.8906 | 13.8955 | 14.1963 | 16.0159 |
| `abcijk-ijmb-mkac` | 13.6124 | 13.6518 | 13.9651 | 21.4016 |
| `abcijk-ijmc-mkab` | 13.9078 | 13.9890 | 14.3266 | 16.3197 |
| `abcijk-ikma-mjbc` | 13.9238 | 13.9184 | 14.2125 | 16.0303 |
| `abcijk-ikmb-mjac` | 13.5911 | 13.6230 | 14.0191 | 17.9324 |
| `abcijk-ikmc-mjab` | 13.9000 | 13.9165 | 14.2896 | 18.5037 |
| `abcijk-jkma-mibc` | 13.9685 | 13.8364 | 14.2135 | 16.0805 |
| `abcijk-jkmb-miac` | 13.7580 | 13.6499 | 14.0050 | 26.7429 |
| `abcijk-jkmc-miab` | 14.1300 | 14.1258 | 14.8172 | 22.5370 |
| `abcs-rc-abrs` | 8.4122 | 8.3292 | 7.9761 | 12.3165 |
| `abj-bka-kj` | 19.0738 | 19.0384 | 19.3792 | 26.6216 |
| `abjc-cbka-kj` | 20.4688 | 20.3446 | 20.8875 | 19.0525 |
| `abjc-kbac-jk` | 9.9636 | 10.0348 | 10.6735 | 18.2652 |
| `abjcd-dkbac-jk` | 13.4099 | 13.3468 | 13.7677 | 13.8911 |
| `abrs-qb-aqrs` | 8.5488 | 8.9905 | 8.4755 | 11.7746 |
| `adbjc-cbdka-kj` | 21.1260 | 20.9311 | 20.8755 | 18.6559 |
| `ajb-kba-jk` | 16.4332 | 16.4632 | 16.5863 | 20.0208 |
| `ajbc-ckba-jk` | 13.0260 | 13.1669 | 13.5176 | 13.6833 |
| `ajbdc-ckbad-jk` | 12.9314 | 12.8099 | 13.3773 | 13.2302 |
| `aqrs-pa-pqrs` | 8.0824 | 8.4770 | 8.7177 | 10.3978 |
| `ij-ik-kj` | 128.8936 | 128.7064 | 131.9013 | 134.2628 |
| `ij-ikl-ljk` | 23.0839 | 22.8933 | 23.1381 | 23.0174 |
| `ij-kil-lkj` | 26.5583 | 26.6041 | 27.0897 | 27.9357 |
| `ijk-ikl-lj` | 15.3381 | 15.2908 | 15.3042 | 20.0566 |
| `ijk-il-jlk` | 19.7577 | 19.8735 | 20.0066 | 16.1900 |
| `ijk-ilk-jl` | 14.9192 | 14.5829 | 14.7392 | 18.5299 |
| `ijk-ilk-lj` | 15.0456 | 15.0340 | 15.2687 | 18.9289 |
| `ijk-ilmk-mjl` | 8.0145 | 8.3954 | 8.2418 | 10.8369 |
| `ijkl-imjn-lnkm` | 250.2673 | 249.4758 | 256.8777 | 261.8368 |
| `ijkl-imjn-nlmk` | 248.8213 | 248.9123 | 254.6267 | 262.6390 |
| `ijkl-imkn-jnlm` | 248.0535 | 248.0751 | 250.7948 | 263.1194 |
| `ijkl-imkn-njml` | 249.2479 | 249.2056 | 252.3020 | 263.8246 |
| `ijkl-imln-jnkm` | 247.5389 | 247.6299 | 250.8750 | 263.3635 |
| `ijkl-imln-njmk` | 248.7080 | 248.5471 | 253.5127 | 261.5955 |
| `ijkl-imnj-nlkm` | 248.4115 | 248.3413 | 254.5079 | 262.7680 |
| `ijkl-imnk-njml` | 249.0487 | 249.1052 | 252.4611 | 263.2723 |
| `ijkl-minj-nlmk` | 299.6508 | 299.5684 | 305.7066 | 317.8281 |
| `ijkl-mink-jnlm` | 297.9398 | 297.9655 | 302.0465 | 314.5198 |
| `ijkl-minl-njmk` | 299.8606 | 299.4288 | 302.7013 | 317.5992 |
| **geomean** | 28.3715 | 28.4059 | 28.9799 | 34.2477 |

## 16 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 7.5392 | 7.5597 | 7.7153 | 10.5404 |
| `abcijk-eiab-jkec` | 8.9380 | 8.7115 | 8.5966 | 14.2369 |
| `abcijk-eiac-jkeb` | 8.3619 | 8.3080 | 8.4301 | 16.8515 |
| `abcijk-eibc-jkea` | 8.4578 | 8.3481 | 10.1830 | 9.7184 |
| `abcijk-ejab-ikec` | 8.9618 | 8.5571 | 8.4523 | 11.6968 |
| `abcijk-ejac-ikeb` | 8.2787 | 8.2626 | 8.5238 | 11.0105 |
| `abcijk-ejbc-ikea` | 8.3411 | 8.3763 | 10.2545 | 9.8614 |
| `abcijk-ekab-ijec` | 8.8882 | 8.3875 | 8.6297 | 10.3829 |
| `abcijk-ekac-ijeb` | 8.2512 | 8.2859 | 8.5593 | 13.4399 |
| `abcijk-ekbc-ijea` | 8.3235 | 8.3776 | 10.2529 | 9.7984 |
| `abcijk-ijma-mkbc` | 8.3385 | 8.3906 | 10.1909 | 9.8422 |
| `abcijk-ijmb-mkac` | 8.3078 | 8.3094 | 8.7053 | 13.4951 |
| `abcijk-ijmc-mkab` | 8.8229 | 9.0388 | 9.1354 | 10.4169 |
| `abcijk-ikma-mjbc` | 9.1585 | 8.3417 | 10.2581 | 9.8837 |
| `abcijk-ikmb-mjac` | 8.3312 | 8.3051 | 8.6363 | 11.1555 |
| `abcijk-ikmc-mjab` | 8.8698 | 8.6311 | 8.9441 | 11.6862 |
| `abcijk-jkma-mibc` | 8.3627 | 8.3542 | 10.1471 | 9.7683 |
| `abcijk-jkmb-miac` | 8.2867 | 8.2651 | 8.5368 | 16.8194 |
| `abcijk-jkmc-miab` | 8.9841 | 8.8953 | 9.0623 | 13.9342 |
| `abcs-rc-abrs` | 4.7155 | 4.6350 | 4.6562 | 9.2071 |
| `abj-bka-kj` | 10.4751 | 10.5890 | 10.7431 | 15.6743 |
| `abjc-cbka-kj` | 12.2752 | 12.3746 | 12.4072 | 12.4721 |
| `abjc-kbac-jk` | 6.0320 | 5.9997 | 7.5747 | 10.7142 |
| `abjcd-dkbac-jk` | 8.9358 | 8.7446 | 8.9446 | 10.8000 |
| `abrs-qb-aqrs` | 4.6237 | 4.5886 | 4.6311 | 8.1910 |
| `adbjc-cbdka-kj` | 12.8919 | 12.8507 | 12.9446 | 14.5825 |
| `ajb-kba-jk` | 8.7108 | 8.6140 | 8.6711 | 11.3966 |
| `ajbc-ckba-jk` | 8.5442 | 8.6127 | 36.1783 | 9.5801 |
| `ajbdc-ckbad-jk` | 8.3707 | 8.3572 | 27.7135 | 9.7602 |
| `aqrs-pa-pqrs` | 4.4279 | 4.4223 | 4.6487 | 5.9200 |
| `ij-ik-kj` | 70.5310 | 70.5002 | 73.9197 | 69.2024 |
| `ij-ikl-ljk` | 16.1009 | 16.1555 | 16.3516 | 13.7021 |
| `ij-kil-lkj` | 18.5470 | 18.5747 | 19.2308 | 17.6447 |
| `ijk-ikl-lj` | 8.3804 | 8.3032 | 7.9959 | 11.8578 |
| `ijk-il-jlk` | 13.5812 | 13.5953 | 13.8240 | 8.2805 |
| `ijk-ilk-jl` | 7.6559 | 7.5595 | 8.0114 | 10.5355 |
| `ijk-ilk-lj` | 7.7560 | 7.8463 | 7.8670 | 10.8467 |
| `ijk-ilmk-mjl` | 4.8927 | 4.4771 | 4.9133 | 5.8662 |
| `ijkl-imjn-lnkm` | 131.3308 | 131.2535 | 137.9312 | 133.7630 |
| `ijkl-imjn-nlmk` | 130.4549 | 130.5837 | 135.6099 | 134.2762 |
| `ijkl-imkn-jnlm` | 129.3138 | 129.1550 | 133.0335 | 135.8675 |
| `ijkl-imkn-njml` | 130.4826 | 130.4082 | 133.0631 | 135.2702 |
| `ijkl-imln-jnkm` | 128.8947 | 129.1237 | 132.3548 | 136.9035 |
| `ijkl-imln-njmk` | 129.8975 | 130.0798 | 133.3391 | 134.4057 |
| `ijkl-imnj-nlkm` | 129.9465 | 130.0758 | 134.8348 | 134.0295 |
| `ijkl-imnk-njml` | 131.7511 | 131.6897 | 135.3640 | 134.5871 |
| `ijkl-minj-nlmk` | 158.4101 | 158.1020 | 162.5662 | 162.7858 |
| `ijkl-mink-jnlm` | 154.1846 | 154.1009 | 158.1361 | 161.9759 |
| `ijkl-minl-njmk` | 156.0649 | 156.1116 | 158.8837 | 162.6272 |
| **geomean** | 16.5638 | 16.4371 | 18.2086 | 20.3796 |
