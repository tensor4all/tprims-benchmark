# `tcbench` on `zen5-cpu`

- tprims-rs commit: `b01471956e4f92a379442a75ff628e202c892217`
- features: `default`
- harness commit: `d16afcbab1c38fcb609cd28accdb063a8725530e`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-09T23:01:45.160071Z`
- timing policy: v1, best of 5 reps, priming 1500 ms
- command: `scripts/record_run.py zen5-cpu tcbench --jobs 24`
- raw data: `data/results/zen5-cpu/tcbench/20261009T224615Z/`
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

## 16 MiB, f64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) |
|---|---|---|
| `abc-bk-akc` | 15.2241 | 15.2203 |
| `abcijk-eiab-jkec` | 14.9003 | 14.9248 |
| `abcijk-eiac-jkeb` | 14.0582 | 13.9952 |
| `abcijk-eibc-jkea` | 13.7619 | 13.7513 |
| `abcijk-ejab-ikec` | 14.7621 | 14.7543 |
| `abcijk-ejac-ikeb` | 13.9979 | 14.0546 |
| `abcijk-ejbc-ikea` | 13.8990 | 13.8963 |
| `abcijk-ekab-ijec` | 14.7700 | 14.7587 |
| `abcijk-ekac-ijeb` | 13.8996 | 13.9811 |
| `abcijk-ekbc-ijea` | 13.8512 | 13.8306 |
| `abcijk-ijma-mkbc` | 13.8587 | 13.8297 |
| `abcijk-ijmb-mkac` | 13.9364 | 14.0154 |
| `abcijk-ijmc-mkab` | 14.7446 | 14.7434 |
| `abcijk-ikma-mjbc` | 13.9118 | 13.8922 |
| `abcijk-ikmb-mjac` | 14.0603 | 14.0801 |
| `abcijk-ikmc-mjab` | 14.6443 | 14.6753 |
| `abcijk-jkma-mibc` | 13.7597 | 13.7332 |
| `abcijk-jkmb-miac` | 14.0864 | 14.0364 |
| `abcijk-jkmc-miab` | 14.8557 | 14.8351 |
| `abcs-rc-abrs` | 9.4443 | 9.4284 |
| `abj-bka-kj` | 19.4096 | 19.4405 |
| `abjc-cbka-kj` | 37.8119 | 37.8527 |
| `abjc-kbac-jk` | 12.7124 | 12.4043 |
| `abjcd-dkbac-jk` | 17.5171 | 17.3814 |
| `abrs-qb-aqrs` | 8.3799 | 8.4904 |
| `adbjc-cbdka-kj` | 47.3507 | 47.3660 |
| `ajb-kba-jk` | 18.1681 | 18.1824 |
| `ajbc-ckba-jk` | 20.9393 | 20.9525 |
| `ajbdc-ckbad-jk` | 17.3729 | 17.2187 |
| `aqrs-pa-pqrs` | 7.5050 | 9.1740 |
| `ij-ik-kj` | 124.2547 | 130.2224 |
| `ij-ikl-ljk` | 17.7063 | 17.7156 |
| `ij-kil-lkj` | 21.4592 | 21.5748 |
| `ijk-ikl-lj` | 15.8883 | 15.8826 |
| `ijk-il-jlk` | 16.1678 | 16.2423 |
| `ijk-ilk-jl` | 15.4684 | 15.3956 |
| `ijk-ilk-lj` | 15.5689 | 15.4768 |
| `ijk-ilmk-mjl` | 7.5038 | 7.4456 |
| `ijkl-imjn-lnkm` | 253.4014 | 253.1615 |
| `ijkl-imjn-nlmk` | 254.3880 | 254.5169 |
| `ijkl-imkn-jnlm` | 252.2329 | 252.7444 |
| `ijkl-imkn-njml` | 251.6785 | 251.4385 |
| `ijkl-imln-jnkm` | 251.1762 | 251.0035 |
| `ijkl-imln-njmk` | 250.2093 | 249.1360 |
| `ijkl-imnj-nlkm` | 253.3352 | 253.3956 |
| `ijkl-imnk-njml` | 250.5223 | 250.5520 |
| `ijkl-minj-nlmk` | 310.5533 | 310.2963 |
| `ijkl-mink-jnlm` | 305.6230 | 305.2745 |
| `ijkl-minl-njmk` | 305.0170 | 305.2624 |
| **geomean** | 30.0622 | 30.1917 |

## 16 MiB, f64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) |
|---|---|---|
| `abc-bk-akc` | 3.9131 | 3.8793 |
| `abcijk-eiab-jkec` | 5.1859 | 5.1993 |
| `abcijk-eiac-jkeb` | 4.6411 | 4.6241 |
| `abcijk-eibc-jkea` | 4.3623 | 4.2557 |
| `abcijk-ejab-ikec` | 4.9834 | 4.9748 |
| `abcijk-ejac-ikeb` | 4.6339 | 4.6191 |
| `abcijk-ejbc-ikea` | 4.4052 | 4.3773 |
| `abcijk-ekab-ijec` | 4.9705 | 4.9712 |
| `abcijk-ekac-ijeb` | 4.6248 | 4.6153 |
| `abcijk-ekbc-ijea` | 4.3566 | 4.2745 |
| `abcijk-ijma-mkbc` | 4.2686 | 4.3760 |
| `abcijk-ijmb-mkac` | 4.6142 | 4.6007 |
| `abcijk-ijmc-mkab` | 4.9327 | 4.9398 |
| `abcijk-ikma-mjbc` | 4.2797 | 4.2673 |
| `abcijk-ikmb-mjac` | 4.6035 | 4.6181 |
| `abcijk-ikmc-mjab` | 4.9884 | 4.9811 |
| `abcijk-jkma-mibc` | 4.3440 | 4.2329 |
| `abcijk-jkmb-miac` | 4.6379 | 4.6164 |
| `abcijk-jkmc-miab` | 5.1815 | 5.2409 |
| `abcs-rc-abrs` | 2.6209 | 2.5469 |
| `abj-bka-kj` | 5.4464 | 5.4524 |
| `abjc-cbka-kj` | 13.0056 | 12.6571 |
| `abjc-kbac-jk` | 3.7494 | 3.6509 |
| `abjcd-dkbac-jk` | 7.1584 | 7.1043 |
| `abrs-qb-aqrs` | 2.2167 | 2.2103 |
| `adbjc-cbdka-kj` | 14.7441 | 15.2208 |
| `ajb-kba-jk` | 4.8205 | 4.7768 |
| `ajbc-ckba-jk` | 7.9866 | 8.1249 |
| `ajbdc-ckbad-jk` | 6.9874 | 6.9506 |
| `aqrs-pa-pqrs` | 2.1915 | 2.7273 |
| `ij-ik-kj` | 31.0467 | 35.4023 |
| `ij-ikl-ljk` | 6.2976 | 6.6354 |
| `ij-kil-lkj` | 7.6407 | 7.5507 |
| `ijk-ikl-lj` | 4.1455 | 4.1401 |
| `ijk-il-jlk` | 5.8049 | 5.8819 |
| `ijk-ilk-jl` | 3.8992 | 3.9568 |
| `ijk-ilk-lj` | 3.9655 | 3.9514 |
| `ijk-ilmk-mjl` | 2.1725 | 2.1180 |
| `ijkl-imjn-lnkm` | 66.7218 | 67.0224 |
| `ijkl-imjn-nlmk` | 66.5645 | 66.6585 |
| `ijkl-imkn-jnlm` | 65.6398 | 65.4607 |
| `ijkl-imkn-njml` | 65.4004 | 65.3812 |
| `ijkl-imln-jnkm` | 64.6383 | 65.1610 |
| `ijkl-imln-njmk` | 64.7898 | 64.8369 |
| `ijkl-imnj-nlkm` | 65.9692 | 66.6749 |
| `ijkl-imnk-njml` | 65.2789 | 65.4224 |
| `ijkl-minj-nlmk` | 80.1845 | 80.1344 |
| `ijkl-mink-jnlm` | 78.7471 | 78.6786 |
| `ijkl-minl-njmk` | 78.0041 | 77.8436 |
| **geomean** | 9.0660 | 9.1194 |

## 16 MiB, c64, 1T (CPU 4)

| case | tprims [plan] (ms) | tprims [packed] (ms) |
|---|---|---|
| `abc-bk-akc` | 57.0780 | 57.1332 |
| `abcijk-eiab-jkec` | 54.4451 | 54.4496 |
| `abcijk-eiac-jkeb` | 53.6476 | 53.6081 |
| `abcijk-eibc-jkea` | 54.4196 | 54.4102 |
| `abcijk-ejab-ikec` | 54.1338 | 54.1188 |
| `abcijk-ejac-ikeb` | 53.5775 | 53.5125 |
| `abcijk-ejbc-ikea` | 54.4603 | 54.4485 |
| `abcijk-ekab-ijec` | 54.1195 | 54.0685 |
| `abcijk-ekac-ijeb` | 53.6015 | 53.5799 |
| `abcijk-ekbc-ijea` | 54.4073 | 54.3734 |
| `abcijk-ijma-mkbc` | 54.3037 | 54.3503 |
| `abcijk-ijmb-mkac` | 53.5941 | 53.4450 |
| `abcijk-ijmc-mkab` | 54.1215 | 54.1490 |
| `abcijk-ikma-mjbc` | 54.3839 | 54.3525 |
| `abcijk-ikmb-mjac` | 53.5786 | 53.5412 |
| `abcijk-ikmc-mjab` | 54.1112 | 54.1384 |
| `abcijk-jkma-mibc` | 54.3415 | 54.3873 |
| `abcijk-jkmb-miac` | 53.6618 | 53.6615 |
| `abcijk-jkmc-miab` | 54.5679 | 54.4059 |
| `abcs-rc-abrs` | 31.8557 | 31.8033 |
| `abj-bka-kj` | 72.9996 | 72.8825 |
| `abjc-cbka-kj` | 67.7332 | 67.7026 |
| `abjc-kbac-jk` | 39.4889 | 39.3919 |
| `abjcd-dkbac-jk` | 42.9765 | 42.9399 |
| `abrs-qb-aqrs` | 33.3000 | 32.9837 |
| `adbjc-cbdka-kj` | 73.0566 | 72.9614 |
| `ajb-kba-jk` | 64.2946 | 64.3672 |
| `ajbc-ckba-jk` | 49.0370 | 49.0848 |
| `ajbdc-ckbad-jk` | 42.7573 | 42.7520 |
| `aqrs-pa-pqrs` | 31.4835 | 31.4661 |
| `ij-ik-kj` | 507.9733 | 508.6932 |
| `ij-ikl-ljk` | 64.9075 | 64.8239 |
| `ij-kil-lkj` | 76.0900 | 76.0731 |
| `ijk-ikl-lj` | 59.8318 | 59.7445 |
| `ijk-il-jlk` | 58.1521 | 58.2203 |
| `ijk-ilk-jl` | 57.3371 | 57.3693 |
| `ijk-ilk-lj` | 59.2646 | 59.3463 |
| `ijk-ilmk-mjl` | 30.6943 | 30.6670 |
| `ijkl-imjn-lnkm` | 973.6787 | 974.3019 |
| `ijkl-imjn-nlmk` | 975.7023 | 975.4749 |
| `ijkl-imkn-jnlm` | 978.6674 | 977.9309 |
| `ijkl-imkn-njml` | 984.6054 | 984.5455 |
| `ijkl-imln-jnkm` | 976.7362 | 977.3849 |
| `ijkl-imln-njmk` | 977.6556 | 978.1520 |
| `ijkl-imnj-nlkm` | 975.0245 | 974.8924 |
| `ijkl-imnk-njml` | 982.0552 | 981.6971 |
| `ijkl-minj-nlmk` | 1181.1820 | 1180.4816 |
| `ijkl-mink-jnlm` | 1181.1668 | 1180.7858 |
| `ijkl-minl-njmk` | 1185.8425 | 1185.1599 |
| **geomean** | 107.2669 | 107.2124 |

## 16 MiB, c64, 4T (CPU 4-7)

| case | tprims [plan] (ms) | tprims [packed] (ms) |
|---|---|---|
| `abc-bk-akc` | 14.5583 | 14.5425 |
| `abcijk-eiab-jkec` | 14.1771 | 14.1854 |
| `abcijk-eiac-jkeb` | 13.5859 | 13.5656 |
| `abcijk-eibc-jkea` | 13.9237 | 13.9275 |
| `abcijk-ejab-ikec` | 13.9503 | 13.9460 |
| `abcijk-ejac-ikeb` | 13.5643 | 13.6812 |
| `abcijk-ejbc-ikea` | 13.9761 | 13.9111 |
| `abcijk-ekab-ijec` | 13.9073 | 13.9189 |
| `abcijk-ekac-ijeb` | 13.5717 | 13.5079 |
| `abcijk-ekbc-ijea` | 14.0057 | 13.9749 |
| `abcijk-ijma-mkbc` | 13.8648 | 13.8578 |
| `abcijk-ijmb-mkac` | 13.5662 | 13.5335 |
| `abcijk-ijmc-mkab` | 13.8902 | 13.9069 |
| `abcijk-ikma-mjbc` | 13.9353 | 13.9888 |
| `abcijk-ikmb-mjac` | 13.5660 | 13.6296 |
| `abcijk-ikmc-mjab` | 13.9051 | 13.9147 |
| `abcijk-jkma-mibc` | 13.9102 | 13.9172 |
| `abcijk-jkmb-miac` | 13.6335 | 13.6104 |
| `abcijk-jkmc-miab` | 14.1784 | 14.1564 |
| `abcs-rc-abrs` | 8.0823 | 8.1530 |
| `abj-bka-kj` | 19.1417 | 19.0205 |
| `abjc-cbka-kj` | 20.3935 | 20.6456 |
| `abjc-kbac-jk` | 10.5542 | 10.5634 |
| `abjcd-dkbac-jk` | 13.3145 | 13.4252 |
| `abrs-qb-aqrs` | 8.5248 | 8.4837 |
| `adbjc-cbdka-kj` | 20.5914 | 21.0348 |
| `ajb-kba-jk` | 16.4638 | 16.4141 |
| `ajbc-ckba-jk` | 13.4196 | 13.4091 |
| `ajbdc-ckbad-jk` | 12.9583 | 12.8413 |
| `aqrs-pa-pqrs` | 8.1647 | 8.1354 |
| `ij-ik-kj` | 128.6808 | 128.6296 |
| `ij-ikl-ljk` | 22.7486 | 22.8148 |
| `ij-kil-lkj` | 26.4933 | 26.4897 |
| `ijk-ikl-lj` | 15.6237 | 15.3133 |
| `ijk-il-jlk` | 19.7275 | 19.7935 |
| `ijk-ilk-jl` | 14.5572 | 14.6239 |
| `ijk-ilk-lj` | 15.0483 | 15.0886 |
| `ijk-ilmk-mjl` | 7.9679 | 7.9536 |
| `ijkl-imjn-lnkm` | 250.2238 | 250.1937 |
| `ijkl-imjn-nlmk` | 248.2993 | 248.1224 |
| `ijkl-imkn-jnlm` | 248.0051 | 248.0750 |
| `ijkl-imkn-njml` | 248.8729 | 249.0722 |
| `ijkl-imln-jnkm` | 247.4994 | 247.5275 |
| `ijkl-imln-njmk` | 248.3925 | 248.0787 |
| `ijkl-imnj-nlkm` | 248.4890 | 248.4877 |
| `ijkl-imnk-njml` | 248.7843 | 249.0390 |
| `ijkl-minj-nlmk` | 299.9749 | 299.9139 |
| `ijkl-mink-jnlm` | 298.1123 | 298.8692 |
| `ijkl-minl-njmk` | 299.2222 | 299.2423 |
| **geomean** | 28.3482 | 28.3586 |
