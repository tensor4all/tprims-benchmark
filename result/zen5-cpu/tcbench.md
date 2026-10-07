<!-- generated from data/results/zen5-cpu/tcbench/20261007T225255Z-smoke/report.md by scripts/record_run.py; the report below is the source of truth -->

# `tcbench` on `zen5-cpu`

- tprims-rs commit: `0aeb77dd6728d94b43f5690ebbb3dfac2dde1fad`
- features: `upstream`
- harness commit: `0aeb77dd6728d94b43f5690ebbb3dfac2dde1fad`
- host: `AMD Ryzen AI 9 HX 470` (24 logical)
- timestamp: `2026-10-07T22:53:09.156287Z`
- timing policy: v1, best of 1 reps, priming 500 ms
- command: `scripts/record_run.py zen5-cpu tcbench --sizes 1 --threads 1 --dtypes f64 --engines plan --reps 1 --aa 1 --label smoke`
- raw data: `/home/shinaoka/projects/tensor4all/tprims-benchmark/data/results/zen5-cpu/tcbench/20261007T225255Z-smoke/`

Every row below passed `tcbench verify` (known values and full-output residual <= 1e-10) before timing. Values are the geometric mean over repetitions and A/A repeats of the best wall time per engine.

## 1.0 MiB, f64, 1T (CPU 4)

| case | plan (ms) |
|---|---|
| `abc-bk-akc` | 0.6671 |
| `abcijk-eiab-jkec` | 3.1373 |
| `abcijk-eiac-jkeb` | 2.7854 |
| `abcijk-eibc-jkea` | 2.9564 |
| `abcijk-ejab-ikec` | 2.9398 |
| `abcijk-ejac-ikeb` | 2.7672 |
| `abcijk-ejbc-ikea` | 3.0005 |
| `abcijk-ekab-ijec` | 2.9287 |
| `abcijk-ekac-ijeb` | 2.7466 |
| `abcijk-ekbc-ijea` | 2.9609 |
| `abcijk-ijma-mkbc` | 4.0732 |
| `abcijk-ijmb-mkac` | 3.7711 |
| `abcijk-ijmc-mkab` | 3.9513 |
| `abcijk-ikma-mjbc` | 4.0173 |
| `abcijk-ikmb-mjac` | 3.7728 |
| `abcijk-ikmc-mjab` | 3.8542 |
| `abcijk-jkma-mibc` | 3.7153 |
| `abcijk-jkmb-miac` | 3.3493 |
| `abcijk-jkmc-miab` | 3.3197 |
| `abcs-rc-abrs` | 0.4100 |
| `abj-bka-kj` | 1.5876 |
| `abjc-cbka-kj` | 0.7722 |
| `abjc-kbac-jk` | 0.4622 |
| `abjcd-dkbac-jk` | 3.8385 |
| `abrs-qb-aqrs` | 0.4088 |
| `adbjc-cbdka-kj` | 10.3643 |
| `ajb-kba-jk` | 1.2222 |
| `ajbc-ckba-jk` | 0.6219 |
| `ajbdc-ckbad-jk` | 3.6764 |
| `aqrs-pa-pqrs` | 0.2780 |
| `ij-ik-kj` | 2.9276 |
| `ij-ikl-ljk` | 1.0438 |
| `ij-kil-lkj` | 1.5594 |
| `ijk-ikl-lj` | 0.9310 |
| `ijk-il-jlk` | 0.9131 |
| `ijk-ilk-jl` | 0.8712 |
| `ijk-ilk-lj` | 0.9283 |
| `ijk-ilmk-mjl` | 0.3673 |
| `ijkl-imjn-lnkm` | 5.3044 |
| `ijkl-imjn-nlmk` | 5.2832 |
| `ijkl-imkn-jnlm` | 5.2481 |
| `ijkl-imkn-njml` | 5.2796 |
| `ijkl-imln-jnkm` | 5.2423 |
| `ijkl-imln-njmk` | 5.2377 |
| `ijkl-imnj-nlkm` | 5.2397 |
| `ijkl-imnk-njml` | 5.2560 |
| `ijkl-minj-nlmk` | 6.4801 |
| `ijkl-mink-jnlm` | 6.3418 |
| `ijkl-minl-njmk` | 6.4352 |
| **geomean** | 2.3196 |
