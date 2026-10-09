<!-- generated from data/results/zen5-cpu/tcbench/20261009T080245Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tcbench` on `zen5-cpu`

- tprims-rs commit: `e42f6afefb709aa036f6cd3a423f858256622542`
- features: `upstream`
- harness commit: `c80c5e8490253dc1d4d12d3b2815f902201b8e2d`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-09T08:32:16.005319Z`
- timing policy: v1, best of 5 reps, priming 500 ms
- command: `scripts/record_run.py zen5-cpu tcbench`
- raw data: `data/results/zen5-cpu/tcbench/20261009T080245Z/`
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

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.6142 | 0.6143 | 0.6602 |
| `abcijk-eiab-jkec` | 2.9465 | 2.9375 | 3.0244 |
| `abcijk-eiac-jkeb` | 2.7371 | 2.7268 | 2.9905 |
| `abcijk-eibc-jkea` | 2.8437 | 2.8558 | 3.1498 |
| `abcijk-ejab-ikec` | 2.9066 | 2.9034 | 3.0166 |
| `abcijk-ejac-ikeb` | 2.7299 | 2.7191 | 2.9839 |
| `abcijk-ejbc-ikea` | 2.8501 | 2.8481 | 3.1511 |
| `abcijk-ekab-ijec` | 2.9127 | 2.9296 | 3.0116 |
| `abcijk-ekac-ijeb` | 2.7240 | 2.7401 | 2.9689 |
| `abcijk-ekbc-ijea` | 2.8417 | 2.8454 | 3.1423 |
| `abcijk-ijma-mkbc` | 2.8462 | 2.8459 | 3.1556 |
| `abcijk-ijmb-mkac` | 2.7224 | 2.7330 | 2.9915 |
| `abcijk-ijmc-mkab` | 2.9029 | 2.9025 | 3.0222 |
| `abcijk-ikma-mjbc` | 2.8559 | 2.8791 | 3.1472 |
| `abcijk-ikmb-mjac` | 2.7244 | 2.7141 | 2.9793 |
| `abcijk-ikmc-mjab` | 2.9047 | 2.9172 | 3.0241 |
| `abcijk-jkma-mibc` | 2.8464 | 2.8400 | 3.1476 |
| `abcijk-jkmb-miac` | 2.7268 | 2.7311 | 2.9974 |
| `abcijk-jkmc-miab` | 2.9465 | 2.9618 | 3.0278 |
| `abcs-rc-abrs` | 0.2942 | 0.2943 | 0.3348 |
| `abj-bka-kj` | 1.1347 | 1.1341 | 1.1645 |
| `abjc-cbka-kj` | 0.5800 | 0.5800 | 0.6325 |
| `abjc-kbac-jk` | 0.3257 | 0.3262 | 0.3669 |
| `abjcd-dkbac-jk` | 3.1601 | 3.1802 | 3.3124 |
| `abrs-qb-aqrs` | 0.2889 | 0.2892 | 0.3294 |
| `adbjc-cbdka-kj` | 8.1817 | 8.4352 | 8.7229 |
| `ajb-kba-jk` | 0.8637 | 0.8636 | 0.9188 |
| `ajbc-ckba-jk` | 0.4408 | 0.4406 | 0.4852 |
| `ajbdc-ckbad-jk` | 2.8856 | 2.9385 | 3.6034 |
| `aqrs-pa-pqrs` | 0.1848 | 0.2827 | 0.3358 |
| `ij-ik-kj` | 2.8791 | 2.2167 | 2.2780 |
| `ij-ikl-ljk` | 0.7295 | 0.7303 | 0.7957 |
| `ij-kil-lkj` | 1.1087 | 1.1066 | 1.1850 |
| `ijk-ikl-lj` | 0.6615 | 0.6624 | 0.6998 |
| `ijk-il-jlk` | 0.6500 | 0.6511 | 0.7093 |
| `ijk-ilk-jl` | 0.6125 | 0.6122 | 0.6610 |
| `ijk-ilk-lj` | 0.6543 | 0.6545 | 0.7044 |
| `ijk-ilmk-mjl` | 0.2591 | 0.2596 | 0.2754 |
| `ijkl-imjn-lnkm` | 3.7979 | 3.8129 | 3.9043 |
| `ijkl-imjn-nlmk` | 3.7887 | 3.7672 | 3.9004 |
| `ijkl-imkn-jnlm` | 3.7839 | 3.7783 | 3.8646 |
| `ijkl-imkn-njml` | 3.7574 | 3.7435 | 3.8464 |
| `ijkl-imln-jnkm` | 3.7785 | 3.7854 | 3.8662 |
| `ijkl-imln-njmk` | 3.7442 | 3.7451 | 3.8519 |
| `ijkl-imnj-nlkm` | 3.7555 | 3.7447 | 3.8542 |
| `ijkl-imnk-njml` | 3.7363 | 3.7397 | 3.8558 |
| `ijkl-minj-nlmk` | 4.6268 | 4.6699 | 4.7934 |
| `ijkl-mink-jnlm` | 4.5829 | 4.5171 | 4.6939 |
| `ijkl-minl-njmk` | 4.6417 | 4.5974 | 4.7537 |
| **geomean** | 1.8011 | 1.8093 | 1.9372 |

## 1 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.1656 | 0.1658 | 0.2180 |
| `abcijk-eiab-jkec` | 0.8714 | 0.8928 | 0.9065 |
| `abcijk-eiac-jkeb` | 0.7502 | 0.7519 | 0.8563 |
| `abcijk-eibc-jkea` | 0.8036 | 0.7890 | 0.9305 |
| `abcijk-ejab-ikec` | 0.8145 | 0.8203 | 0.8904 |
| `abcijk-ejac-ikeb` | 0.7378 | 0.7373 | 0.8426 |
| `abcijk-ejbc-ikea` | 0.8145 | 0.8017 | 0.9157 |
| `abcijk-ekab-ijec` | 0.8294 | 0.8209 | 0.8823 |
| `abcijk-ekac-ijeb` | 0.7440 | 0.7464 | 0.8435 |
| `abcijk-ekbc-ijea` | 0.8089 | 0.8129 | 0.9302 |
| `abcijk-ijma-mkbc` | 0.7967 | 0.8092 | 0.9318 |
| `abcijk-ijmb-mkac` | 0.7387 | 0.7409 | 0.8557 |
| `abcijk-ijmc-mkab` | 0.8188 | 0.8156 | 0.8862 |
| `abcijk-ikma-mjbc` | 0.8046 | 0.8140 | 0.9245 |
| `abcijk-ikmb-mjac` | 0.7421 | 0.7490 | 0.8471 |
| `abcijk-ikmc-mjab` | 0.8261 | 0.8321 | 0.8725 |
| `abcijk-jkma-mibc` | 0.7965 | 0.7917 | 0.9234 |
| `abcijk-jkmb-miac` | 0.7576 | 0.7693 | 0.8545 |
| `abcijk-jkmc-miab` | 0.8852 | 0.8832 | 0.9014 |
| `abcs-rc-abrs` | 0.0867 | 0.0866 | 0.1392 |
| `abj-bka-kj` | 0.2998 | 0.2995 | 0.3545 |
| `abjc-cbka-kj` | 0.1759 | 0.1745 | 0.2214 |
| `abjc-kbac-jk` | 0.0964 | 0.0956 | 0.1463 |
| `abjcd-dkbac-jk` | 1.2640 | 1.2345 | 1.3264 |
| `abrs-qb-aqrs` | 0.0857 | 0.0865 | 0.1399 |
| `adbjc-cbdka-kj` | 4.7986 | 5.4027 | 5.5610 |
| `ajb-kba-jk` | 0.2311 | 0.2321 | 0.2841 |
| `ajbc-ckba-jk` | 0.1371 | 0.1375 | 0.1835 |
| `ajbdc-ckbad-jk` | 1.1319 | 1.1241 | 1.4070 |
| `aqrs-pa-pqrs` | 0.0564 | 0.0834 | 0.1220 |
| `ij-ik-kj` | 0.7376 | 0.5659 | 0.6275 |
| `ij-ikl-ljk` | 0.3345 | 0.3300 | 0.3803 |
| `ij-kil-lkj` | 0.4665 | 0.4677 | 0.5608 |
| `ijk-ikl-lj` | 0.1780 | 0.1754 | 0.2301 |
| `ijk-il-jlk` | 0.1700 | 0.1691 | 0.2146 |
| `ijk-ilk-jl` | 0.1650 | 0.1649 | 0.2092 |
| `ijk-ilk-lj` | 0.1755 | 0.1746 | 0.2325 |
| `ijk-ilmk-mjl` | 0.0768 | 0.0755 | 0.1229 |
| `ijkl-imjn-lnkm` | 0.9776 | 0.9796 | 1.0844 |
| `ijkl-imjn-nlmk` | 0.9591 | 0.9564 | 1.0548 |
| `ijkl-imkn-jnlm` | 0.9633 | 0.9624 | 1.0484 |
| `ijkl-imkn-njml` | 0.9545 | 0.9520 | 1.0292 |
| `ijkl-imln-jnkm` | 0.9590 | 0.9599 | 1.0479 |
| `ijkl-imln-njmk` | 0.9575 | 0.9607 | 1.0394 |
| `ijkl-imnj-nlkm` | 0.9531 | 0.9556 | 1.0464 |
| `ijkl-imnk-njml` | 0.9480 | 0.9498 | 1.0391 |
| `ijkl-minj-nlmk` | 1.1782 | 1.1756 | 1.3034 |
| `ijkl-mink-jnlm` | 1.1501 | 1.1461 | 1.2408 |
| `ijkl-minl-njmk` | 1.1821 | 1.1720 | 1.2845 |
| **geomean** | 0.5190 | 0.5212 | 0.6151 |

## 1 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.0933 | 0.0934 | 0.2612 |
| `abcijk-eiab-jkec` | 0.5231 | 0.5252 | 0.5556 |
| `abcijk-eiac-jkeb` | 0.4632 | 0.4656 | 0.5335 |
| `abcijk-eibc-jkea` | 0.4905 | 0.4885 | 0.7317 |
| `abcijk-ejab-ikec` | 0.4743 | 0.4864 | 0.5646 |
| `abcijk-ejac-ikeb` | 0.4177 | 0.4130 | 0.5404 |
| `abcijk-ejbc-ikea` | 0.4828 | 0.4838 | 0.7036 |
| `abcijk-ekab-ijec` | 0.4963 | 0.4692 | 0.5623 |
| `abcijk-ekac-ijeb` | 0.4112 | 0.4092 | 0.5387 |
| `abcijk-ekbc-ijea` | 0.5024 | 0.5130 | 0.7418 |
| `abcijk-ijma-mkbc` | 0.4775 | 0.4681 | 0.7040 |
| `abcijk-ijmb-mkac` | 0.4108 | 0.4153 | 0.5418 |
| `abcijk-ijmc-mkab` | 0.4815 | 0.4868 | 0.5586 |
| `abcijk-ikma-mjbc` | 0.4852 | 0.4876 | 0.6995 |
| `abcijk-ikmb-mjac` | 0.4335 | 0.4350 | 0.5412 |
| `abcijk-ikmc-mjab` | 0.4762 | 0.4939 | 0.5568 |
| `abcijk-jkma-mibc` | 0.4958 | 0.4890 | 0.7277 |
| `abcijk-jkmb-miac` | 0.4721 | 0.4608 | 0.5534 |
| `abcijk-jkmc-miab` | 0.5109 | 0.5064 | 0.5592 |
| `abcs-rc-abrs` | 0.0542 | 0.0537 | 0.1579 |
| `abj-bka-kj` | 0.1766 | 0.1599 | 0.2388 |
| `abjc-cbka-kj` | 0.1070 | 0.1097 | 0.1900 |
| `abjc-kbac-jk` | 0.0589 | 0.0597 | 0.1534 |
| `abjcd-dkbac-jk` | 0.9856 | 1.0116 | 1.2077 |
| `abrs-qb-aqrs` | 0.0535 | 0.0650 | 0.1455 |
| `adbjc-cbdka-kj` | 3.1311 | 3.2921 | 3.5959 |
| `ajb-kba-jk` | 0.1252 | 0.1264 | 0.1999 |
| `ajbc-ckba-jk` | 0.0849 | 0.0851 | 0.1766 |
| `ajbdc-ckbad-jk` | 0.9341 | 0.9058 | 1.1032 |
| `aqrs-pa-pqrs` | 0.0339 | 0.0502 | 0.1128 |
| `ij-ik-kj` | 0.4103 | 0.2982 | 0.4200 |
| `ij-ikl-ljk` | 0.2324 | 0.2281 | 0.2960 |
| `ij-kil-lkj` | 0.3306 | 0.3189 | 0.4092 |
| `ijk-ikl-lj` | 0.0974 | 0.1011 | 0.1819 |
| `ijk-il-jlk` | 0.0904 | 0.0910 | 0.1574 |
| `ijk-ilk-jl` | 0.0914 | 0.0902 | 0.2582 |
| `ijk-ilk-lj` | 0.0993 | 0.0952 | 0.1881 |
| `ijk-ilmk-mjl` | 0.0545 | 0.0555 | 0.1223 |
| `ijkl-imjn-lnkm` | 0.6074 | 0.6029 | 0.7090 |
| `ijkl-imjn-nlmk` | 0.5947 | 0.5965 | 0.6847 |
| `ijkl-imkn-jnlm` | 0.5907 | 0.5867 | 0.6806 |
| `ijkl-imkn-njml` | 0.5843 | 0.5888 | 0.6731 |
| `ijkl-imln-jnkm` | 0.5888 | 0.5901 | 0.6840 |
| `ijkl-imln-njmk` | 0.5851 | 0.5894 | 0.6767 |
| `ijkl-imnj-nlkm` | 0.5973 | 0.5938 | 0.6807 |
| `ijkl-imnk-njml` | 0.5908 | 0.5924 | 0.6700 |
| `ijkl-minj-nlmk` | 0.7269 | 0.7243 | 0.8495 |
| `ijkl-mink-jnlm` | 0.7111 | 0.7094 | 0.8222 |
| `ijkl-minl-njmk` | 0.7161 | 0.7254 | 0.8254 |
| **geomean** | 0.3163 | 0.3176 | 0.4561 |

## 1 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 2.5459 | 2.5374 | 2.5474 |
| `abcijk-eiab-jkec` | 10.8857 | 10.8815 | 11.2250 |
| `abcijk-eiac-jkeb` | 10.5504 | 10.5400 | 10.7966 |
| `abcijk-eibc-jkea` | 11.0263 | 10.9966 | 11.3050 |
| `abcijk-ejab-ikec` | 10.8194 | 10.8128 | 11.0837 |
| `abcijk-ejac-ikeb` | 10.6160 | 10.6304 | 10.8284 |
| `abcijk-ejbc-ikea` | 10.9037 | 10.9167 | 11.2615 |
| `abcijk-ekab-ijec` | 10.8063 | 10.8213 | 11.1119 |
| `abcijk-ekac-ijeb` | 10.6257 | 10.6143 | 10.8026 |
| `abcijk-ekbc-ijea` | 11.0130 | 10.9967 | 11.3222 |
| `abcijk-ijma-mkbc` | 11.0022 | 11.0021 | 11.2983 |
| `abcijk-ijmb-mkac` | 10.6130 | 10.6091 | 10.8201 |
| `abcijk-ijmc-mkab` | 10.7586 | 10.7786 | 11.0314 |
| `abcijk-ikma-mjbc` | 10.8824 | 11.0082 | 11.2981 |
| `abcijk-ikmb-mjac` | 10.6204 | 10.6122 | 10.8103 |
| `abcijk-ikmc-mjab` | 10.7923 | 10.7712 | 11.0612 |
| `abcijk-jkma-mibc` | 10.9955 | 11.0006 | 11.3298 |
| `abcijk-jkmb-miac` | 10.5647 | 10.5603 | 10.7765 |
| `abcijk-jkmc-miab` | 10.8613 | 10.8670 | 11.2017 |
| `abcs-rc-abrs` | 1.1702 | 1.1697 | 1.1481 |
| `abj-bka-kj` | 3.9064 | 3.9102 | 3.9651 |
| `abjc-cbka-kj` | 1.8335 | 1.8342 | 1.8622 |
| `abjc-kbac-jk` | 1.2261 | 1.2271 | 1.2747 |
| `abjcd-dkbac-jk` | 8.7318 | 8.8408 | 9.1872 |
| `abrs-qb-aqrs` | 0.9846 | 0.9850 | 1.0432 |
| `adbjc-cbdka-kj` | 20.0323 | 20.2451 | 21.0071 |
| `ajb-kba-jk` | 3.5044 | 3.5361 | 3.5745 |
| `ajbc-ckba-jk` | 1.4216 | 1.4200 | 1.5027 |
| `ajbdc-ckbad-jk` | 8.4185 | 8.5728 | 8.9209 |
| `aqrs-pa-pqrs` | 1.2426 | 1.2396 | 1.3122 |
| `ij-ik-kj` | 8.8965 | 8.8623 | 8.9202 |
| `ij-ikl-ljk` | 3.0166 | 3.0818 | 3.0794 |
| `ij-kil-lkj` | 4.8174 | 4.7699 | 4.9517 |
| `ijk-ikl-lj` | 2.5929 | 2.6000 | 2.5533 |
| `ijk-il-jlk` | 2.7676 | 2.7970 | 2.8117 |
| `ijk-ilk-jl` | 2.5383 | 2.5148 | 2.5599 |
| `ijk-ilk-lj` | 2.6174 | 2.6260 | 2.5962 |
| `ijk-ilmk-mjl` | 0.9842 | 0.9842 | 1.0100 |
| `ijkl-imjn-lnkm` | 15.2714 | 15.2642 | 15.5069 |
| `ijkl-imjn-nlmk` | 15.2774 | 15.2528 | 15.4657 |
| `ijkl-imkn-jnlm` | 15.2534 | 15.2642 | 15.3831 |
| `ijkl-imkn-njml` | 15.3296 | 15.3106 | 15.4671 |
| `ijkl-imln-jnkm` | 15.1673 | 15.1776 | 15.3028 |
| `ijkl-imln-njmk` | 15.2493 | 15.3018 | 15.3486 |
| `ijkl-imnj-nlkm` | 15.1451 | 15.1203 | 15.2990 |
| `ijkl-imnk-njml` | 15.2262 | 15.2128 | 15.3262 |
| `ijkl-minj-nlmk` | 18.8186 | 18.8310 | 19.0904 |
| `ijkl-mink-jnlm` | 18.4445 | 18.4457 | 18.6714 |
| `ijkl-minl-njmk` | 18.8551 | 18.8404 | 19.0798 |
| **geomean** | 6.8767 | 6.8861 | 7.0251 |

## 1 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.6389 | 0.6366 | 0.6850 |
| `abcijk-eiab-jkec` | 2.8745 | 2.8760 | 3.0370 |
| `abcijk-eiac-jkeb` | 2.6859 | 2.6717 | 2.7829 |
| `abcijk-eibc-jkea` | 2.8932 | 2.9252 | 2.9127 |
| `abcijk-ejab-ikec` | 2.7587 | 2.7681 | 2.8903 |
| `abcijk-ejac-ikeb` | 2.6933 | 2.6767 | 2.8122 |
| `abcijk-ejbc-ikea` | 2.9029 | 2.9326 | 2.9037 |
| `abcijk-ekab-ijec` | 2.7916 | 2.7994 | 2.9150 |
| `abcijk-ekac-ijeb` | 2.6728 | 2.6822 | 2.8001 |
| `abcijk-ekbc-ijea` | 2.9040 | 2.8439 | 2.9274 |
| `abcijk-ijma-mkbc` | 2.9090 | 3.3861 | 2.9366 |
| `abcijk-ijmb-mkac` | 2.6678 | 2.6819 | 2.7966 |
| `abcijk-ijmc-mkab` | 2.7423 | 2.7282 | 2.8594 |
| `abcijk-ikma-mjbc` | 3.3377 | 2.9110 | 2.8969 |
| `abcijk-ikmb-mjac` | 2.6681 | 2.6708 | 2.7863 |
| `abcijk-ikmc-mjab` | 2.7255 | 2.7264 | 2.8679 |
| `abcijk-jkma-mibc` | 2.9263 | 2.9534 | 2.9414 |
| `abcijk-jkmb-miac` | 2.6835 | 2.6744 | 2.7959 |
| `abcijk-jkmc-miab` | 2.8690 | 2.8230 | 3.0013 |
| `abcs-rc-abrs` | 0.2934 | 0.2914 | 0.3543 |
| `abj-bka-kj` | 1.0736 | 1.0283 | 1.0997 |
| `abjc-cbka-kj` | 0.4905 | 0.4907 | 0.5485 |
| `abjc-kbac-jk` | 0.3132 | 0.3072 | 0.3762 |
| `abjcd-dkbac-jk` | 3.1108 | 3.1134 | 3.2989 |
| `abrs-qb-aqrs` | 0.2561 | 0.2573 | 0.3198 |
| `adbjc-cbdka-kj` | 6.9072 | 7.0204 | 7.3823 |
| `ajb-kba-jk` | 0.8964 | 0.8939 | 0.9531 |
| `ajbc-ckba-jk` | 0.3834 | 0.3827 | 0.4434 |
| `ajbdc-ckbad-jk` | 3.0326 | 3.0292 | 3.1717 |
| `aqrs-pa-pqrs` | 0.3699 | 0.3726 | 0.4204 |
| `ij-ik-kj` | 2.2619 | 2.2597 | 2.3548 |
| `ij-ikl-ljk` | 1.2862 | 1.2810 | 1.3688 |
| `ij-kil-lkj` | 2.0536 | 2.0217 | 2.0410 |
| `ijk-ikl-lj` | 0.6637 | 0.6616 | 0.6987 |
| `ijk-il-jlk` | 1.1502 | 1.1563 | 1.1888 |
| `ijk-ilk-jl` | 0.6334 | 0.6345 | 0.6864 |
| `ijk-ilk-lj` | 0.6544 | 0.6533 | 0.7035 |
| `ijk-ilmk-mjl` | 0.2782 | 0.2795 | 0.3217 |
| `ijkl-imjn-lnkm` | 4.2326 | 4.2130 | 4.3412 |
| `ijkl-imjn-nlmk` | 4.1857 | 4.2079 | 4.2482 |
| `ijkl-imkn-jnlm` | 4.1903 | 4.2121 | 4.2862 |
| `ijkl-imkn-njml` | 4.1988 | 4.1816 | 4.2352 |
| `ijkl-imln-jnkm` | 4.1620 | 4.2533 | 4.2533 |
| `ijkl-imln-njmk` | 4.1741 | 4.1566 | 4.2323 |
| `ijkl-imnj-nlkm` | 4.2082 | 4.1755 | 4.2335 |
| `ijkl-imnk-njml` | 4.1406 | 4.1715 | 4.2150 |
| `ijkl-minj-nlmk` | 5.1732 | 5.2019 | 5.2856 |
| `ijkl-mink-jnlm` | 5.0477 | 5.0644 | 5.1110 |
| `ijkl-minl-njmk` | 5.1731 | 5.1829 | 5.2204 |
| **geomean** | 1.9061 | 1.9051 | 2.0012 |

## 1 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.3277 | 0.3398 | 0.5890 |
| `abcijk-eiab-jkec` | 1.8135 | 1.7220 | 1.7194 |
| `abcijk-eiac-jkeb` | 1.5379 | 1.5442 | 1.7668 |
| `abcijk-eibc-jkea` | 1.6206 | 1.6097 | 2.5899 |
| `abcijk-ejab-ikec` | 1.6884 | 1.7231 | 1.6907 |
| `abcijk-ejac-ikeb` | 1.5328 | 1.5383 | 1.7592 |
| `abcijk-ejbc-ikea` | 1.6042 | 1.5849 | 2.5674 |
| `abcijk-ekab-ijec` | 1.6933 | 1.6395 | 1.6962 |
| `abcijk-ekac-ijeb` | 1.5269 | 1.5418 | 1.7586 |
| `abcijk-ekbc-ijea` | 1.5899 | 1.6927 | 2.5251 |
| `abcijk-ijma-mkbc` | 1.6586 | 1.6086 | 2.5288 |
| `abcijk-ijmb-mkac` | 1.5407 | 1.5272 | 1.7624 |
| `abcijk-ijmc-mkab` | 1.7749 | 1.7323 | 1.6900 |
| `abcijk-ikma-mjbc` | 1.5848 | 1.6265 | 2.5392 |
| `abcijk-ikmb-mjac` | 1.5684 | 1.5465 | 1.7705 |
| `abcijk-ikmc-mjab` | 1.7845 | 1.7736 | 1.6892 |
| `abcijk-jkma-mibc` | 1.5992 | 1.5814 | 2.5137 |
| `abcijk-jkmb-miac` | 1.5362 | 1.5398 | 1.7299 |
| `abcijk-jkmc-miab` | 1.7662 | 1.6385 | 1.6969 |
| `abcs-rc-abrs` | 0.1546 | 0.1550 | 0.2501 |
| `abj-bka-kj` | 0.5273 | 0.5260 | 0.6340 |
| `abjc-cbka-kj` | 0.2667 | 0.2634 | 0.3944 |
| `abjc-kbac-jk` | 0.1659 | 0.1635 | 0.2511 |
| `abjcd-dkbac-jk` | 2.3108 | 2.2573 | 2.4162 |
| `abrs-qb-aqrs` | 0.1377 | 0.1404 | 0.2381 |
| `adbjc-cbdka-kj` | 4.3512 | 4.4344 | 4.6738 |
| `ajb-kba-jk` | 0.4625 | 0.4506 | 0.5473 |
| `ajbc-ckba-jk` | 0.2010 | 0.2020 | 0.8329 |
| `ajbdc-ckbad-jk` | 2.2041 | 2.2220 | 4.1739 |
| `aqrs-pa-pqrs` | 0.2218 | 0.2215 | 0.2766 |
| `ij-ik-kj` | 1.1584 | 1.1566 | 1.3355 |
| `ij-ikl-ljk` | 0.7191 | 0.7148 | 0.8239 |
| `ij-kil-lkj` | 1.1227 | 1.1249 | 1.2303 |
| `ijk-ikl-lj` | 0.3380 | 0.3341 | 0.4274 |
| `ijk-il-jlk` | 0.3570 | 0.3570 | 0.4426 |
| `ijk-ilk-jl` | 0.3289 | 0.3257 | 0.5922 |
| `ijk-ilk-lj` | 0.3348 | 0.3364 | 0.4361 |
| `ijk-ilmk-mjl` | 0.1524 | 0.1517 | 0.2273 |
| `ijkl-imjn-lnkm` | 2.2196 | 2.2180 | 2.3665 |
| `ijkl-imjn-nlmk` | 2.1556 | 2.1703 | 2.2697 |
| `ijkl-imkn-jnlm` | 2.1482 | 2.1568 | 2.2922 |
| `ijkl-imkn-njml` | 2.1491 | 2.1337 | 2.2467 |
| `ijkl-imln-jnkm` | 2.1363 | 2.1527 | 2.2842 |
| `ijkl-imln-njmk` | 2.1528 | 2.1475 | 2.2400 |
| `ijkl-imnj-nlkm` | 2.1698 | 2.1651 | 2.2854 |
| `ijkl-imnk-njml` | 2.1291 | 2.1291 | 2.2381 |
| `ijkl-minj-nlmk` | 2.6506 | 2.6626 | 2.8424 |
| `ijkl-mink-jnlm` | 2.5768 | 2.5754 | 2.7094 |
| `ijkl-minl-njmk` | 2.6252 | 2.6332 | 2.7737 |
| **geomean** | 1.0433 | 1.0402 | 1.3111 |

## 16 MiB, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 14.9212 | 14.9253 | 15.3295 |
| `abcijk-eiab-jkec` | 14.7942 | 14.8280 | 15.4432 |
| `abcijk-eiac-jkeb` | 13.9226 | 13.9443 | 15.5887 |
| `abcijk-eibc-jkea` | 13.6532 | 13.6722 | 15.2015 |
| `abcijk-ejab-ikec` | 14.8403 | 14.8271 | 15.3763 |
| `abcijk-ejac-ikeb` | 14.0361 | 14.0093 | 15.6817 |
| `abcijk-ejbc-ikea` | 13.7802 | 13.8063 | 15.1969 |
| `abcijk-ekab-ijec` | 14.8057 | 14.8173 | 15.3569 |
| `abcijk-ekac-ijeb` | 13.9131 | 13.9330 | 15.6029 |
| `abcijk-ekbc-ijea` | 13.7225 | 13.7106 | 15.1658 |
| `abcijk-ijma-mkbc` | 13.6351 | 13.6418 | 15.1228 |
| `abcijk-ijmb-mkac` | 13.9468 | 13.8988 | 15.6593 |
| `abcijk-ijmc-mkab` | 14.7371 | 14.7622 | 15.3771 |
| `abcijk-ikma-mjbc` | 13.7532 | 13.7237 | 15.1641 |
| `abcijk-ikmb-mjac` | 14.0384 | 14.0212 | 15.7101 |
| `abcijk-ikmc-mjab` | 14.7775 | 14.7506 | 15.3576 |
| `abcijk-jkma-mibc` | 13.6906 | 13.7038 | 15.1147 |
| `abcijk-jkmb-miac` | 13.9468 | 14.0724 | 15.6476 |
| `abcijk-jkmc-miab` | 14.7951 | 14.8556 | 15.4148 |
| `abcs-rc-abrs` | 8.8614 | 8.9596 | 9.1096 |
| `abj-bka-kj` | 20.0263 | 19.9030 | 20.1770 |
| `abjc-cbka-kj` | 34.3963 | 34.3195 | 35.5301 |
| `abjc-kbac-jk` | 12.4351 | 12.4325 | 12.6989 |
| `abjcd-dkbac-jk` | 17.8385 | 17.8515 | 20.2958 |
| `abrs-qb-aqrs` | 8.5340 | 8.6110 | 8.5901 |
| `adbjc-cbdka-kj` | 41.3145 | 41.4363 | 43.6519 |
| `ajb-kba-jk` | 18.2200 | 18.2418 | 18.5434 |
| `ajbc-ckba-jk` | 19.6761 | 19.6460 | 21.4919 |
| `ajbdc-ckbad-jk` | 17.1587 | 17.1290 | 19.9256 |
| `aqrs-pa-pqrs` | 7.7021 | 9.2651 | 10.7689 |
| `ij-ik-kj` | 140.8104 | 130.2715 | 131.6268 |
| `ij-ikl-ljk` | 17.7474 | 17.7315 | 18.3551 |
| `ij-kil-lkj` | 21.5501 | 21.5812 | 23.0172 |
| `ijk-ikl-lj` | 15.9049 | 15.8859 | 15.8713 |
| `ijk-il-jlk` | 17.1140 | 17.1521 | 18.4459 |
| `ijk-ilk-jl` | 15.1810 | 15.2081 | 15.7025 |
| `ijk-ilk-lj` | 15.3801 | 15.3244 | 15.7720 |
| `ijk-ilmk-mjl` | 7.5223 | 7.5179 | 7.4503 |
| `ijkl-imjn-lnkm` | 254.1011 | 254.0860 | 254.9106 |
| `ijkl-imjn-nlmk` | 255.6067 | 255.4212 | 256.3306 |
| `ijkl-imkn-jnlm` | 252.1766 | 252.1407 | 259.5013 |
| `ijkl-imkn-njml` | 253.0259 | 252.7680 | 259.5889 |
| `ijkl-imln-jnkm` | 253.1118 | 253.1399 | 258.1609 |
| `ijkl-imln-njmk` | 251.0934 | 251.0928 | 258.5021 |
| `ijkl-imnj-nlkm` | 254.9716 | 254.8918 | 256.0158 |
| `ijkl-imnk-njml` | 252.1043 | 252.1105 | 258.5973 |
| `ijkl-minj-nlmk` | 310.1941 | 310.4831 | 312.1628 |
| `ijkl-mink-jnlm` | 305.1420 | 304.8219 | 314.2909 |
| `ijkl-minl-njmk` | 305.2818 | 305.0932 | 314.5858 |
| **geomean** | 29.9461 | 30.0255 | 31.6940 |

## 16 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 4.1015 | 4.0539 | 4.0924 |
| `abcijk-eiab-jkec` | 5.1750 | 5.2418 | 4.9851 |
| `abcijk-eiac-jkeb` | 4.6565 | 4.6561 | 4.8622 |
| `abcijk-eibc-jkea` | 4.3094 | 4.4056 | 4.5631 |
| `abcijk-ejab-ikec` | 4.9322 | 4.9470 | 4.9003 |
| `abcijk-ejac-ikeb` | 4.6434 | 4.6512 | 4.8365 |
| `abcijk-ejbc-ikea` | 4.3554 | 4.3912 | 4.6133 |
| `abcijk-ekab-ijec` | 4.9523 | 4.9624 | 4.9183 |
| `abcijk-ekac-ijeb` | 4.6473 | 4.6270 | 4.8598 |
| `abcijk-ekbc-ijea` | 4.3258 | 4.3455 | 4.6362 |
| `abcijk-ijma-mkbc` | 4.2930 | 4.3855 | 4.6316 |
| `abcijk-ijmb-mkac` | 4.6464 | 4.6751 | 4.8706 |
| `abcijk-ijmc-mkab` | 4.9870 | 5.0091 | 4.9073 |
| `abcijk-ikma-mjbc` | 4.3498 | 4.3938 | 4.6265 |
| `abcijk-ikmb-mjac` | 4.6677 | 4.6592 | 4.8598 |
| `abcijk-ikmc-mjab` | 4.9537 | 4.9910 | 4.9094 |
| `abcijk-jkma-mibc` | 4.3362 | 4.3185 | 4.5793 |
| `abcijk-jkmb-miac` | 4.7060 | 4.6715 | 4.8687 |
| `abcijk-jkmc-miab` | 5.2895 | 5.2004 | 4.9381 |
| `abcs-rc-abrs` | 2.7350 | 2.7236 | 2.5925 |
| `abj-bka-kj` | 5.5758 | 5.5018 | 5.8732 |
| `abjc-cbka-kj` | 12.3559 | 12.6658 | 13.4540 |
| `abjc-kbac-jk` | 3.7076 | 3.5979 | 3.7177 |
| `abjcd-dkbac-jk` | 7.1947 | 7.1339 | 7.5077 |
| `abrs-qb-aqrs` | 2.2780 | 2.2956 | 2.2890 |
| `adbjc-cbdka-kj` | 13.7059 | 13.5919 | 14.4575 |
| `ajb-kba-jk` | 4.8088 | 4.9441 | 4.9794 |
| `ajbc-ckba-jk` | 7.5112 | 7.5486 | 7.9390 |
| `ajbdc-ckbad-jk` | 6.9942 | 6.9785 | 7.5932 |
| `aqrs-pa-pqrs` | 2.1894 | 2.7128 | 3.2780 |
| `ij-ik-kj` | 42.7498 | 35.4895 | 36.1759 |
| `ij-ikl-ljk` | 6.6439 | 6.6108 | 7.0052 |
| `ij-kil-lkj` | 7.8409 | 7.8413 | 8.3186 |
| `ijk-ikl-lj` | 4.2385 | 4.2249 | 4.4223 |
| `ijk-il-jlk` | 5.7717 | 5.8277 | 6.3705 |
| `ijk-ilk-jl` | 3.9978 | 3.9830 | 4.0792 |
| `ijk-ilk-lj` | 4.0349 | 4.0439 | 4.1332 |
| `ijk-ilmk-mjl` | 2.1722 | 2.1991 | 2.2976 |
| `ijkl-imjn-lnkm` | 66.3396 | 66.3488 | 67.6963 |
| `ijkl-imjn-nlmk` | 66.6557 | 66.5556 | 67.1646 |
| `ijkl-imkn-jnlm` | 65.0211 | 65.0724 | 66.4806 |
| `ijkl-imkn-njml` | 65.7442 | 65.7205 | 67.3323 |
| `ijkl-imln-jnkm` | 64.5841 | 64.7644 | 66.2488 |
| `ijkl-imln-njmk` | 64.9968 | 65.2158 | 67.0003 |
| `ijkl-imnj-nlkm` | 66.5912 | 66.6394 | 67.4257 |
| `ijkl-imnk-njml` | 65.7022 | 65.7331 | 66.5395 |
| `ijkl-minj-nlmk` | 80.5632 | 80.5212 | 80.8516 |
| `ijkl-mink-jnlm` | 78.2507 | 78.4103 | 80.5695 |
| `ijkl-minl-njmk` | 79.1114 | 79.0942 | 81.7064 |
| **geomean** | 9.1534 | 9.1728 | 9.4666 |

## 16 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 2.1498 | 2.1555 | 2.2736 |
| `abcijk-eiab-jkec` | 3.9893 | 3.9800 | 3.6609 |
| `abcijk-eiac-jkeb` | 3.5288 | 3.4175 | 3.5944 |
| `abcijk-eibc-jkea` | 3.7144 | 3.6974 | 3.7484 |
| `abcijk-ejab-ikec` | 3.9417 | 3.8950 | 3.6408 |
| `abcijk-ejac-ikeb` | 3.5927 | 3.6049 | 3.5680 |
| `abcijk-ejbc-ikea` | 3.6351 | 3.5864 | 3.7860 |
| `abcijk-ekab-ijec` | 3.8969 | 3.9394 | 3.7418 |
| `abcijk-ekac-ijeb` | 3.5611 | 3.5620 | 3.5741 |
| `abcijk-ekbc-ijea` | 3.7153 | 3.5892 | 3.7344 |
| `abcijk-ijma-mkbc` | 3.7379 | 3.7642 | 3.7733 |
| `abcijk-ijmb-mkac` | 3.5893 | 3.4402 | 3.5641 |
| `abcijk-ijmc-mkab` | 3.9408 | 3.9023 | 3.6212 |
| `abcijk-ikma-mjbc` | 3.6027 | 3.7710 | 3.7700 |
| `abcijk-ikmb-mjac` | 3.5454 | 3.4750 | 3.5791 |
| `abcijk-ikmc-mjab` | 3.9431 | 3.8857 | 3.6607 |
| `abcijk-jkma-mibc` | 3.6957 | 3.6490 | 3.8004 |
| `abcijk-jkmb-miac` | 3.4128 | 3.4832 | 3.5650 |
| `abcijk-jkmc-miab` | 3.9629 | 3.9662 | 3.6517 |
| `abcs-rc-abrs` | 1.8760 | 1.8653 | 2.1132 |
| `abj-bka-kj` | 4.1456 | 4.1746 | 4.3868 |
| `abjc-cbka-kj` | 8.7073 | 8.4505 | 8.4082 |
| `abjc-kbac-jk` | 2.5289 | 2.5139 | 2.4593 |
| `abjcd-dkbac-jk` | 4.5464 | 4.5899 | 4.8957 |
| `abrs-qb-aqrs` | 1.3731 | 1.3750 | 1.4863 |
| `adbjc-cbdka-kj` | 8.7132 | 8.8035 | 9.2693 |
| `ajb-kba-jk` | 2.7219 | 2.7786 | 2.8399 |
| `ajbc-ckba-jk` | 5.1875 | 5.2110 | 5.6016 |
| `ajbdc-ckbad-jk` | 4.5452 | 4.5462 | 4.9092 |
| `aqrs-pa-pqrs` | 1.3869 | 1.6968 | 1.9673 |
| `ij-ik-kj` | 21.9948 | 21.1211 | 18.3535 |
| `ij-ikl-ljk` | 3.2918 | 3.2985 | 3.4391 |
| `ij-kil-lkj` | 4.4624 | 4.4455 | 4.6762 |
| `ijk-ikl-lj` | 2.4103 | 2.4140 | 2.5909 |
| `ijk-il-jlk` | 2.2638 | 2.2472 | 2.7164 |
| `ijk-ilk-jl` | 2.1125 | 2.1934 | 2.2875 |
| `ijk-ilk-lj` | 2.1280 | 2.1915 | 2.2837 |
| `ijk-ilmk-mjl` | 1.3308 | 1.3363 | 1.5052 |
| `ijkl-imjn-lnkm` | 36.0005 | 36.0897 | 36.8756 |
| `ijkl-imjn-nlmk` | 36.1347 | 36.1275 | 36.6996 |
| `ijkl-imkn-jnlm` | 34.1741 | 33.9697 | 35.0050 |
| `ijkl-imkn-njml` | 34.0032 | 34.0495 | 34.9417 |
| `ijkl-imln-jnkm` | 33.7133 | 33.6421 | 34.8541 |
| `ijkl-imln-njmk` | 33.5740 | 33.4465 | 34.7598 |
| `ijkl-imnj-nlkm` | 36.1077 | 36.1926 | 37.0758 |
| `ijkl-imnk-njml` | 34.2468 | 34.5022 | 34.8029 |
| `ijkl-minj-nlmk` | 43.3510 | 43.2867 | 44.1600 |
| `ijkl-mink-jnlm` | 41.1659 | 41.3055 | 42.8385 |
| `ijkl-minl-njmk` | 42.6134 | 42.3758 | 43.4861 |
| **geomean** | 5.8932 | 5.9085 | 6.0639 |

## 16 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 57.1934 | 57.2037 | 58.1199 |
| `abcijk-eiab-jkec` | 54.5027 | 54.4353 | 56.3480 |
| `abcijk-eiac-jkeb` | 53.4908 | 53.4941 | 54.5724 |
| `abcijk-eibc-jkea` | 54.2097 | 54.3684 | 55.5920 |
| `abcijk-ejab-ikec` | 54.0844 | 54.1075 | 55.6474 |
| `abcijk-ejac-ikeb` | 53.4703 | 53.4286 | 54.6999 |
| `abcijk-ejbc-ikea` | 54.2401 | 54.3417 | 55.6214 |
| `abcijk-ekab-ijec` | 54.0570 | 54.1159 | 55.4335 |
| `abcijk-ekac-ijeb` | 53.4748 | 53.4909 | 54.6772 |
| `abcijk-ekbc-ijea` | 54.3425 | 54.3009 | 55.5715 |
| `abcijk-ijma-mkbc` | 54.3525 | 54.3528 | 55.5652 |
| `abcijk-ijmb-mkac` | 53.4902 | 53.4564 | 54.6871 |
| `abcijk-ijmc-mkab` | 54.1035 | 54.1022 | 55.7034 |
| `abcijk-ikma-mjbc` | 54.1610 | 54.2182 | 55.7004 |
| `abcijk-ikmb-mjac` | 53.4437 | 53.4651 | 54.7505 |
| `abcijk-ikmc-mjab` | 53.9475 | 54.0094 | 55.5915 |
| `abcijk-jkma-mibc` | 54.3014 | 54.3615 | 55.6996 |
| `abcijk-jkmb-miac` | 53.5717 | 53.5613 | 54.6523 |
| `abcijk-jkmc-miab` | 54.3853 | 54.3565 | 56.3676 |
| `abcs-rc-abrs` | 31.9184 | 31.9734 | 31.0252 |
| `abj-bka-kj` | 72.4110 | 72.4028 | 73.5216 |
| `abjc-cbka-kj` | 66.8463 | 66.8898 | 67.8317 |
| `abjc-kbac-jk` | 39.8791 | 39.9337 | 40.9623 |
| `abjcd-dkbac-jk` | 43.1349 | 43.0858 | 44.6793 |
| `abrs-qb-aqrs` | 33.5039 | 33.5049 | 33.2401 |
| `adbjc-cbdka-kj` | 69.9670 | 70.9739 | 73.8791 |
| `ajb-kba-jk` | 64.2170 | 64.1742 | 64.6016 |
| `ajbc-ckba-jk` | 48.5976 | 48.5884 | 50.0558 |
| `ajbdc-ckbad-jk` | 42.8243 | 42.8087 | 43.9719 |
| `aqrs-pa-pqrs` | 31.0488 | 31.0662 | 33.2214 |
| `ij-ik-kj` | 507.4638 | 507.7843 | 520.0973 |
| `ij-ikl-ljk` | 65.0833 | 65.0813 | 67.5009 |
| `ij-kil-lkj` | 76.2279 | 76.3203 | 78.4889 |
| `ijk-ikl-lj` | 59.5863 | 59.5916 | 60.1847 |
| `ijk-il-jlk` | 57.7904 | 57.6607 | 58.4290 |
| `ijk-ilk-jl` | 57.1693 | 57.2351 | 58.0453 |
| `ijk-ilk-lj` | 59.0450 | 59.0386 | 59.9360 |
| `ijk-ilmk-mjl` | 30.7446 | 30.7302 | 30.5376 |
| `ijkl-imjn-lnkm` | 975.2514 | 975.3529 | 995.4659 |
| `ijkl-imjn-nlmk` | 977.3440 | 977.7510 | 999.8096 |
| `ijkl-imkn-jnlm` | 978.4663 | 978.1095 | 985.9231 |
| `ijkl-imkn-njml` | 982.7811 | 982.4425 | 989.7647 |
| `ijkl-imln-jnkm` | 977.4951 | 977.3970 | 983.9054 |
| `ijkl-imln-njmk` | 979.5816 | 979.8727 | 987.9853 |
| `ijkl-imnj-nlkm` | 976.7041 | 977.0645 | 996.1585 |
| `ijkl-imnk-njml` | 981.5623 | 981.7307 | 990.6488 |
| `ijkl-minj-nlmk` | 1180.1876 | 1180.0189 | 1208.1940 |
| `ijkl-mink-jnlm` | 1179.9378 | 1179.8164 | 1188.8594 |
| `ijkl-minl-njmk` | 1183.3347 | 1183.5967 | 1191.8620 |
| **geomean** | 107.0300 | 107.0809 | 109.2185 |

## 16 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 14.6843 | 14.6134 | 14.9529 |
| `abcijk-eiab-jkec` | 14.1783 | 14.1832 | 14.7149 |
| `abcijk-eiac-jkeb` | 13.6117 | 13.6356 | 13.9896 |
| `abcijk-eibc-jkea` | 13.8638 | 13.8582 | 14.1895 |
| `abcijk-ejab-ikec` | 13.9146 | 13.9302 | 14.3395 |
| `abcijk-ejac-ikeb` | 13.5996 | 13.6118 | 14.0580 |
| `abcijk-ejbc-ikea` | 13.8707 | 13.8416 | 14.1440 |
| `abcijk-ekab-ijec` | 13.9124 | 13.9336 | 14.2992 |
| `abcijk-ekac-ijeb` | 13.6220 | 13.6683 | 14.0648 |
| `abcijk-ekbc-ijea` | 13.8413 | 13.8565 | 14.1952 |
| `abcijk-ijma-mkbc` | 13.8941 | 13.9362 | 14.2576 |
| `abcijk-ijmb-mkac` | 13.5821 | 13.5978 | 14.0253 |
| `abcijk-ijmc-mkab` | 13.8910 | 13.8900 | 14.2536 |
| `abcijk-ikma-mjbc` | 13.9467 | 13.9043 | 14.2490 |
| `abcijk-ikmb-mjac` | 13.6210 | 13.6543 | 14.0522 |
| `abcijk-ikmc-mjab` | 13.9299 | 13.9508 | 14.3193 |
| `abcijk-jkma-mibc` | 13.9159 | 13.9825 | 14.2359 |
| `abcijk-jkmb-miac` | 13.6489 | 13.7250 | 14.0403 |
| `abcijk-jkmc-miab` | 14.1652 | 14.1741 | 14.8179 |
| `abcs-rc-abrs` | 8.2511 | 8.2967 | 8.0117 |
| `abj-bka-kj` | 18.9283 | 19.0130 | 19.3198 |
| `abjc-cbka-kj` | 19.8321 | 19.5048 | 20.5510 |
| `abjc-kbac-jk` | 10.2467 | 10.4938 | 10.7991 |
| `abjcd-dkbac-jk` | 13.4009 | 13.4083 | 13.9960 |
| `abrs-qb-aqrs` | 8.5388 | 8.5400 | 8.4446 |
| `adbjc-cbdka-kj` | 20.5395 | 20.5272 | 23.7904 |
| `ajb-kba-jk` | 16.3544 | 16.4227 | 16.5628 |
| `ajbc-ckba-jk` | 13.1568 | 13.0578 | 13.8139 |
| `ajbdc-ckbad-jk` | 12.8372 | 12.8765 | 13.4838 |
| `aqrs-pa-pqrs` | 8.0566 | 8.0945 | 8.5533 |
| `ij-ik-kj` | 128.6803 | 128.6735 | 132.2279 |
| `ij-ikl-ljk` | 23.0069 | 22.8685 | 23.7088 |
| `ij-kil-lkj` | 26.3877 | 26.4121 | 27.1289 |
| `ijk-ikl-lj` | 15.2762 | 15.2453 | 15.3991 |
| `ijk-il-jlk` | 20.2695 | 19.7533 | 19.9657 |
| `ijk-ilk-jl` | 15.1708 | 14.7760 | 14.9209 |
| `ijk-ilk-lj` | 15.0580 | 15.0722 | 15.4312 |
| `ijk-ilmk-mjl` | 8.4002 | 8.3772 | 8.1137 |
| `ijkl-imjn-lnkm` | 249.9898 | 249.6753 | 255.8809 |
| `ijkl-imjn-nlmk` | 248.5615 | 248.5730 | 254.5518 |
| `ijkl-imkn-jnlm` | 247.6425 | 247.5935 | 251.1848 |
| `ijkl-imkn-njml` | 249.0609 | 248.4807 | 252.2374 |
| `ijkl-imln-jnkm` | 247.5524 | 247.4248 | 250.4284 |
| `ijkl-imln-njmk` | 248.3843 | 248.4880 | 251.6724 |
| `ijkl-imnj-nlkm` | 248.4175 | 248.3691 | 254.2542 |
| `ijkl-imnk-njml` | 249.0427 | 249.0424 | 252.2257 |
| `ijkl-minj-nlmk` | 299.4966 | 299.5403 | 305.9766 |
| `ijkl-mink-jnlm` | 298.4058 | 298.6042 | 301.9200 |
| `ijkl-minl-njmk` | 299.6976 | 299.7954 | 302.3432 |
| **geomean** | 28.3587 | 28.3450 | 29.0555 |

## 16 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 7.5618 | 7.5634 | 7.6838 |
| `abcijk-eiab-jkec` | 8.9476 | 8.9320 | 8.2043 |
| `abcijk-eiac-jkeb` | 8.3223 | 8.2870 | 8.3682 |
| `abcijk-eibc-jkea` | 8.4809 | 8.4720 | 10.0405 |
| `abcijk-ejab-ikec` | 8.2762 | 8.7861 | 8.1677 |
| `abcijk-ejac-ikeb` | 8.2434 | 8.3024 | 8.3941 |
| `abcijk-ejbc-ikea` | 8.4059 | 8.3666 | 10.0876 |
| `abcijk-ekab-ijec` | 8.3940 | 8.9534 | 8.2146 |
| `abcijk-ekac-ijeb` | 8.3099 | 8.2700 | 8.3764 |
| `abcijk-ekbc-ijea` | 8.4184 | 8.4532 | 10.0834 |
| `abcijk-ijma-mkbc` | 8.5934 | 8.3983 | 9.9782 |
| `abcijk-ijmb-mkac` | 8.2553 | 8.2386 | 8.3902 |
| `abcijk-ijmc-mkab` | 9.0213 | 8.9906 | 8.1432 |
| `abcijk-ikma-mjbc` | 8.4341 | 8.3885 | 10.0123 |
| `abcijk-ikmb-mjac` | 8.2526 | 8.3459 | 8.4057 |
| `abcijk-ikmc-mjab` | 8.7641 | 8.9834 | 8.1468 |
| `abcijk-jkma-mibc` | 8.3662 | 8.3883 | 9.9898 |
| `abcijk-jkmb-miac` | 8.2940 | 8.2254 | 8.3864 |
| `abcijk-jkmc-miab` | 8.8598 | 8.7514 | 8.2009 |
| `abcs-rc-abrs` | 4.9507 | 4.6156 | 4.4693 |
| `abj-bka-kj` | 10.5395 | 10.3677 | 10.6931 |
| `abjc-cbka-kj` | 12.8640 | 12.9128 | 12.9404 |
| `abjc-kbac-jk` | 6.0132 | 5.8879 | 8.1290 |
| `abjcd-dkbac-jk` | 8.8196 | 8.7891 | 9.0737 |
| `abrs-qb-aqrs` | 4.9688 | 4.5876 | 4.5693 |
| `adbjc-cbdka-kj` | 13.5349 | 13.8401 | 13.9553 |
| `ajb-kba-jk` | 8.5106 | 8.6085 | 8.6992 |
| `ajbc-ckba-jk` | 8.7546 | 8.6066 | 39.8557 |
| `ajbdc-ckbad-jk` | 8.4048 | 8.4929 | 30.0541 |
| `aqrs-pa-pqrs` | 4.3590 | 4.3650 | 4.6883 |
| `ij-ik-kj` | 70.8862 | 70.6621 | 72.8924 |
| `ij-ikl-ljk` | 16.2592 | 16.3874 | 16.8982 |
| `ij-kil-lkj` | 18.6189 | 18.8505 | 19.4024 |
| `ijk-ikl-lj` | 7.8895 | 7.8990 | 7.9497 |
| `ijk-il-jlk` | 13.7265 | 13.7268 | 13.9166 |
| `ijk-ilk-jl` | 7.5296 | 7.5397 | 7.6968 |
| `ijk-ilk-lj` | 7.7603 | 7.7692 | 7.9721 |
| `ijk-ilmk-mjl` | 4.5549 | 4.4954 | 4.8566 |
| `ijkl-imjn-lnkm` | 130.9770 | 130.7943 | 138.0861 |
| `ijkl-imjn-nlmk` | 130.0758 | 129.9383 | 135.8315 |
| `ijkl-imkn-jnlm` | 128.6562 | 128.8466 | 132.6846 |
| `ijkl-imkn-njml` | 130.3400 | 130.3778 | 134.7118 |
| `ijkl-imln-jnkm` | 128.3346 | 128.3077 | 132.3564 |
| `ijkl-imln-njmk` | 130.1191 | 130.0277 | 133.6142 |
| `ijkl-imnj-nlkm` | 130.4497 | 130.0766 | 135.9980 |
| `ijkl-imnk-njml` | 130.9321 | 131.4630 | 135.2186 |
| `ijkl-minj-nlmk` | 157.3958 | 157.2530 | 162.7416 |
| `ijkl-mink-jnlm` | 155.1833 | 155.1522 | 158.7186 |
| `ijkl-minl-njmk` | 156.4790 | 156.3810 | 159.7941 |
| **geomean** | 16.5231 | 16.5064 | 18.0897 |
