# `tcbench` on `zen5-cpu`

- tprims-rs commit: `c743ccf6d6de11ed328e79ac3d0b78492c8d61b1`
- features: `upstream\, tblis`
- harness commit: `c90655cc714b06238ca7b459c9db019bec8771d8`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-08T01:56:11.472014Z`
- timing policy: v1, best of 5 reps, priming 500 ms
- command: `scripts/record_run.py zen5-cpu tcbench`
- raw data: `data/results/zen5-cpu/tcbench/20261008T014102Z/`
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
| `abc-bk-akc` | 0.6169 | 0.6163 | 0.6610 | 0.9097 |
| `abcijk-eiab-jkec` | 2.9757 | 2.9506 | 3.0337 | 3.7228 |
| `abcijk-eiac-jkeb` | 2.7526 | 2.7410 | 2.9731 | 5.2315 |
| `abcijk-eibc-jkea` | 2.8653 | 2.8738 | 3.1594 | 3.5786 |
| `abcijk-ejab-ikec` | 2.9140 | 2.9151 | 3.0674 | 4.0701 |
| `abcijk-ejac-ikeb` | 2.7395 | 2.7257 | 2.9619 | 4.0737 |
| `abcijk-ejbc-ikea` | 2.9144 | 2.8812 | 3.1372 | 4.0303 |
| `abcijk-ekab-ijec` | 2.9186 | 2.8918 | 3.0333 | 3.5202 |
| `abcijk-ekac-ijeb` | 2.7693 | 2.7431 | 2.9642 | 4.2679 |
| `abcijk-ekbc-ijea` | 2.8528 | 2.8670 | 3.1411 | 3.9501 |
| `abcijk-ijma-mkbc` | 2.8677 | 2.8641 | 3.1616 | 4.0032 |
| `abcijk-ijmb-mkac` | 2.7322 | 2.7199 | 2.9994 | 4.2526 |
| `abcijk-ijmc-mkab` | 2.9387 | 2.8894 | 3.0537 | 3.5224 |
| `abcijk-ikma-mjbc` | 2.8962 | 2.8653 | 3.1485 | 3.9452 |
| `abcijk-ikmb-mjac` | 2.7603 | 2.7187 | 2.9888 | 4.0705 |
| `abcijk-ikmc-mjab` | 2.9289 | 2.9070 | 3.0400 | 3.9610 |
| `abcijk-jkma-mibc` | 2.8614 | 2.8752 | 3.1462 | 3.6411 |
| `abcijk-jkmb-miac` | 2.7876 | 2.7123 | 3.0133 | 5.1779 |
| `abcijk-jkmc-miab` | 2.9676 | 2.9485 | 3.0515 | 3.8394 |
| `abcs-rc-abrs` | 0.3013 | 0.2976 | 0.3381 | 0.6928 |
| `abj-bka-kj` | 1.1347 | 1.1292 | 1.1908 | 1.7272 |
| `abjc-cbka-kj` | 0.6186 | 0.5935 | 0.6258 | 0.8506 |
| `abjc-kbac-jk` | 0.3326 | 0.3297 | 0.3737 | 0.6881 |
| `abjcd-dkbac-jk` | 3.2708 | 3.2052 | 3.2846 | 5.9190 |
| `abrs-qb-aqrs` | 0.2901 | 0.2889 | 0.3304 | 0.6901 |
| `adbjc-cbdka-kj` | 8.5261 | 8.5306 | 8.7837 | 6.2254 |
| `ajb-kba-jk` | 0.8974 | 0.8823 | 0.9300 | 1.2674 |
| `ajbc-ckba-jk` | 0.4426 | 0.4390 | 0.4908 | 0.7467 |
| `ajbdc-ckbad-jk` | 2.9290 | 2.8973 | 3.5880 | 5.5457 |
| `aqrs-pa-pqrs` | 0.1872 | 0.2819 | 0.3352 | 0.6530 |
| `ij-ik-kj` | 2.8974 | 3.0996 | 3.2019 | 3.6491 |
| `ij-ikl-ljk` | 0.7427 | 0.7427 | 0.7982 | 1.2831 |
| `ij-kil-lkj` | 1.1169 | 1.1139 | 1.1759 | 1.8259 |
| `ijk-ikl-lj` | 0.6599 | 0.6597 | 0.7025 | 1.0544 |
| `ijk-il-jlk` | 0.6431 | 0.6437 | 0.7117 | 0.9560 |
| `ijk-ilk-jl` | 0.6179 | 0.6172 | 0.6611 | 0.8982 |
| `ijk-ilk-lj` | 0.6606 | 0.6592 | 0.7036 | 1.0403 |
| `ijk-ilmk-mjl` | 0.2599 | 0.2598 | 0.2757 | 0.5719 |
| `ijkl-imjn-lnkm` | 3.7814 | 3.7894 | 3.9046 | 4.4985 |
| `ijkl-imjn-nlmk` | 3.7613 | 3.7727 | 3.8789 | 4.5400 |
| `ijkl-imkn-jnlm` | 3.7559 | 3.7554 | 3.8789 | 4.3535 |
| `ijkl-imkn-njml` | 3.7504 | 3.7439 | 3.8337 | 4.4731 |
| `ijkl-imln-jnkm` | 3.7961 | 3.8079 | 3.8441 | 4.3701 |
| `ijkl-imln-njmk` | 3.7449 | 3.7415 | 3.9612 | 4.7018 |
| `ijkl-imnj-nlkm` | 3.7424 | 3.8404 | 3.8718 | 4.4422 |
| `ijkl-imnk-njml` | 3.7370 | 3.7921 | 3.8573 | 4.4064 |
| `ijkl-minj-nlmk` | 4.6401 | 4.6417 | 4.8426 | 5.5866 |
| `ijkl-mink-jnlm` | 4.5289 | 4.5261 | 4.7123 | 5.3475 |
| `ijkl-minl-njmk` | 4.6104 | 4.6405 | 4.7904 | 5.3893 |
| **geomean** | 1.8172 | 1.8272 | 1.9568 | 2.6453 |

## 1 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.1678 | 0.1691 | 0.2282 | 0.2515 |
| `abcijk-eiab-jkec` | 0.8724 | 0.9113 | 1.0212 | 1.3919 |
| `abcijk-eiac-jkeb` | 0.8380 | 0.7808 | 0.8840 | 1.8265 |
| `abcijk-eibc-jkea` | 0.8701 | 0.8113 | 0.9967 | 1.0019 |
| `abcijk-ejab-ikec` | 0.8901 | 0.8439 | 1.0846 | 1.3733 |
| `abcijk-ejac-ikeb` | 0.9995 | 0.8335 | 0.8867 | 1.1898 |
| `abcijk-ejbc-ikea` | 0.8627 | 0.8571 | 0.9855 | 1.1230 |
| `abcijk-ekab-ijec` | 0.8982 | 0.8214 | 0.9412 | 1.3309 |
| `abcijk-ekac-ijeb` | 0.8463 | 0.9557 | 0.8768 | 1.8859 |
| `abcijk-ekbc-ijea` | 0.8632 | 0.8283 | 1.0053 | 1.1156 |
| `abcijk-ijma-mkbc` | 0.8462 | 0.7936 | 1.0128 | 1.1643 |
| `abcijk-ijmb-mkac` | 1.0481 | 0.7886 | 0.8817 | 1.7832 |
| `abcijk-ijmc-mkab` | 0.8645 | 0.8055 | 0.9412 | 1.1855 |
| `abcijk-ikma-mjbc` | 0.8490 | 0.8229 | 1.0056 | 1.5126 |
| `abcijk-ikmb-mjac` | 0.9835 | 0.7649 | 0.9131 | 1.1646 |
| `abcijk-ikmc-mjab` | 0.8961 | 0.8743 | 0.9241 | 1.3697 |
| `abcijk-jkma-mibc` | 0.8534 | 0.8033 | 0.9902 | 1.0666 |
| `abcijk-jkmb-miac` | 0.8304 | 0.7691 | 0.9157 | 1.8707 |
| `abcijk-jkmc-miab` | 0.8892 | 0.8711 | 0.9650 | 1.3254 |
| `abcs-rc-abrs` | 0.0877 | 0.0878 | 0.1479 | 0.2323 |
| `abj-bka-kj` | 0.3094 | 0.3049 | 0.3659 | 0.4657 |
| `abjc-cbka-kj` | 0.1725 | 0.1701 | 0.2387 | 0.2772 |
| `abjc-kbac-jk` | 0.1149 | 0.1142 | 0.1679 | 0.2375 |
| `abjcd-dkbac-jk` | 1.3016 | 1.2317 | 1.3516 | 2.0885 |
| `abrs-qb-aqrs` | 0.0872 | 0.0866 | 0.1505 | 0.2313 |
| `adbjc-cbdka-kj` | 5.4480 | 5.0291 | 5.6225 | 2.7363 |
| `ajb-kba-jk` | 0.2446 | 0.2335 | 0.2911 | 0.3415 |
| `ajbc-ckba-jk` | 0.1354 | 0.1323 | 0.1967 | 0.2482 |
| `ajbdc-ckbad-jk` | 1.2611 | 1.2466 | 1.4497 | 1.9498 |
| `aqrs-pa-pqrs` | 0.2023 | 0.2997 | 0.2058 | 0.2156 |
| `ij-ik-kj` | 0.7446 | 0.8044 | 0.9041 | 1.0202 |
| `ij-ikl-ljk` | 0.4521 | 0.4460 | 0.5331 | 0.7361 |
| `ij-kil-lkj` | 0.7050 | 0.7007 | 0.7619 | 1.0257 |
| `ijk-ikl-lj` | 0.2524 | 0.2502 | 0.3308 | 0.4057 |
| `ijk-il-jlk` | 0.4564 | 0.2297 | 0.2960 | 0.3419 |
| `ijk-ilk-jl` | 0.1909 | 0.1895 | 0.2492 | 0.2910 |
| `ijk-ilk-lj` | 0.1795 | 0.1779 | 0.2423 | 0.2872 |
| `ijk-ilmk-mjl` | 0.0763 | 0.0850 | 0.1616 | 0.2570 |
| `ijkl-imjn-lnkm` | 0.9751 | 0.9791 | 1.0871 | 1.2327 |
| `ijkl-imjn-nlmk` | 0.9836 | 0.9583 | 1.0719 | 1.2534 |
| `ijkl-imkn-jnlm` | 0.9560 | 0.9525 | 1.0486 | 1.1928 |
| `ijkl-imkn-njml` | 0.9812 | 0.9784 | 1.0540 | 1.2230 |
| `ijkl-imln-jnkm` | 0.9641 | 0.9519 | 1.0536 | 1.1891 |
| `ijkl-imln-njmk` | 0.9580 | 0.9564 | 1.0401 | 1.2080 |
| `ijkl-imnj-nlkm` | 0.9609 | 0.9564 | 1.0449 | 1.2235 |
| `ijkl-imnk-njml` | 0.9516 | 0.9855 | 1.0352 | 1.2007 |
| `ijkl-minj-nlmk` | 1.1859 | 1.1860 | 1.3083 | 1.4847 |
| `ijkl-mink-jnlm` | 1.1654 | 1.1623 | 1.3596 | 1.4647 |
| `ijkl-minl-njmk` | 1.1773 | 1.1967 | 1.3009 | 1.4703 |
| **geomean** | 0.5875 | 0.5683 | 0.6778 | 0.8597 |

## 1 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.1097 | 0.0943 | 0.2727 | 0.1507 |
| `abcijk-eiab-jkec` | 0.6277 | 0.5744 | 0.6572 | 0.8642 |
| `abcijk-eiac-jkeb` | 0.5857 | 0.5362 | 0.6442 | 1.0573 |
| `abcijk-eibc-jkea` | 0.6063 | 0.5433 | 0.8154 | 0.6651 |
| `abcijk-ejab-ikec` | 0.5844 | 0.4911 | 0.6241 | 0.8463 |
| `abcijk-ejac-ikeb` | 0.5573 | 0.4874 | 0.6438 | 0.7432 |
| `abcijk-ejbc-ikea` | 0.5630 | 0.5148 | 0.8268 | 0.6809 |
| `abcijk-ekab-ijec` | 0.5652 | 0.4994 | 0.6651 | 0.8428 |
| `abcijk-ekac-ijeb` | 0.5408 | 0.4812 | 0.6121 | 1.1040 |
| `abcijk-ekbc-ijea` | 0.5883 | 0.5586 | 0.8337 | 0.6585 |
| `abcijk-ijma-mkbc` | 0.5689 | 0.5216 | 0.7807 | 0.6830 |
| `abcijk-ijmb-mkac` | 0.5297 | 0.4594 | 0.6268 | 1.0852 |
| `abcijk-ijmc-mkab` | 0.5703 | 0.5106 | 0.6735 | 0.7790 |
| `abcijk-ikma-mjbc` | 0.6637 | 0.5626 | 0.8331 | 0.6862 |
| `abcijk-ikmb-mjac` | 0.5511 | 0.5580 | 0.6243 | 0.7071 |
| `abcijk-ikmc-mjab` | 0.5535 | 0.5117 | 0.6900 | 0.9987 |
| `abcijk-jkma-mibc` | 0.6105 | 0.5885 | 0.8390 | 0.6676 |
| `abcijk-jkmb-miac` | 0.5607 | 0.5085 | 0.6609 | 1.0232 |
| `abcijk-jkmc-miab` | 0.6010 | 0.5897 | 0.6610 | 0.9354 |
| `abcs-rc-abrs` | 0.0565 | 0.0544 | 0.1739 | 0.1588 |
| `abj-bka-kj` | 0.1612 | 0.1611 | 0.2550 | 0.2351 |
| `abjc-cbka-kj` | 0.1012 | 0.1019 | 0.2327 | 0.1894 |
| `abjc-kbac-jk` | 0.0604 | 0.0614 | 0.1609 | 0.1645 |
| `abjcd-dkbac-jk` | 1.0793 | 0.9579 | 1.0879 | 1.5073 |
| `abrs-qb-aqrs` | 0.0561 | 0.0541 | 0.1732 | 0.1593 |
| `adbjc-cbdka-kj` | 3.1282 | 3.1590 | 3.3469 | 2.0663 |
| `ajb-kba-jk` | 0.1307 | 0.1296 | 0.2202 | 0.1957 |
| `ajbc-ckba-jk` | 0.0859 | 0.0856 | 0.2141 | 0.1756 |
| `ajbdc-ckbad-jk` | 0.9686 | 0.9429 | 1.2023 | 1.4611 |
| `aqrs-pa-pqrs` | 0.1229 | 0.3115 | 0.1266 | 0.1493 |
| `ij-ik-kj` | 0.4480 | 0.4201 | 0.5855 | 0.6063 |
| `ij-ikl-ljk` | 0.3118 | 0.3038 | 0.4291 | 0.5849 |
| `ij-kil-lkj` | 0.4456 | 0.4427 | 0.5720 | 0.8069 |
| `ijk-ikl-lj` | 0.1433 | 0.1395 | 0.2748 | 0.2368 |
| `ijk-il-jlk` | 0.3690 | 0.1296 | 0.2299 | 0.2142 |
| `ijk-ilk-jl` | 0.1335 | 0.1318 | 0.3640 | 0.2145 |
| `ijk-ilk-lj` | 0.1414 | 0.1414 | 0.3180 | 0.2349 |
| `ijk-ilmk-mjl` | 0.5438 | 0.1907 | 0.1994 | 0.1563 |
| `ijkl-imjn-lnkm` | 0.8485 | 0.8515 | 0.9983 | 0.9937 |
| `ijkl-imjn-nlmk` | 0.6935 | 0.6813 | 0.7912 | 0.7552 |
| `ijkl-imkn-jnlm` | 0.5992 | 0.6005 | 0.6955 | 0.7003 |
| `ijkl-imkn-njml` | 0.6103 | 0.6041 | 0.6919 | 0.6957 |
| `ijkl-imln-jnkm` | 0.6104 | 0.5933 | 0.7013 | 0.6875 |
| `ijkl-imln-njmk` | 0.6236 | 0.6010 | 0.6988 | 0.6903 |
| `ijkl-imnj-nlkm` | 0.5978 | 0.6032 | 0.7210 | 0.7040 |
| `ijkl-imnk-njml` | 0.6095 | 0.5875 | 0.7022 | 0.6982 |
| `ijkl-minj-nlmk` | 0.7392 | 0.7245 | 0.8641 | 0.8537 |
| `ijkl-mink-jnlm` | 0.7306 | 0.7091 | 0.8408 | 0.8433 |
| `ijkl-minl-njmk` | 0.7344 | 0.7146 | 0.8262 | 0.8408 |
| **geomean** | 0.4002 | 0.3723 | 0.5331 | 0.5439 |

## 1 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 2.4810 | 2.5699 | 2.5465 | 3.0558 |
| `abcijk-eiab-jkec` | 10.9755 | 10.9740 | 11.2203 | 12.4868 |
| `abcijk-eiac-jkeb` | 10.6749 | 10.6686 | 10.8410 | 14.9537 |
| `abcijk-eibc-jkea` | 10.9434 | 10.8718 | 11.2452 | 12.3875 |
| `abcijk-ejab-ikec` | 10.8566 | 10.8747 | 11.0856 | 12.8755 |
| `abcijk-ejac-ikeb` | 10.7203 | 10.6532 | 10.8616 | 13.2502 |
| `abcijk-ejbc-ikea` | 10.8898 | 10.9184 | 11.2274 | 13.5721 |
| `abcijk-ekab-ijec` | 10.8654 | 10.8577 | 11.0522 | 11.9217 |
| `abcijk-ekac-ijeb` | 10.6278 | 10.5996 | 10.8196 | 13.6868 |
| `abcijk-ekbc-ijea` | 10.9520 | 10.8868 | 11.2145 | 13.8115 |
| `abcijk-ijma-mkbc` | 11.0345 | 10.9101 | 11.2237 | 13.3174 |
| `abcijk-ijmb-mkac` | 10.6416 | 10.6553 | 10.8935 | 13.7002 |
| `abcijk-ijmc-mkab` | 10.8183 | 10.7992 | 11.0625 | 11.8820 |
| `abcijk-ikma-mjbc` | 10.8799 | 10.9138 | 11.2761 | 13.4438 |
| `abcijk-ikmb-mjac` | 10.7166 | 10.7199 | 10.9289 | 12.8508 |
| `abcijk-ikmc-mjab` | 10.8178 | 10.8310 | 11.0641 | 12.8347 |
| `abcijk-jkma-mibc` | 10.9236 | 10.8889 | 11.1759 | 12.6469 |
| `abcijk-jkmb-miac` | 10.6602 | 10.6674 | 10.8708 | 14.9884 |
| `abcijk-jkmc-miab` | 10.9235 | 10.9381 | 11.1924 | 12.5014 |
| `abcs-rc-abrs` | 1.1734 | 1.1810 | 1.1846 | 1.5294 |
| `abj-bka-kj` | 3.9283 | 3.9173 | 3.9889 | 5.5827 |
| `abjc-cbka-kj` | 1.9607 | 1.8611 | 1.8406 | 1.9249 |
| `abjc-kbac-jk` | 1.2342 | 1.2513 | 1.2913 | 1.7827 |
| `abjcd-dkbac-jk` | 8.6751 | 8.6894 | 9.1534 | 12.1343 |
| `abrs-qb-aqrs` | 0.9871 | 0.9890 | 1.0339 | 1.7107 |
| `adbjc-cbdka-kj` | 20.2459 | 20.3751 | 20.7269 | 13.4368 |
| `ajb-kba-jk` | 3.6224 | 3.5267 | 3.6202 | 4.7325 |
| `ajbc-ckba-jk` | 1.4465 | 1.4265 | 1.4549 | 1.9029 |
| `ajbdc-ckbad-jk` | 8.5826 | 8.5560 | 8.7881 | 11.9762 |
| `aqrs-pa-pqrs` | 1.2587 | 1.2607 | 1.3100 | 1.4333 |
| `ij-ik-kj` | 12.2933 | 12.2906 | 12.4246 | 10.3944 |
| `ij-ikl-ljk` | 3.0429 | 3.0222 | 3.0792 | 3.6739 |
| `ij-kil-lkj` | 4.7864 | 4.7900 | 4.8658 | 5.3461 |
| `ijk-ikl-lj` | 2.6239 | 2.6301 | 2.5705 | 3.6970 |
| `ijk-il-jlk` | 2.7394 | 2.7814 | 2.8199 | 2.9740 |
| `ijk-ilk-jl` | 2.4895 | 2.5301 | 2.5528 | 3.1234 |
| `ijk-ilk-lj` | 2.5970 | 2.6153 | 2.6312 | 3.4979 |
| `ijk-ilmk-mjl` | 0.9841 | 0.9835 | 1.0075 | 1.2348 |
| `ijkl-imjn-lnkm` | 15.2338 | 15.2368 | 15.5136 | 16.3564 |
| `ijkl-imjn-nlmk` | 15.2253 | 15.2366 | 15.4284 | 16.7931 |
| `ijkl-imkn-jnlm` | 15.2615 | 15.2332 | 15.4871 | 16.1689 |
| `ijkl-imkn-njml` | 15.2572 | 15.2128 | 15.4816 | 16.6561 |
| `ijkl-imln-jnkm` | 15.2007 | 15.1645 | 15.4281 | 16.1820 |
| `ijkl-imln-njmk` | 15.2419 | 15.2271 | 15.4907 | 16.4561 |
| `ijkl-imnj-nlkm` | 15.1232 | 15.1312 | 15.3287 | 16.3544 |
| `ijkl-imnk-njml` | 15.2346 | 15.2130 | 15.5011 | 16.4137 |
| `ijkl-minj-nlmk` | 18.8284 | 18.8385 | 19.1391 | 20.5483 |
| `ijkl-mink-jnlm` | 18.4424 | 18.3746 | 18.7786 | 19.7936 |
| `ijkl-minl-njmk` | 18.8864 | 18.8136 | 19.2514 | 20.0365 |
| **geomean** | 6.9463 | 6.9406 | 7.0758 | 8.2245 |

## 1 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.6391 | 0.6415 | 0.7570 | 0.9313 |
| `abcijk-eiab-jkec` | 2.8752 | 2.9211 | 3.0069 | 3.7366 |
| `abcijk-eiac-jkeb` | 2.7364 | 2.7270 | 2.8864 | 4.4619 |
| `abcijk-eibc-jkea` | 2.8829 | 3.3506 | 3.1446 | 3.3279 |
| `abcijk-ejab-ikec` | 2.7950 | 2.8655 | 2.9530 | 3.5979 |
| `abcijk-ejac-ikeb` | 2.6860 | 2.9025 | 2.8401 | 3.7230 |
| `abcijk-ejbc-ikea` | 2.8472 | 2.9004 | 3.0757 | 3.6601 |
| `abcijk-ekab-ijec` | 2.8389 | 2.8683 | 2.9547 | 3.3555 |
| `abcijk-ekac-ijeb` | 2.7418 | 2.7578 | 2.8701 | 4.1031 |
| `abcijk-ekbc-ijea` | 2.8876 | 3.4079 | 3.0908 | 3.6629 |
| `abcijk-ijma-mkbc` | 2.8207 | 2.9093 | 3.0344 | 3.6479 |
| `abcijk-ijmb-mkac` | 2.7126 | 2.7298 | 2.8774 | 4.2218 |
| `abcijk-ijmc-mkab` | 2.8019 | 2.8393 | 2.9491 | 3.3287 |
| `abcijk-ikma-mjbc` | 2.9018 | 3.1902 | 3.0633 | 3.6636 |
| `abcijk-ikmb-mjac` | 2.6926 | 2.7389 | 2.8853 | 3.7574 |
| `abcijk-ikmc-mjab` | 3.1527 | 2.8279 | 2.9102 | 3.5894 |
| `abcijk-jkma-mibc` | 2.8645 | 2.8947 | 3.0050 | 3.3687 |
| `abcijk-jkmb-miac` | 2.7291 | 3.2092 | 2.8764 | 4.5632 |
| `abcijk-jkmc-miab` | 3.3138 | 2.8798 | 3.0318 | 3.7110 |
| `abcs-rc-abrs` | 0.2916 | 0.2918 | 0.3607 | 0.4599 |
| `abj-bka-kj` | 1.0366 | 1.1397 | 1.2565 | 1.5710 |
| `abjc-cbka-kj` | 0.5102 | 0.5148 | 0.6162 | 0.6189 |
| `abjc-kbac-jk` | 0.3175 | 0.3146 | 0.3919 | 0.5231 |
| `abjcd-dkbac-jk` | 3.1101 | 3.1637 | 3.2936 | 4.0278 |
| `abrs-qb-aqrs` | 0.2839 | 0.2580 | 0.3248 | 0.4658 |
| `adbjc-cbdka-kj` | 6.9412 | 6.8806 | 7.2062 | 5.7757 |
| `ajb-kba-jk` | 0.9029 | 0.9070 | 0.9880 | 1.3388 |
| `ajbc-ckba-jk` | 0.3779 | 0.3765 | 0.4594 | 0.6052 |
| `ajbdc-ckbad-jk` | 3.1058 | 3.0690 | 3.2597 | 3.9508 |
| `aqrs-pa-pqrs` | 0.3798 | 0.3728 | 0.4291 | 0.4040 |
| `ij-ik-kj` | 3.1464 | 3.1397 | 3.2650 | 3.4154 |
| `ij-ikl-ljk` | 1.7557 | 1.7546 | 1.8814 | 1.4439 |
| `ij-kil-lkj` | 2.7068 | 2.6998 | 2.7418 | 2.1026 |
| `ijk-ikl-lj` | 0.9283 | 0.9275 | 0.9902 | 1.2522 |
| `ijk-il-jlk` | 1.4757 | 1.4563 | 1.4816 | 0.8890 |
| `ijk-ilk-jl` | 0.6788 | 0.6571 | 0.7104 | 0.7976 |
| `ijk-ilk-lj` | 0.6692 | 0.6671 | 0.7293 | 0.8871 |
| `ijk-ilmk-mjl` | 0.3033 | 0.2922 | 0.3340 | 0.3272 |
| `ijkl-imjn-lnkm` | 4.2459 | 4.2688 | 4.3608 | 4.3093 |
| `ijkl-imjn-nlmk` | 4.1899 | 4.1866 | 4.2737 | 4.4646 |
| `ijkl-imkn-jnlm` | 4.3223 | 4.2026 | 4.3117 | 4.3674 |
| `ijkl-imkn-njml` | 4.1819 | 4.1838 | 4.2606 | 4.5008 |
| `ijkl-imln-jnkm` | 4.2069 | 4.1684 | 4.2937 | 4.3736 |
| `ijkl-imln-njmk` | 4.3023 | 4.1753 | 4.2602 | 4.3924 |
| `ijkl-imnj-nlkm` | 4.2122 | 4.1838 | 4.2668 | 4.2759 |
| `ijkl-imnk-njml` | 4.1538 | 4.1467 | 4.2463 | 4.3141 |
| `ijkl-minj-nlmk` | 5.2808 | 5.1742 | 5.3144 | 5.3807 |
| `ijkl-mink-jnlm` | 5.7544 | 5.1553 | 5.1822 | 5.3160 |
| `ijkl-minl-njmk` | 7.0622 | 5.1249 | 5.2833 | 5.3160 |
| **geomean** | 2.0095 | 2.0062 | 2.1172 | 2.3874 |

## 1 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 0.3329 | 0.3329 | 0.6001 | 0.4006 |
| `abcijk-eiab-jkec` | 1.6884 | 1.7925 | 1.9202 | 2.2258 |
| `abcijk-eiac-jkeb` | 1.5981 | 1.6746 | 1.8906 | 2.8259 |
| `abcijk-eibc-jkea` | 1.7079 | 1.7638 | 3.0143 | 2.0574 |
| `abcijk-ejab-ikec` | 1.6700 | 1.6927 | 1.8796 | 2.4922 |
| `abcijk-ejac-ikeb` | 1.6007 | 1.5425 | 1.9598 | 2.4482 |
| `abcijk-ejbc-ikea` | 1.6738 | 1.6245 | 3.0511 | 2.1937 |
| `abcijk-ekab-ijec` | 1.6795 | 1.6772 | 1.8543 | 2.1643 |
| `abcijk-ekac-ijeb` | 1.5869 | 1.5767 | 1.8972 | 2.7061 |
| `abcijk-ekbc-ijea` | 1.6054 | 1.6133 | 3.0399 | 2.2014 |
| `abcijk-ijma-mkbc` | 1.5946 | 1.6958 | 2.9286 | 2.1913 |
| `abcijk-ijmb-mkac` | 1.6154 | 1.6448 | 1.8986 | 2.6999 |
| `abcijk-ijmc-mkab` | 1.6672 | 1.8088 | 1.8555 | 2.1532 |
| `abcijk-ikma-mjbc` | 1.6595 | 1.7550 | 2.8293 | 2.1824 |
| `abcijk-ikmb-mjac` | 1.5654 | 1.6398 | 1.9186 | 2.4285 |
| `abcijk-ikmc-mjab` | 1.6470 | 1.7800 | 1.8566 | 2.5331 |
| `abcijk-jkma-mibc` | 1.6618 | 1.7115 | 2.8337 | 2.0704 |
| `abcijk-jkmb-miac` | 1.6090 | 1.6949 | 1.9089 | 2.8392 |
| `abcijk-jkmc-miab` | 1.6736 | 1.7741 | 1.8580 | 2.2996 |
| `abcs-rc-abrs` | 0.1593 | 0.1550 | 0.2981 | 0.2605 |
| `abj-bka-kj` | 0.5179 | 0.5190 | 0.6470 | 0.8345 |
| `abjc-cbka-kj` | 0.2834 | 0.2723 | 0.4147 | 0.3535 |
| `abjc-kbac-jk` | 0.1712 | 0.1674 | 0.2844 | 0.2770 |
| `abjcd-dkbac-jk` | 2.2409 | 2.2500 | 2.4264 | 2.9771 |
| `abrs-qb-aqrs` | 0.1396 | 0.1371 | 0.2415 | 0.2595 |
| `adbjc-cbdka-kj` | 4.0959 | 4.1232 | 4.3112 | 4.4797 |
| `ajb-kba-jk` | 0.4587 | 0.4478 | 0.5691 | 0.5766 |
| `ajbc-ckba-jk` | 0.2185 | 0.1943 | 0.8533 | 0.3592 |
| `ajbdc-ckbad-jk` | 2.1995 | 2.2122 | 4.2485 | 2.8083 |
| `aqrs-pa-pqrs` | 0.2156 | 0.2227 | 0.2983 | 0.2422 |
| `ij-ik-kj` | 1.5994 | 1.5982 | 1.9243 | 1.8232 |
| `ij-ikl-ljk` | 0.9741 | 0.9732 | 1.1492 | 0.9774 |
| `ij-kil-lkj` | 1.5118 | 1.4962 | 1.6700 | 1.4114 |
| `ijk-ikl-lj` | 0.4831 | 0.4759 | 0.5913 | 0.6179 |
| `ijk-il-jlk` | 0.5150 | 0.5048 | 0.6101 | 0.5542 |
| `ijk-ilk-jl` | 0.4718 | 0.4632 | 0.8411 | 0.5533 |
| `ijk-ilk-lj` | 0.4969 | 0.4800 | 0.5983 | 0.5913 |
| `ijk-ilmk-mjl` | 0.2300 | 0.2183 | 0.3380 | 0.2668 |
| `ijkl-imjn-lnkm` | 3.0403 | 3.0257 | 3.2036 | 2.9856 |
| `ijkl-imjn-nlmk` | 2.2064 | 2.1737 | 2.3265 | 2.4487 |
| `ijkl-imkn-jnlm` | 2.1694 | 2.1471 | 2.3519 | 2.4745 |
| `ijkl-imkn-njml` | 2.1363 | 2.1385 | 2.2981 | 2.3637 |
| `ijkl-imln-jnkm` | 2.2002 | 2.1558 | 2.3309 | 2.4796 |
| `ijkl-imln-njmk` | 2.1714 | 2.1291 | 2.2802 | 2.3267 |
| `ijkl-imnj-nlkm` | 2.1459 | 2.1506 | 2.3002 | 2.3541 |
| `ijkl-imnk-njml` | 2.1373 | 2.1301 | 2.2700 | 2.3229 |
| `ijkl-minj-nlmk` | 2.6700 | 2.6898 | 2.8149 | 2.9335 |
| `ijkl-mink-jnlm` | 2.5776 | 2.5684 | 2.7813 | 2.9828 |
| `ijkl-minl-njmk` | 2.6204 | 2.6423 | 2.8021 | 2.8634 |
| **geomean** | 1.1172 | 1.1207 | 1.4708 | 1.4385 |

## 16 MiB, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 14.9293 | 14.9138 | 15.3739 | 18.8001 |
| `abcijk-eiab-jkec` | 14.7723 | 14.7781 | 15.5942 | 25.8901 |
| `abcijk-eiac-jkeb` | 13.9463 | 13.8945 | 15.8382 | 35.4592 |
| `abcijk-eibc-jkea` | 13.6702 | 13.6308 | 15.4542 | 17.3084 |
| `abcijk-ejab-ikec` | 14.7976 | 14.7956 | 15.5300 | 21.7746 |
| `abcijk-ejac-ikeb` | 13.9464 | 14.0197 | 15.8158 | 19.3076 |
| `abcijk-ejbc-ikea` | 13.7789 | 13.7951 | 15.3173 | 17.2900 |
| `abcijk-ekab-ijec` | 14.7646 | 14.7574 | 15.5844 | 18.0154 |
| `abcijk-ekac-ijeb` | 13.8999 | 13.8742 | 15.7604 | 23.7049 |
| `abcijk-ekbc-ijea` | 13.6899 | 13.7311 | 15.3678 | 17.2965 |
| `abcijk-ijma-mkbc` | 13.6820 | 13.7071 | 15.2846 | 17.1363 |
| `abcijk-ijmb-mkac` | 13.8383 | 13.8748 | 15.8778 | 23.6836 |
| `abcijk-ijmc-mkab` | 14.8217 | 14.8005 | 15.5326 | 18.2831 |
| `abcijk-ikma-mjbc` | 13.7495 | 13.7413 | 15.5014 | 17.3297 |
| `abcijk-ikmb-mjac` | 13.9648 | 13.9416 | 15.8374 | 19.3277 |
| `abcijk-ikmc-mjab` | 14.7767 | 14.7749 | 15.5268 | 22.0408 |
| `abcijk-jkma-mibc` | 13.6757 | 13.6578 | 15.4696 | 17.2137 |
| `abcijk-jkmb-miac` | 13.9116 | 13.9199 | 15.7419 | 35.2313 |
| `abcijk-jkmc-miab` | 14.7548 | 14.7575 | 15.5653 | 26.2968 |
| `abcs-rc-abrs` | 9.4478 | 9.3498 | 9.7170 | 14.9877 |
| `abj-bka-kj` | 20.0154 | 19.8503 | 20.1291 | 29.3857 |
| `abjc-cbka-kj` | 35.8022 | 35.8087 | 36.8308 | 25.5616 |
| `abjc-kbac-jk` | 13.0615 | 13.2796 | 13.1170 | 19.2739 |
| `abjcd-dkbac-jk` | 17.3003 | 17.1829 | 19.6732 | 21.9712 |
| `abrs-qb-aqrs` | 8.4906 | 8.3506 | 8.4615 | 15.8003 |
| `adbjc-cbdka-kj` | 42.7601 | 42.7670 | 44.6591 | 29.3205 |
| `ajb-kba-jk` | 18.0806 | 18.5053 | 19.0795 | 20.5011 |
| `ajbc-ckba-jk` | 19.4576 | 19.4562 | 21.2421 | 17.7220 |
| `ajbdc-ckbad-jk` | 17.2427 | 17.2757 | 19.8844 | 20.8026 |
| `aqrs-pa-pqrs` | 7.5167 | 9.1427 | 10.7967 | 15.2511 |
| `ij-ik-kj` | 169.5535 | 129.8194 | 131.3144 | 136.0510 |
| `ij-ikl-ljk` | 17.7143 | 17.6042 | 18.4221 | 24.6042 |
| `ij-kil-lkj` | 21.4845 | 21.5438 | 23.0263 | 30.0656 |
| `ijk-ikl-lj` | 16.0379 | 16.2058 | 16.1806 | 19.7798 |
| `ijk-il-jlk` | 15.8228 | 15.8176 | 19.0058 | 18.4421 |
| `ijk-ilk-jl` | 14.8279 | 14.8139 | 15.4694 | 18.5404 |
| `ijk-ilk-lj` | 14.8876 | 14.9272 | 15.5042 | 19.7406 |
| `ijk-ilmk-mjl` | 7.2203 | 7.1591 | 7.5099 | 13.3465 |
| `ijkl-imjn-lnkm` | 255.2479 | 255.2303 | 254.5608 | 252.8857 |
| `ijkl-imjn-nlmk` | 255.0240 | 254.9772 | 256.1825 | 261.5030 |
| `ijkl-imkn-jnlm` | 251.5312 | 251.4976 | 259.2793 | 250.6135 |
| `ijkl-imkn-njml` | 252.2563 | 252.5495 | 260.2785 | 258.0449 |
| `ijkl-imln-jnkm` | 250.4370 | 249.9494 | 258.7640 | 253.7315 |
| `ijkl-imln-njmk` | 250.3329 | 250.9163 | 259.4240 | 256.3656 |
| `ijkl-imnj-nlkm` | 254.2820 | 254.5350 | 255.2294 | 257.9424 |
| `ijkl-imnk-njml` | 251.3912 | 251.2105 | 258.8816 | 256.8509 |
| `ijkl-minj-nlmk` | 309.4700 | 309.5119 | 312.3626 | 314.5101 |
| `ijkl-mink-jnlm` | 304.6301 | 304.9038 | 314.2920 | 306.7726 |
| `ijkl-minl-njmk` | 303.6311 | 305.3717 | 314.5266 | 314.1101 |
| **geomean** | 29.9893 | 29.9504 | 31.9403 | 38.2574 |

## 16 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 4.1022 | 4.0522 | 4.1514 | 5.5924 |
| `abcijk-eiab-jkec` | 5.1916 | 5.1901 | 4.8519 | 9.3677 |
| `abcijk-eiac-jkeb` | 4.6587 | 4.5933 | 5.0219 | 11.9383 |
| `abcijk-eibc-jkea` | 4.2736 | 4.2845 | 4.8202 | 5.1190 |
| `abcijk-ejab-ikec` | 5.0074 | 4.9436 | 4.8593 | 7.3170 |
| `abcijk-ejac-ikeb` | 4.6171 | 4.6342 | 4.9777 | 6.3824 |
| `abcijk-ejbc-ikea` | 4.4460 | 4.3529 | 4.8111 | 5.2164 |
| `abcijk-ekab-ijec` | 5.0265 | 4.9669 | 4.8719 | 6.7859 |
| `abcijk-ekac-ijeb` | 4.6380 | 4.6129 | 4.9400 | 8.8460 |
| `abcijk-ekbc-ijea` | 4.4551 | 4.3928 | 4.8358 | 5.2426 |
| `abcijk-ijma-mkbc` | 4.3564 | 4.3076 | 4.8107 | 5.2001 |
| `abcijk-ijmb-mkac` | 4.7443 | 4.6170 | 4.9533 | 8.5604 |
| `abcijk-ijmc-mkab` | 4.9060 | 4.9416 | 5.0234 | 6.8132 |
| `abcijk-ikma-mjbc` | 4.3278 | 4.4351 | 4.8059 | 5.2415 |
| `abcijk-ikmb-mjac` | 4.7007 | 4.6093 | 5.0442 | 6.3904 |
| `abcijk-ikmc-mjab` | 5.0730 | 4.9147 | 4.8613 | 7.0963 |
| `abcijk-jkma-mibc` | 4.2483 | 4.2295 | 4.7039 | 5.1580 |
| `abcijk-jkmb-miac` | 4.6176 | 4.6305 | 5.0765 | 11.8645 |
| `abcijk-jkmc-miab` | 5.1412 | 5.1787 | 4.8718 | 9.4346 |
| `abcs-rc-abrs` | 2.8197 | 2.7395 | 2.7387 | 5.1407 |
| `abj-bka-kj` | 5.6080 | 5.5189 | 6.0115 | 9.3130 |
| `abjc-cbka-kj` | 12.5619 | 12.5646 | 13.4655 | 8.9791 |
| `abjc-kbac-jk` | 3.5298 | 3.8905 | 3.5503 | 6.9306 |
| `abjcd-dkbac-jk` | 7.1234 | 7.1396 | 7.4948 | 7.3716 |
| `abrs-qb-aqrs` | 2.3712 | 2.3963 | 2.3686 | 4.6034 |
| `adbjc-cbdka-kj` | 13.7603 | 13.8664 | 14.1184 | 12.0806 |
| `ajb-kba-jk` | 4.8238 | 4.7765 | 4.9346 | 6.0694 |
| `ajbc-ckba-jk` | 7.5633 | 7.6185 | 8.1045 | 5.3931 |
| `ajbdc-ckbad-jk` | 6.9590 | 6.9348 | 7.5524 | 6.7987 |
| `aqrs-pa-pqrs` | 2.4908 | 2.8027 | 3.2940 | 4.7432 |
| `ij-ik-kj` | 43.1226 | 47.9142 | 44.8507 | 35.6905 |
| `ij-ikl-ljk` | 6.5545 | 6.3240 | 6.9794 | 7.6488 |
| `ij-kil-lkj` | 7.8456 | 7.6574 | 8.1838 | 9.4970 |
| `ijk-ikl-lj` | 4.2431 | 4.7048 | 4.5243 | 6.3346 |
| `ijk-il-jlk` | 5.4447 | 5.4728 | 6.2367 | 4.7863 |
| `ijk-ilk-jl` | 4.1131 | 4.0082 | 4.1615 | 5.4061 |
| `ijk-ilk-lj` | 4.1143 | 4.0477 | 4.2031 | 5.7979 |
| `ijk-ilmk-mjl` | 2.1659 | 2.1132 | 2.4726 | 3.5546 |
| `ijkl-imjn-lnkm` | 66.5094 | 66.8468 | 67.8388 | 66.2221 |
| `ijkl-imjn-nlmk` | 66.3251 | 66.3321 | 66.6104 | 68.4357 |
| `ijkl-imkn-jnlm` | 65.0371 | 65.0440 | 67.8432 | 66.2581 |
| `ijkl-imkn-njml` | 65.5956 | 65.7192 | 68.5071 | 68.9237 |
| `ijkl-imln-jnkm` | 64.6072 | 64.6355 | 67.3870 | 66.7139 |
| `ijkl-imln-njmk` | 65.2311 | 64.6230 | 68.1468 | 68.3147 |
| `ijkl-imnj-nlkm` | 66.3601 | 66.2200 | 66.9445 | 67.6718 |
| `ijkl-imnk-njml` | 65.4696 | 65.4900 | 68.3646 | 67.4229 |
| `ijkl-minj-nlmk` | 80.1731 | 80.0451 | 80.4799 | 83.6545 |
| `ijkl-mink-jnlm` | 78.3546 | 78.3955 | 81.8074 | 80.5579 |
| `ijkl-minl-njmk` | 77.6316 | 77.8424 | 80.6478 | 82.5372 |
| **geomean** | 9.1852 | 9.2099 | 9.6277 | 11.7551 |

## 16 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 2.2169 | 2.1659 | 2.2976 | 3.2850 |
| `abcijk-eiab-jkec` | 3.8907 | 3.9814 | 3.7727 | 6.6172 |
| `abcijk-eiac-jkeb` | 3.5745 | 3.6334 | 3.8618 | 7.3231 |
| `abcijk-eibc-jkea` | 3.7960 | 3.7688 | 3.8250 | 3.8539 |
| `abcijk-ejab-ikec` | 3.8275 | 3.9231 | 3.7963 | 5.4622 |
| `abcijk-ejac-ikeb` | 3.6462 | 3.5966 | 3.9050 | 4.7681 |
| `abcijk-ejbc-ikea` | 3.7892 | 3.7779 | 3.8537 | 3.8983 |
| `abcijk-ekab-ijec` | 3.9114 | 3.9674 | 3.7799 | 5.4510 |
| `abcijk-ekac-ijeb` | 3.5939 | 3.6189 | 3.8510 | 6.6166 |
| `abcijk-ekbc-ijea` | 3.6754 | 3.7169 | 3.8394 | 3.9042 |
| `abcijk-ijma-mkbc` | 3.7239 | 3.7407 | 3.7623 | 3.8653 |
| `abcijk-ijmb-mkac` | 3.6397 | 3.6216 | 3.8159 | 6.5228 |
| `abcijk-ijmc-mkab` | 3.9489 | 3.9461 | 3.7689 | 5.3746 |
| `abcijk-ikma-mjbc` | 3.8126 | 3.7446 | 3.7966 | 3.9271 |
| `abcijk-ikmb-mjac` | 3.6529 | 3.6148 | 3.9390 | 4.7604 |
| `abcijk-ikmc-mjab` | 3.8546 | 3.9563 | 3.7600 | 5.3676 |
| `abcijk-jkma-mibc` | 3.7077 | 3.7029 | 3.8063 | 3.7464 |
| `abcijk-jkmb-miac` | 3.5740 | 3.6119 | 3.8038 | 7.3774 |
| `abcijk-jkmc-miab` | 3.8725 | 3.9879 | 3.7841 | 6.6609 |
| `abcs-rc-abrs` | 1.9794 | 2.0098 | 2.1461 | 4.1806 |
| `abj-bka-kj` | 4.1745 | 4.1936 | 4.5477 | 6.6162 |
| `abjc-cbka-kj` | 8.4203 | 8.6466 | 8.9869 | 6.5804 |
| `abjc-kbac-jk` | 2.4503 | 2.4038 | 2.5590 | 4.6647 |
| `abjcd-dkbac-jk` | 4.5467 | 4.5497 | 4.7863 | 5.1589 |
| `abrs-qb-aqrs` | 1.5218 | 1.4845 | 1.6357 | 2.7520 |
| `adbjc-cbdka-kj` | 8.7855 | 8.9839 | 9.6104 | 10.6382 |
| `ajb-kba-jk` | 2.7133 | 2.6975 | 2.8695 | 3.7159 |
| `ajbc-ckba-jk` | 5.1841 | 5.0948 | 5.4618 | 4.0163 |
| `ajbdc-ckbad-jk` | 4.4612 | 4.4419 | 4.7818 | 4.7392 |
| `aqrs-pa-pqrs` | 1.5169 | 1.7016 | 1.9611 | 2.6771 |
| `ij-ik-kj` | 21.9747 | 24.5251 | 25.1228 | 19.5192 |
| `ij-ikl-ljk` | 3.5132 | 3.2745 | 3.5655 | 5.1100 |
| `ij-kil-lkj` | 4.5208 | 4.4114 | 4.6676 | 6.5011 |
| `ijk-ikl-lj` | 2.4438 | 2.4128 | 2.6723 | 4.2251 |
| `ijk-il-jlk` | 2.2803 | 2.2836 | 2.7572 | 2.5528 |
| `ijk-ilk-jl` | 2.1885 | 2.1459 | 2.3057 | 3.3019 |
| `ijk-ilk-lj` | 2.1929 | 2.1855 | 2.2990 | 3.6162 |
| `ijk-ilmk-mjl` | 1.7273 | 1.4724 | 1.5625 | 1.9480 |
| `ijkl-imjn-lnkm` | 35.9045 | 35.9517 | 36.9690 | 36.2065 |
| `ijkl-imjn-nlmk` | 36.3842 | 36.4544 | 36.7953 | 35.8634 |
| `ijkl-imkn-jnlm` | 34.9620 | 34.7989 | 35.3621 | 36.5224 |
| `ijkl-imkn-njml` | 35.3333 | 35.2027 | 36.3028 | 35.9033 |
| `ijkl-imln-jnkm` | 34.6262 | 34.6126 | 35.4170 | 36.8347 |
| `ijkl-imln-njmk` | 35.2948 | 35.4943 | 36.1603 | 35.8856 |
| `ijkl-imnj-nlkm` | 36.5873 | 36.6814 | 37.2567 | 35.3613 |
| `ijkl-imnk-njml` | 34.6932 | 34.7297 | 36.2476 | 35.7521 |
| `ijkl-minj-nlmk` | 43.6671 | 43.6853 | 44.4167 | 44.3443 |
| `ijkl-mink-jnlm` | 41.4433 | 41.1789 | 42.4475 | 43.6009 |
| `ijkl-minl-njmk` | 41.6616 | 41.8481 | 43.0411 | 44.1412 |
| **geomean** | 6.0060 | 6.0085 | 6.2577 | 7.6586 |

## 16 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 57.3099 | 57.3285 | 57.7914 | 69.8642 |
| `abcijk-eiab-jkec` | 54.3528 | 54.3666 | 56.3866 | 65.6952 |
| `abcijk-eiac-jkeb` | 53.5969 | 53.5578 | 54.6396 | 82.0080 |
| `abcijk-eibc-jkea` | 54.4232 | 54.4293 | 55.5759 | 61.4053 |
| `abcijk-ejab-ikec` | 54.1715 | 54.1773 | 55.5949 | 64.7652 |
| `abcijk-ejac-ikeb` | 53.4119 | 53.4870 | 54.6484 | 65.0731 |
| `abcijk-ejbc-ikea` | 54.3858 | 54.4063 | 55.6829 | 61.4382 |
| `abcijk-ekab-ijec` | 54.1287 | 54.0503 | 55.5336 | 58.5112 |
| `abcijk-ekac-ijeb` | 53.5045 | 53.5845 | 54.5913 | 69.1334 |
| `abcijk-ekbc-ijea` | 54.4502 | 54.3856 | 55.7932 | 61.7096 |
| `abcijk-ijma-mkbc` | 54.3460 | 54.3874 | 55.5731 | 61.5140 |
| `abcijk-ijmb-mkac` | 53.4710 | 53.3931 | 54.7120 | 68.9435 |
| `abcijk-ijmc-mkab` | 54.0687 | 54.0736 | 55.5119 | 58.4861 |
| `abcijk-ikma-mjbc` | 54.4275 | 54.4650 | 55.6388 | 60.9700 |
| `abcijk-ikmb-mjac` | 53.5231 | 53.5394 | 54.6694 | 66.0956 |
| `abcijk-ikmc-mjab` | 54.1440 | 54.1172 | 55.7553 | 64.9099 |
| `abcijk-jkma-mibc` | 54.3885 | 54.3804 | 55.6524 | 61.3779 |
| `abcijk-jkmb-miac` | 53.6181 | 53.6157 | 54.5958 | 82.0333 |
| `abcijk-jkmc-miab` | 54.4255 | 54.4093 | 56.4562 | 65.6372 |
| `abcs-rc-abrs` | 31.7310 | 31.7417 | 31.2364 | 40.6628 |
| `abj-bka-kj` | 72.7502 | 72.9640 | 73.9390 | 98.6212 |
| `abjc-cbka-kj` | 66.4845 | 66.4206 | 67.5651 | 63.3750 |
| `abjc-kbac-jk` | 39.5603 | 39.2333 | 39.9500 | 53.5563 |
| `abjcd-dkbac-jk` | 43.1008 | 43.1746 | 44.8126 | 46.0454 |
| `abrs-qb-aqrs` | 33.3141 | 33.3104 | 33.2158 | 40.5220 |
| `adbjc-cbdka-kj` | 72.1478 | 72.0573 | 73.0476 | 49.5027 |
| `ajb-kba-jk` | 64.4013 | 64.3343 | 64.7098 | 75.7854 |
| `ajbc-ckba-jk` | 49.0268 | 48.9946 | 50.4033 | 43.1970 |
| `ajbdc-ckbad-jk` | 42.7093 | 42.7141 | 44.1658 | 44.8135 |
| `aqrs-pa-pqrs` | 31.1143 | 31.1188 | 32.9466 | 40.2514 |
| `ij-ik-kj` | 506.6645 | 506.4135 | 517.4028 | 528.0653 |
| `ij-ikl-ljk` | 64.8624 | 64.9119 | 66.9635 | 79.1438 |
| `ij-kil-lkj` | 75.9590 | 75.9843 | 79.0098 | 99.1135 |
| `ijk-ikl-lj` | 59.5228 | 59.4481 | 59.8343 | 75.2476 |
| `ijk-il-jlk` | 57.5713 | 57.6925 | 58.4655 | 63.3932 |
| `ijk-ilk-jl` | 57.3134 | 57.1727 | 57.2277 | 69.9801 |
| `ijk-ilk-lj` | 59.0012 | 58.9799 | 59.5823 | 71.6383 |
| `ijk-ilmk-mjl` | 30.7468 | 30.6671 | 30.3230 | 41.3230 |
| `ijkl-imjn-lnkm` | 970.6077 | 971.0805 | 993.6391 | 1035.9546 |
| `ijkl-imjn-nlmk` | 977.0505 | 974.6498 | 996.3402 | 1040.3543 |
| `ijkl-imkn-jnlm` | 977.9029 | 978.6124 | 988.6040 | 1030.7171 |
| `ijkl-imkn-njml` | 981.2335 | 981.2411 | 990.9109 | 1048.2650 |
| `ijkl-imln-jnkm` | 976.4034 | 975.4442 | 985.4045 | 1039.8566 |
| `ijkl-imln-njmk` | 979.4136 | 979.5576 | 988.2968 | 1030.7800 |
| `ijkl-imnj-nlkm` | 976.4399 | 976.2404 | 996.2891 | 1030.1365 |
| `ijkl-imnk-njml` | 980.3978 | 979.6628 | 991.1838 | 1043.1038 |
| `ijkl-minj-nlmk` | 1180.1893 | 1180.1891 | 1203.6360 | 1253.7006 |
| `ijkl-mink-jnlm` | 1177.4892 | 1177.0802 | 1191.3190 | 1251.2995 |
| `ijkl-minl-njmk` | 1181.9910 | 1181.7273 | 1194.6672 | 1244.1341 |
| **geomean** | 107.0744 | 107.0426 | 109.0813 | 123.0050 |

## 16 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 14.5834 | 14.6409 | 14.7565 | 18.5720 |
| `abcijk-eiab-jkec` | 14.1727 | 14.1648 | 14.7938 | 23.0087 |
| `abcijk-eiac-jkeb` | 13.5976 | 13.5554 | 14.0763 | 27.1517 |
| `abcijk-eibc-jkea` | 13.8944 | 13.8438 | 14.1685 | 16.0421 |
| `abcijk-ejab-ikec` | 13.9454 | 13.9681 | 14.3628 | 18.3964 |
| `abcijk-ejac-ikeb` | 13.4990 | 13.4396 | 14.0210 | 17.7408 |
| `abcijk-ejbc-ikea` | 13.9457 | 13.9356 | 14.2187 | 16.1068 |
| `abcijk-ekab-ijec` | 13.9650 | 13.9600 | 14.2989 | 16.5121 |
| `abcijk-ekac-ijeb` | 13.4582 | 13.6834 | 13.9807 | 21.3020 |
| `abcijk-ekbc-ijea` | 13.9267 | 13.9163 | 14.2337 | 16.0877 |
| `abcijk-ijma-mkbc` | 13.8996 | 13.9169 | 14.2685 | 16.1039 |
| `abcijk-ijmb-mkac` | 13.5415 | 13.6745 | 14.0264 | 21.2633 |
| `abcijk-ijmc-mkab` | 13.9318 | 13.8804 | 14.2641 | 16.2946 |
| `abcijk-ikma-mjbc` | 13.9428 | 13.8969 | 14.2073 | 16.1447 |
| `abcijk-ikmb-mjac` | 13.6414 | 13.6170 | 14.5933 | 17.7689 |
| `abcijk-ikmc-mjab` | 13.9451 | 13.9434 | 14.2664 | 18.3811 |
| `abcijk-jkma-mibc` | 13.8661 | 13.8875 | 14.2582 | 16.0537 |
| `abcijk-jkmb-miac` | 13.5921 | 13.7388 | 13.9889 | 26.6616 |
| `abcijk-jkmc-miab` | 14.1336 | 14.1376 | 14.8020 | 22.9413 |
| `abcs-rc-abrs` | 8.3046 | 8.2552 | 8.0606 | 12.3522 |
| `abj-bka-kj` | 19.0817 | 19.0241 | 19.4099 | 26.7095 |
| `abjc-cbka-kj` | 20.1933 | 20.1504 | 20.5013 | 20.1217 |
| `abjc-kbac-jk` | 9.8328 | 10.5134 | 10.6590 | 18.2628 |
| `abjcd-dkbac-jk` | 13.3795 | 13.3289 | 13.8617 | 14.1675 |
| `abrs-qb-aqrs` | 8.5124 | 8.5441 | 8.4976 | 11.7181 |
| `adbjc-cbdka-kj` | 20.9958 | 21.4030 | 21.7712 | 18.4705 |
| `ajb-kba-jk` | 16.3873 | 16.4087 | 16.6110 | 20.0680 |
| `ajbc-ckba-jk` | 13.2335 | 13.1100 | 13.7358 | 13.3751 |
| `ajbdc-ckbad-jk` | 12.7981 | 12.9043 | 13.3129 | 13.0446 |
| `aqrs-pa-pqrs` | 8.1725 | 8.1731 | 8.5551 | 10.4607 |
| `ij-ik-kj` | 128.5984 | 128.6075 | 131.8229 | 135.3094 |
| `ij-ikl-ljk` | 22.7349 | 22.9866 | 23.4734 | 23.1218 |
| `ij-kil-lkj` | 26.5192 | 26.5822 | 27.2178 | 28.0297 |
| `ijk-ikl-lj` | 15.2603 | 15.2413 | 15.2924 | 19.8423 |
| `ijk-il-jlk` | 19.7067 | 19.7270 | 20.0229 | 16.1271 |
| `ijk-ilk-jl` | 14.5568 | 14.5945 | 14.7454 | 18.4311 |
| `ijk-ilk-lj` | 15.0619 | 15.1401 | 15.2008 | 18.8871 |
| `ijk-ilmk-mjl` | 8.3857 | 8.1065 | 8.3898 | 10.9681 |
| `ijkl-imjn-lnkm` | 248.9256 | 249.2044 | 255.5987 | 260.9684 |
| `ijkl-imjn-nlmk` | 248.2737 | 248.3930 | 254.3137 | 262.9711 |
| `ijkl-imkn-jnlm` | 247.6600 | 247.7380 | 251.5161 | 264.1470 |
| `ijkl-imkn-njml` | 248.8825 | 248.9770 | 252.4850 | 262.6610 |
| `ijkl-imln-jnkm` | 246.9459 | 247.1676 | 250.9259 | 264.3515 |
| `ijkl-imln-njmk` | 248.0855 | 248.3892 | 251.7394 | 263.0519 |
| `ijkl-imnj-nlkm` | 248.1916 | 248.1420 | 254.2457 | 262.8014 |
| `ijkl-imnk-njml` | 248.8949 | 248.9639 | 252.5975 | 262.9658 |
| `ijkl-minj-nlmk` | 299.7645 | 299.6976 | 305.7349 | 317.3695 |
| `ijkl-mink-jnlm` | 298.0561 | 298.3291 | 302.3755 | 316.9124 |
| `ijkl-minl-njmk` | 299.3550 | 299.2453 | 302.8042 | 314.8752 |
| **geomean** | 28.3124 | 28.3647 | 29.0046 | 34.2980 |

## 16 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) | tblis (ms) |
|---|---|---|---|---|
| `abc-bk-akc` | 7.5627 | 7.8676 | 7.9686 | 10.5282 |
| `abcijk-eiab-jkec` | 8.9150 | 8.8540 | 9.1038 | 14.4935 |
| `abcijk-eiac-jkeb` | 8.2710 | 8.2923 | 8.8102 | 16.8221 |
| `abcijk-eibc-jkea` | 8.3101 | 8.4024 | 10.2394 | 9.7898 |
| `abcijk-ejab-ikec` | 8.6112 | 8.3993 | 8.7830 | 11.6929 |
| `abcijk-ejac-ikeb` | 8.2369 | 8.3044 | 9.0777 | 11.0968 |
| `abcijk-ejbc-ikea` | 8.2790 | 8.3415 | 10.2546 | 9.8212 |
| `abcijk-ekab-ijec` | 8.8800 | 8.6605 | 8.9131 | 10.3943 |
| `abcijk-ekac-ijeb` | 8.2959 | 8.2556 | 8.7287 | 13.5981 |
| `abcijk-ekbc-ijea` | 8.4060 | 8.3257 | 10.2458 | 9.8218 |
| `abcijk-ijma-mkbc` | 8.3296 | 8.3383 | 10.2629 | 9.8493 |
| `abcijk-ijmb-mkac` | 8.3160 | 8.3144 | 9.2012 | 13.3422 |
| `abcijk-ijmc-mkab` | 8.9899 | 8.4049 | 8.5389 | 10.3761 |
| `abcijk-ikma-mjbc` | 8.3405 | 8.4210 | 10.3024 | 9.7937 |
| `abcijk-ikmb-mjac` | 8.2819 | 8.2325 | 8.4965 | 11.0981 |
| `abcijk-ikmc-mjab` | 8.9667 | 8.4688 | 8.1732 | 11.7020 |
| `abcijk-jkma-mibc` | 8.2751 | 8.4073 | 10.2383 | 9.7450 |
| `abcijk-jkmb-miac` | 8.3120 | 8.3125 | 9.2589 | 16.7586 |
| `abcijk-jkmc-miab` | 8.9477 | 8.7131 | 8.9817 | 14.1489 |
| `abcs-rc-abrs` | 4.5698 | 4.6280 | 4.6514 | 9.1541 |
| `abj-bka-kj` | 10.6534 | 10.5338 | 10.9041 | 15.7837 |
| `abjc-cbka-kj` | 12.7913 | 12.4741 | 12.7175 | 13.0441 |
| `abjc-kbac-jk` | 5.9859 | 6.0926 | 8.1436 | 10.5893 |
| `abjcd-dkbac-jk` | 8.7458 | 8.6425 | 8.8973 | 10.7994 |
| `abrs-qb-aqrs` | 4.8917 | 4.5716 | 4.5837 | 8.3384 |
| `adbjc-cbdka-kj` | 13.0077 | 12.4171 | 13.1616 | 14.2597 |
| `ajb-kba-jk` | 9.2079 | 8.5808 | 8.7260 | 11.3849 |
| `ajbc-ckba-jk` | 9.0045 | 9.0041 | 35.6752 | 9.8114 |
| `ajbdc-ckbad-jk` | 8.3533 | 8.3550 | 27.3898 | 9.7860 |
| `aqrs-pa-pqrs` | 4.4416 | 4.4545 | 4.7544 | 5.9342 |
| `ij-ik-kj` | 71.1983 | 70.7914 | 73.7051 | 69.6445 |
| `ij-ikl-ljk` | 16.4045 | 16.3463 | 16.6953 | 14.1619 |
| `ij-kil-lkj` | 18.8281 | 18.8469 | 19.3831 | 17.6348 |
| `ijk-ikl-lj` | 7.8788 | 8.4606 | 7.9096 | 11.7043 |
| `ijk-il-jlk` | 13.6785 | 13.6026 | 13.8397 | 8.2801 |
| `ijk-ilk-jl` | 8.0450 | 7.8895 | 7.9751 | 10.5412 |
| `ijk-ilk-lj` | 7.7186 | 7.7348 | 7.9076 | 10.8680 |
| `ijk-ilmk-mjl` | 5.0622 | 4.4893 | 5.0330 | 5.8615 |
| `ijkl-imjn-lnkm` | 132.2168 | 133.0919 | 137.6214 | 133.8320 |
| `ijkl-imjn-nlmk` | 131.8065 | 131.6730 | 136.2107 | 134.4188 |
| `ijkl-imkn-jnlm` | 131.9519 | 130.6664 | 133.5596 | 136.4194 |
| `ijkl-imkn-njml` | 132.7906 | 133.7336 | 135.8207 | 134.7857 |
| `ijkl-imln-jnkm` | 131.0406 | 130.6194 | 135.0536 | 136.4095 |
| `ijkl-imln-njmk` | 130.7068 | 130.5651 | 132.8850 | 134.4012 |
| `ijkl-imnj-nlkm` | 130.7232 | 130.7808 | 134.8636 | 134.0484 |
| `ijkl-imnk-njml` | 130.4512 | 130.5872 | 133.5846 | 134.5783 |
| `ijkl-minj-nlmk` | 157.4560 | 157.3246 | 161.8278 | 162.5901 |
| `ijkl-mink-jnlm` | 154.2120 | 154.3736 | 157.6118 | 162.7811 |
| `ijkl-minl-njmk` | 155.9689 | 155.9837 | 158.6138 | 160.8556 |
| **geomean** | 16.6175 | 16.4782 | 18.3738 | 20.4207 |
