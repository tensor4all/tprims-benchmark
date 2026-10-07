# `tcbench` on `zen5-cpu`

- tprims-rs commit: `0aeb77dd6728d94b43f5690ebbb3dfac2dde1fad`
- features: `upstream`
- harness commit: `0aeb77dd6728d94b43f5690ebbb3dfac2dde1fad`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-07T23:05:33.177088Z`
- timing policy: v1, best of 5 reps, priming 500 ms
- command: `scripts/record_run.py zen5-cpu tcbench`
- raw data: `data/results/zen5-cpu/tcbench/20261007T225350Z/`

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
| `abc-bk-akc` | 0.6270 | 0.6185 | 0.6692 |
| `abcijk-eiab-jkec` | 3.0001 | 2.9766 | 3.0528 |
| `abcijk-eiac-jkeb` | 2.7632 | 2.7884 | 2.9927 |
| `abcijk-eibc-jkea` | 2.8916 | 2.8949 | 3.1796 |
| `abcijk-ejab-ikec` | 2.9508 | 2.9444 | 3.0740 |
| `abcijk-ejac-ikeb` | 2.7359 | 2.7336 | 2.9755 |
| `abcijk-ejbc-ikea` | 2.9109 | 2.8947 | 3.1795 |
| `abcijk-ekab-ijec` | 2.9248 | 2.8944 | 3.0558 |
| `abcijk-ekac-ijeb` | 2.7796 | 2.7189 | 2.9765 |
| `abcijk-ekbc-ijea` | 2.9046 | 2.8850 | 3.1568 |
| `abcijk-ijma-mkbc` | 2.9203 | 2.9311 | 3.1496 |
| `abcijk-ijmb-mkac` | 2.7451 | 2.7498 | 3.0038 |
| `abcijk-ijmc-mkab` | 2.9273 | 2.9262 | 3.0741 |
| `abcijk-ikma-mjbc` | 2.9498 | 2.8698 | 3.1753 |
| `abcijk-ikmb-mjac` | 2.7406 | 2.7533 | 2.9871 |
| `abcijk-ikmc-mjab` | 2.9465 | 2.9067 | 3.1057 |
| `abcijk-jkma-mibc` | 2.8879 | 2.9165 | 3.1645 |
| `abcijk-jkmb-miac` | 2.7471 | 2.7752 | 2.9935 |
| `abcijk-jkmc-miab` | 2.9752 | 2.9633 | 3.0581 |
| `abcs-rc-abrs` | 0.2989 | 0.2976 | 0.3359 |
| `abj-bka-kj` | 1.1407 | 1.1321 | 1.1827 |
| `abjc-cbka-kj` | 0.6164 | 0.6054 | 0.6294 |
| `abjc-kbac-jk` | 0.3411 | 0.3390 | 0.3794 |
| `abjcd-dkbac-jk` | 3.1999 | 3.1755 | 3.3366 |
| `abrs-qb-aqrs` | 0.2917 | 0.2918 | 0.3311 |
| `adbjc-cbdka-kj` | 8.8438 | 8.7110 | 9.0657 |
| `ajb-kba-jk` | 0.9470 | 0.9379 | 0.9661 |
| `ajbc-ckba-jk` | 0.4629 | 0.4607 | 0.4954 |
| `ajbdc-ckbad-jk` | 2.9897 | 2.9502 | 3.6249 |
| `aqrs-pa-pqrs` | 0.1889 | 0.2844 | 0.3352 |
| `ij-ik-kj` | 2.8810 | 3.0908 | 3.2054 |
| `ij-ikl-ljk` | 1.0456 | 1.0454 | 1.1188 |
| `ij-kil-lkj` | 1.5285 | 1.5291 | 1.6412 |
| `ijk-ikl-lj` | 0.9645 | 0.9442 | 0.9900 |
| `ijk-il-jlk` | 0.8093 | 0.7923 | 0.8452 |
| `ijk-ilk-jl` | 0.6232 | 0.6198 | 0.6708 |
| `ijk-ilk-lj` | 0.6711 | 0.6713 | 0.7077 |
| `ijk-ilmk-mjl` | 0.2610 | 0.2606 | 0.2798 |
| `ijkl-imjn-lnkm` | 3.8086 | 3.8006 | 3.9183 |
| `ijkl-imjn-nlmk` | 3.7691 | 3.7689 | 3.8859 |
| `ijkl-imkn-jnlm` | 3.7558 | 3.7426 | 3.8575 |
| `ijkl-imkn-njml` | 3.7564 | 3.7563 | 3.8456 |
| `ijkl-imln-jnkm` | 3.7490 | 3.7585 | 3.8387 |
| `ijkl-imln-njmk` | 3.7476 | 3.7584 | 3.9028 |
| `ijkl-imnj-nlkm` | 3.7422 | 3.7376 | 3.8473 |
| `ijkl-imnk-njml` | 3.7331 | 3.7388 | 3.8506 |
| `ijkl-minj-nlmk` | 4.7691 | 4.6919 | 4.8201 |
| `ijkl-mink-jnlm` | 4.5555 | 4.5753 | 4.6861 |
| `ijkl-minl-njmk` | 4.6808 | 4.6429 | 4.7908 |
| **geomean** | 1.8777 | 1.8873 | 2.0139 |

## 1 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.1653 | 0.1655 | 0.2288 |
| `abcijk-eiab-jkec` | 0.9107 | 0.9113 | 0.9350 |
| `abcijk-eiac-jkeb` | 0.7822 | 0.7755 | 0.8819 |
| `abcijk-eibc-jkea` | 0.8467 | 0.8402 | 0.9243 |
| `abcijk-ejab-ikec` | 0.8572 | 0.8531 | 0.9270 |
| `abcijk-ejac-ikeb` | 0.7687 | 0.7544 | 0.8690 |
| `abcijk-ejbc-ikea` | 0.8457 | 0.8303 | 0.9552 |
| `abcijk-ekab-ijec` | 0.8992 | 0.8708 | 0.9071 |
| `abcijk-ekac-ijeb` | 0.7733 | 0.7537 | 0.8582 |
| `abcijk-ekbc-ijea` | 0.8306 | 0.8351 | 0.9479 |
| `abcijk-ijma-mkbc` | 0.9019 | 0.8576 | 0.9523 |
| `abcijk-ijmb-mkac` | 0.7674 | 0.7556 | 0.8936 |
| `abcijk-ijmc-mkab` | 0.8644 | 0.8289 | 0.9383 |
| `abcijk-ikma-mjbc` | 0.8396 | 0.8449 | 0.9535 |
| `abcijk-ikmb-mjac` | 0.8592 | 0.7460 | 0.8617 |
| `abcijk-ikmc-mjab` | 0.8599 | 0.8255 | 0.9073 |
| `abcijk-jkma-mibc` | 0.8424 | 0.8379 | 0.9406 |
| `abcijk-jkmb-miac` | 0.8137 | 0.7711 | 0.8514 |
| `abcijk-jkmc-miab` | 0.8973 | 0.9018 | 0.9388 |
| `abcs-rc-abrs` | 0.0885 | 0.0875 | 0.1592 |
| `abj-bka-kj` | 0.2995 | 0.2960 | 0.3677 |
| `abjc-cbka-kj` | 0.1629 | 0.1685 | 0.2348 |
| `abjc-kbac-jk` | 0.0985 | 0.0969 | 0.1674 |
| `abjcd-dkbac-jk` | 1.3243 | 1.2363 | 1.3442 |
| `abrs-qb-aqrs` | 0.0876 | 0.0864 | 0.1542 |
| `adbjc-cbdka-kj` | 4.8413 | 5.3552 | 5.5209 |
| `ajb-kba-jk` | 0.2324 | 0.2306 | 0.2969 |
| `ajbc-ckba-jk` | 0.1336 | 0.1308 | 0.1984 |
| `ajbdc-ckbad-jk` | 1.2281 | 1.2332 | 1.4376 |
| `aqrs-pa-pqrs` | 0.0603 | 0.0846 | 0.1294 |
| `ij-ik-kj` | 0.7477 | 0.8012 | 0.8936 |
| `ij-ikl-ljk` | 0.4452 | 0.4426 | 0.5334 |
| `ij-kil-lkj` | 0.6861 | 0.6834 | 0.7406 |
| `ijk-ikl-lj` | 0.2526 | 0.2492 | 0.3462 |
| `ijk-il-jlk` | 0.2415 | 0.2395 | 0.3173 |
| `ijk-ilk-jl` | 0.2341 | 0.2314 | 0.3118 |
| `ijk-ilk-lj` | 0.2530 | 0.2479 | 0.3364 |
| `ijk-ilmk-mjl` | 0.1091 | 0.1067 | 0.1813 |
| `ijkl-imjn-lnkm` | 1.3702 | 1.3632 | 1.4887 |
| `ijkl-imjn-nlmk` | 1.3352 | 1.3318 | 1.4748 |
| `ijkl-imkn-jnlm` | 1.3405 | 1.3290 | 1.4484 |
| `ijkl-imkn-njml` | 1.1386 | 1.1181 | 1.2134 |
| `ijkl-imln-jnkm` | 0.9607 | 0.9730 | 1.0642 |
| `ijkl-imln-njmk` | 0.9651 | 0.9588 | 1.0567 |
| `ijkl-imnj-nlkm` | 0.9590 | 0.9626 | 1.0527 |
| `ijkl-imnk-njml` | 0.9684 | 0.9586 | 1.0617 |
| `ijkl-minj-nlmk` | 1.2013 | 1.1834 | 1.3253 |
| `ijkl-mink-jnlm` | 1.1711 | 1.1597 | 1.2667 |
| `ijkl-minl-njmk` | 1.1824 | 1.1752 | 1.2888 |
| **geomean** | 0.5733 | 0.5709 | 0.6865 |

## 1 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.0937 | 0.0929 | 0.2579 |
| `abcijk-eiab-jkec` | 0.5782 | 0.5481 | 0.5842 |
| `abcijk-eiac-jkeb` | 0.5338 | 0.4876 | 0.5789 |
| `abcijk-eibc-jkea` | 0.5718 | 0.5245 | 0.7281 |
| `abcijk-ejab-ikec` | 0.5556 | 0.5154 | 0.6139 |
| `abcijk-ejac-ikeb` | 0.5219 | 0.4556 | 0.5769 |
| `abcijk-ejbc-ikea` | 0.5854 | 0.5329 | 0.7270 |
| `abcijk-ekab-ijec` | 0.5324 | 0.5028 | 0.6123 |
| `abcijk-ekac-ijeb` | 0.5233 | 0.4708 | 0.5775 |
| `abcijk-ekbc-ijea` | 0.5532 | 0.5728 | 0.7361 |
| `abcijk-ijma-mkbc` | 0.5196 | 0.5284 | 0.7570 |
| `abcijk-ijmb-mkac` | 0.5045 | 0.4578 | 0.5877 |
| `abcijk-ijmc-mkab` | 0.5123 | 0.4852 | 0.6232 |
| `abcijk-ikma-mjbc` | 0.5187 | 0.5102 | 0.7500 |
| `abcijk-ikmb-mjac` | 0.5097 | 0.4523 | 0.5943 |
| `abcijk-ikmc-mjab` | 0.5458 | 0.4987 | 0.5973 |
| `abcijk-jkma-mibc` | 0.5446 | 0.5064 | 0.7367 |
| `abcijk-jkmb-miac` | 0.5197 | 0.5060 | 0.5946 |
| `abcijk-jkmc-miab` | 0.5438 | 0.5333 | 0.5909 |
| `abcs-rc-abrs` | 0.0570 | 0.0562 | 0.1397 |
| `abj-bka-kj` | 0.1600 | 0.1592 | 0.2542 |
| `abjc-cbka-kj` | 0.1011 | 0.0975 | 0.2322 |
| `abjc-kbac-jk` | 0.0631 | 0.0608 | 0.1580 |
| `abjcd-dkbac-jk` | 1.0621 | 0.9785 | 1.1637 |
| `abrs-qb-aqrs` | 0.0567 | 0.0543 | 0.1332 |
| `adbjc-cbdka-kj` | 2.8893 | 3.0035 | 3.2756 |
| `ajb-kba-jk` | 0.1290 | 0.1297 | 0.2502 |
| `ajbc-ckba-jk` | 0.0891 | 0.0847 | 0.2095 |
| `ajbdc-ckbad-jk` | 0.9442 | 0.9415 | 1.1014 |
| `aqrs-pa-pqrs` | 0.0371 | 0.0511 | 0.1255 |
| `ij-ik-kj` | 0.4442 | 0.4254 | 0.6074 |
| `ij-ikl-ljk` | 0.3151 | 0.3109 | 0.4159 |
| `ij-kil-lkj` | 0.4519 | 0.4504 | 0.5611 |
| `ijk-ikl-lj` | 0.1413 | 0.1376 | 0.2602 |
| `ijk-il-jlk` | 0.1353 | 0.1283 | 0.2201 |
| `ijk-ilk-jl` | 0.1296 | 0.1288 | 0.3631 |
| `ijk-ilk-lj` | 0.1406 | 0.1401 | 0.2618 |
| `ijk-ilmk-mjl` | 0.0784 | 0.0773 | 0.2095 |
| `ijkl-imjn-lnkm` | 0.8523 | 0.8480 | 0.9723 |
| `ijkl-imjn-nlmk` | 0.8306 | 0.8272 | 0.9646 |
| `ijkl-imkn-jnlm` | 0.8534 | 0.8272 | 0.9586 |
| `ijkl-imkn-njml` | 0.8325 | 0.8230 | 0.9531 |
| `ijkl-imln-jnkm` | 0.8305 | 0.8243 | 0.9559 |
| `ijkl-imln-njmk` | 0.7872 | 0.7798 | 0.9098 |
| `ijkl-imnj-nlkm` | 0.7397 | 0.7133 | 0.8289 |
| `ijkl-imnk-njml` | 0.6489 | 0.6405 | 0.7346 |
| `ijkl-minj-nlmk` | 0.7484 | 0.7301 | 0.8524 |
| `ijkl-mink-jnlm` | 0.7209 | 0.7090 | 0.8165 |
| `ijkl-minl-njmk` | 0.7560 | 0.7271 | 0.8382 |
| **geomean** | 0.3687 | 0.3582 | 0.5234 |

## 1 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 2.4890 | 2.5196 | 2.7199 |
| `abcijk-eiab-jkec` | 10.8606 | 10.8939 | 11.2196 |
| `abcijk-eiac-jkeb` | 10.6491 | 10.6786 | 10.8590 |
| `abcijk-eibc-jkea` | 11.0690 | 10.9805 | 11.2934 |
| `abcijk-ejab-ikec` | 10.8313 | 10.8055 | 11.1113 |
| `abcijk-ejac-ikeb` | 10.6538 | 10.6886 | 10.8850 |
| `abcijk-ejbc-ikea` | 11.0515 | 10.9369 | 11.2094 |
| `abcijk-ekab-ijec` | 10.8319 | 10.7934 | 11.0595 |
| `abcijk-ekac-ijeb` | 10.6785 | 10.7141 | 10.8812 |
| `abcijk-ekbc-ijea` | 11.0543 | 10.9231 | 11.2090 |
| `abcijk-ijma-mkbc` | 11.0640 | 10.9598 | 11.2059 |
| `abcijk-ijmb-mkac` | 10.6666 | 10.6833 | 10.8791 |
| `abcijk-ijmc-mkab` | 10.7030 | 10.7494 | 11.0297 |
| `abcijk-ikma-mjbc` | 11.0478 | 11.0624 | 11.2396 |
| `abcijk-ikmb-mjac` | 10.6461 | 10.7075 | 10.8804 |
| `abcijk-ikmc-mjab` | 10.7498 | 10.7702 | 11.0470 |
| `abcijk-jkma-mibc` | 11.0381 | 10.9045 | 11.3387 |
| `abcijk-jkmb-miac` | 10.6892 | 10.6923 | 10.8062 |
| `abcijk-jkmc-miab` | 10.8728 | 10.8589 | 11.1971 |
| `abcs-rc-abrs` | 1.1730 | 1.1762 | 1.1619 |
| `abj-bka-kj` | 4.0104 | 3.9468 | 3.9948 |
| `abjc-cbka-kj` | 1.9438 | 1.8814 | 1.9329 |
| `abjc-kbac-jk` | 1.2462 | 1.2438 | 1.2952 |
| `abjcd-dkbac-jk` | 8.5278 | 8.5986 | 9.0189 |
| `abrs-qb-aqrs` | 0.9934 | 1.0560 | 1.0300 |
| `adbjc-cbdka-kj` | 20.2404 | 20.3995 | 20.7556 |
| `ajb-kba-jk` | 3.5431 | 3.6218 | 3.7128 |
| `ajbc-ckba-jk` | 1.5794 | 1.5272 | 1.5357 |
| `ajbdc-ckbad-jk` | 8.6713 | 8.5022 | 8.9673 |
| `aqrs-pa-pqrs` | 1.2610 | 1.2651 | 1.3252 |
| `ij-ik-kj` | 12.2782 | 12.3224 | 12.4633 |
| `ij-ikl-ljk` | 4.1469 | 4.1475 | 4.2487 |
| `ij-kil-lkj` | 6.4502 | 6.3996 | 6.5426 |
| `ijk-ikl-lj` | 3.5134 | 3.4786 | 3.3864 |
| `ijk-il-jlk` | 3.0462 | 2.9401 | 2.8607 |
| `ijk-ilk-jl` | 2.4866 | 2.5238 | 2.6082 |
| `ijk-ilk-lj` | 2.6350 | 2.6405 | 2.6663 |
| `ijk-ilmk-mjl` | 0.9873 | 0.9848 | 1.0069 |
| `ijkl-imjn-lnkm` | 15.2587 | 15.2731 | 15.5082 |
| `ijkl-imjn-nlmk` | 15.2469 | 15.2493 | 15.4820 |
| `ijkl-imkn-jnlm` | 15.3362 | 15.2519 | 15.4835 |
| `ijkl-imkn-njml` | 15.2852 | 15.2352 | 15.4883 |
| `ijkl-imln-jnkm` | 15.2189 | 15.1799 | 15.4352 |
| `ijkl-imln-njmk` | 15.2210 | 15.2082 | 15.4314 |
| `ijkl-imnj-nlkm` | 15.2667 | 15.1820 | 15.3557 |
| `ijkl-imnk-njml` | 15.2548 | 15.2022 | 15.4151 |
| `ijkl-minj-nlmk` | 18.8568 | 18.8519 | 19.1399 |
| `ijkl-mink-jnlm` | 18.4093 | 18.4129 | 18.6310 |
| `ijkl-minl-njmk` | 18.8513 | 18.8287 | 19.3047 |
| **geomean** | 7.1115 | 7.1006 | 7.2421 |

## 1 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.6355 | 0.6388 | 0.6916 |
| `abcijk-eiab-jkec` | 2.8205 | 2.8842 | 3.0924 |
| `abcijk-eiac-jkeb` | 2.6887 | 2.6988 | 2.8928 |
| `abcijk-eibc-jkea` | 2.8063 | 2.8330 | 3.0177 |
| `abcijk-ejab-ikec` | 2.7671 | 2.7828 | 2.9588 |
| `abcijk-ejac-ikeb` | 2.6984 | 2.6865 | 2.8814 |
| `abcijk-ejbc-ikea` | 2.7747 | 3.2424 | 3.0558 |
| `abcijk-ekab-ijec` | 2.7649 | 2.7824 | 2.9658 |
| `abcijk-ekac-ijeb` | 2.6967 | 2.6879 | 2.8594 |
| `abcijk-ekbc-ijea` | 2.7832 | 2.9136 | 3.0105 |
| `abcijk-ijma-mkbc` | 2.8157 | 2.9137 | 3.0416 |
| `abcijk-ijmb-mkac` | 2.7047 | 2.6866 | 2.8979 |
| `abcijk-ijmc-mkab` | 2.7335 | 2.7299 | 2.9628 |
| `abcijk-ikma-mjbc` | 2.7936 | 2.8125 | 3.0565 |
| `abcijk-ikmb-mjac` | 2.6964 | 2.6934 | 2.8572 |
| `abcijk-ikmc-mjab` | 2.7382 | 2.7595 | 2.9436 |
| `abcijk-jkma-mibc` | 2.7948 | 2.8314 | 3.0320 |
| `abcijk-jkmb-miac` | 2.7000 | 2.7124 | 2.9006 |
| `abcijk-jkmc-miab` | 2.8303 | 2.8453 | 3.0373 |
| `abcs-rc-abrs` | 0.2948 | 0.2947 | 0.3577 |
| `abj-bka-kj` | 1.0448 | 1.0122 | 1.1083 |
| `abjc-cbka-kj` | 0.5189 | 0.5042 | 0.5891 |
| `abjc-kbac-jk` | 0.3199 | 0.3161 | 0.3870 |
| `abjcd-dkbac-jk` | 3.1007 | 3.1000 | 3.2521 |
| `abrs-qb-aqrs` | 0.2567 | 0.2565 | 0.3260 |
| `adbjc-cbdka-kj` | 6.7357 | 6.6760 | 7.3644 |
| `ajb-kba-jk` | 0.9044 | 0.8982 | 0.9831 |
| `ajbc-ckba-jk` | 0.3761 | 0.3789 | 0.4633 |
| `ajbdc-ckbad-jk` | 3.0582 | 3.0692 | 3.2193 |
| `aqrs-pa-pqrs` | 0.3815 | 0.3841 | 0.4361 |
| `ij-ik-kj` | 3.1568 | 3.1431 | 3.2649 |
| `ij-ikl-ljk` | 1.7629 | 1.7747 | 1.8717 |
| `ij-kil-lkj` | 2.7847 | 2.6881 | 2.7255 |
| `ijk-ikl-lj` | 0.9200 | 0.9247 | 0.9813 |
| `ijk-il-jlk` | 1.7750 | 1.6234 | 1.6808 |
| `ijk-ilk-jl` | 0.8815 | 0.8907 | 0.9720 |
| `ijk-ilk-lj` | 0.9225 | 0.9131 | 0.9891 |
| `ijk-ilmk-mjl` | 0.4011 | 0.3880 | 0.4596 |
| `ijkl-imjn-lnkm` | 5.8709 | 5.8497 | 5.9959 |
| `ijkl-imjn-nlmk` | 5.7824 | 5.7883 | 5.8993 |
| `ijkl-imkn-jnlm` | 5.3932 | 5.3135 | 5.3484 |
| `ijkl-imkn-njml` | 4.5044 | 4.3293 | 4.2850 |
| `ijkl-imln-jnkm` | 4.1784 | 4.1686 | 4.3052 |
| `ijkl-imln-njmk` | 4.6663 | 4.1462 | 4.2711 |
| `ijkl-imnj-nlkm` | 4.1704 | 4.1431 | 4.2570 |
| `ijkl-imnk-njml` | 4.1423 | 4.1564 | 4.2418 |
| `ijkl-minj-nlmk` | 5.2153 | 5.1846 | 5.3218 |
| `ijkl-mink-jnlm` | 5.0352 | 7.5900 | 5.1618 |
| `ijkl-minl-njmk` | 5.1846 | 5.1416 | 5.2978 |
| **geomean** | 2.0482 | 2.0609 | 2.1897 |

## 1 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 0.3296 | 0.3284 | 0.5982 |
| `abcijk-eiab-jkec` | 1.6672 | 1.6521 | 1.9422 |
| `abcijk-eiac-jkeb` | 1.5570 | 1.5474 | 1.8558 |
| `abcijk-eibc-jkea` | 1.6131 | 1.6046 | 2.9315 |
| `abcijk-ejab-ikec` | 1.6919 | 1.6736 | 1.8627 |
| `abcijk-ejac-ikeb` | 1.5745 | 1.5569 | 1.9010 |
| `abcijk-ejbc-ikea` | 1.6171 | 1.5846 | 3.0300 |
| `abcijk-ekab-ijec` | 1.6696 | 1.6641 | 1.8647 |
| `abcijk-ekac-ijeb` | 1.5557 | 1.5292 | 1.9198 |
| `abcijk-ekbc-ijea` | 1.5954 | 1.5850 | 2.8971 |
| `abcijk-ijma-mkbc` | 1.5986 | 1.5898 | 2.7770 |
| `abcijk-ijmb-mkac` | 1.5671 | 1.5782 | 1.8586 |
| `abcijk-ijmc-mkab` | 1.6517 | 1.6478 | 1.9154 |
| `abcijk-ikma-mjbc` | 1.5954 | 1.6031 | 2.8625 |
| `abcijk-ikmb-mjac` | 1.5550 | 1.5378 | 1.9376 |
| `abcijk-ikmc-mjab` | 1.6751 | 1.6724 | 1.8659 |
| `abcijk-jkma-mibc` | 1.6048 | 1.6173 | 3.1115 |
| `abcijk-jkmb-miac` | 1.5609 | 1.5416 | 1.9183 |
| `abcijk-jkmc-miab` | 1.6784 | 1.6658 | 1.8788 |
| `abcs-rc-abrs` | 0.1577 | 0.1573 | 0.2622 |
| `abj-bka-kj` | 0.5241 | 0.5212 | 0.6340 |
| `abjc-cbka-kj` | 0.2692 | 0.2704 | 0.4079 |
| `abjc-kbac-jk` | 0.1650 | 0.1671 | 0.2676 |
| `abjcd-dkbac-jk` | 2.2380 | 2.2658 | 2.3945 |
| `abrs-qb-aqrs` | 0.1429 | 0.1395 | 0.2504 |
| `adbjc-cbdka-kj` | 4.1007 | 4.1076 | 4.2645 |
| `ajb-kba-jk` | 0.4544 | 0.4584 | 0.5576 |
| `ajbc-ckba-jk` | 0.2047 | 0.2053 | 0.8592 |
| `ajbdc-ckbad-jk` | 2.2013 | 2.2251 | 4.1909 |
| `aqrs-pa-pqrs` | 0.2162 | 0.2272 | 0.2874 |
| `ij-ik-kj` | 1.6117 | 1.6034 | 1.8066 |
| `ij-ikl-ljk` | 0.9838 | 0.9696 | 1.1408 |
| `ij-kil-lkj` | 1.4946 | 1.4812 | 1.6331 |
| `ijk-ikl-lj` | 0.4726 | 0.4869 | 0.5916 |
| `ijk-il-jlk` | 0.5088 | 0.5047 | 0.6135 |
| `ijk-ilk-jl` | 0.4662 | 0.4614 | 0.8220 |
| `ijk-ilk-lj` | 0.4772 | 0.4801 | 0.5908 |
| `ijk-ilmk-mjl` | 0.2179 | 0.2237 | 0.3299 |
| `ijkl-imjn-lnkm` | 3.0196 | 3.0267 | 3.1522 |
| `ijkl-imjn-nlmk` | 2.9552 | 2.9671 | 3.1057 |
| `ijkl-imkn-jnlm` | 2.9453 | 2.9520 | 3.1455 |
| `ijkl-imkn-njml` | 3.1062 | 2.9132 | 3.1099 |
| `ijkl-imln-jnkm` | 2.8862 | 2.8920 | 3.0938 |
| `ijkl-imln-njmk` | 2.7181 | 2.6437 | 2.7853 |
| `ijkl-imnj-nlkm` | 2.4763 | 2.4217 | 2.5431 |
| `ijkl-imnk-njml` | 2.1939 | 2.1488 | 2.2708 |
| `ijkl-minj-nlmk` | 2.6690 | 2.6612 | 2.8170 |
| `ijkl-mink-jnlm` | 2.5928 | 2.5740 | 2.7509 |
| `ijkl-minl-njmk` | 2.6508 | 2.6292 | 2.7918 |
| **geomean** | 1.1420 | 1.1380 | 1.5008 |

## 16 MiB, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 14.8944 | 14.8791 | 15.4682 |
| `abcijk-eiab-jkec` | 14.8513 | 14.8741 | 15.5036 |
| `abcijk-eiac-jkeb` | 14.0571 | 14.1194 | 16.0277 |
| `abcijk-eibc-jkea` | 13.8404 | 13.7591 | 15.2483 |
| `abcijk-ejab-ikec` | 14.7996 | 14.7358 | 15.4867 |
| `abcijk-ejac-ikeb` | 13.9553 | 14.1308 | 15.8123 |
| `abcijk-ejbc-ikea` | 13.8941 | 13.9218 | 15.2176 |
| `abcijk-ekab-ijec` | 14.7973 | 14.7672 | 15.5256 |
| `abcijk-ekac-ijeb` | 13.9632 | 14.0048 | 15.7917 |
| `abcijk-ekbc-ijea` | 13.8862 | 13.8908 | 15.2993 |
| `abcijk-ijma-mkbc` | 13.8431 | 13.9546 | 15.4128 |
| `abcijk-ijmb-mkac` | 13.9231 | 13.9281 | 15.6897 |
| `abcijk-ijmc-mkab` | 14.7737 | 14.7457 | 15.5375 |
| `abcijk-ikma-mjbc` | 13.9313 | 14.0114 | 15.2549 |
| `abcijk-ikmb-mjac` | 14.0088 | 14.0020 | 15.9316 |
| `abcijk-ikmc-mjab` | 14.7321 | 14.7820 | 15.5344 |
| `abcijk-jkma-mibc` | 13.7964 | 13.8692 | 15.3881 |
| `abcijk-jkmb-miac` | 13.9251 | 14.1570 | 15.7351 |
| `abcijk-jkmc-miab` | 14.8804 | 14.8199 | 15.6289 |
| `abcs-rc-abrs` | 8.8248 | 8.8456 | 9.1460 |
| `abj-bka-kj` | 20.0220 | 20.0186 | 20.7777 |
| `abjc-cbka-kj` | 34.7215 | 34.6579 | 35.8418 |
| `abjc-kbac-jk` | 12.4033 | 12.4900 | 12.9070 |
| `abjcd-dkbac-jk` | 17.3970 | 17.3484 | 19.8857 |
| `abrs-qb-aqrs` | 8.1921 | 8.1197 | 8.4451 |
| `adbjc-cbdka-kj` | 43.5910 | 43.3820 | 45.9368 |
| `ajb-kba-jk` | 18.1654 | 18.1427 | 18.6661 |
| `ajbc-ckba-jk` | 20.2271 | 20.1966 | 22.2530 |
| `ajbdc-ckbad-jk` | 17.0943 | 16.9593 | 19.9391 |
| `aqrs-pa-pqrs` | 7.4096 | 9.1559 | 10.6235 |
| `ij-ik-kj` | 170.5142 | 130.1194 | 132.5886 |
| `ij-ikl-ljk` | 17.7244 | 17.7018 | 18.3992 |
| `ij-kil-lkj` | 21.4052 | 21.4301 | 22.9139 |
| `ijk-ikl-lj` | 16.0560 | 16.0508 | 16.1818 |
| `ijk-il-jlk` | 16.3219 | 16.2878 | 18.9588 |
| `ijk-ilk-jl` | 15.0700 | 15.0151 | 15.5756 |
| `ijk-ilk-lj` | 15.1184 | 15.1156 | 15.5755 |
| `ijk-ilmk-mjl` | 7.5729 | 7.4977 | 7.5357 |
| `ijkl-imjn-lnkm` | 255.1497 | 254.9872 | 255.2841 |
| `ijkl-imjn-nlmk` | 255.7916 | 255.9064 | 255.6464 |
| `ijkl-imkn-jnlm` | 255.4318 | 255.4311 | 259.8292 |
| `ijkl-imkn-njml` | 254.7587 | 254.7569 | 258.6226 |
| `ijkl-imln-jnkm` | 254.3346 | 253.8829 | 259.4074 |
| `ijkl-imln-njmk` | 253.4732 | 253.6945 | 257.4454 |
| `ijkl-imnj-nlkm` | 255.8202 | 255.8827 | 255.3780 |
| `ijkl-imnk-njml` | 253.8168 | 254.4397 | 257.8453 |
| `ijkl-minj-nlmk` | 311.2578 | 311.0189 | 312.2133 |
| `ijkl-mink-jnlm` | 308.0366 | 308.0578 | 314.8303 |
| `ijkl-minl-njmk` | 305.2227 | 305.6872 | 316.8282 |
| **geomean** | 30.0911 | 30.0609 | 31.9121 |

## 16 MiB, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 3.8973 | 3.9016 | 4.1077 |
| `abcijk-eiab-jkec` | 5.2056 | 5.2647 | 4.9384 |
| `abcijk-eiac-jkeb` | 4.6992 | 4.6976 | 5.1685 |
| `abcijk-eibc-jkea` | 4.5282 | 4.4471 | 4.7965 |
| `abcijk-ejab-ikec` | 5.0308 | 4.9584 | 4.9030 |
| `abcijk-ejac-ikeb` | 4.6723 | 4.6851 | 4.9958 |
| `abcijk-ejbc-ikea` | 4.4509 | 4.4437 | 4.8163 |
| `abcijk-ekab-ijec` | 4.9466 | 4.9664 | 5.0272 |
| `abcijk-ekac-ijeb` | 4.6667 | 4.6735 | 5.0991 |
| `abcijk-ekbc-ijea` | 4.7342 | 4.4600 | 4.8368 |
| `abcijk-ijma-mkbc` | 4.4414 | 4.4706 | 4.8284 |
| `abcijk-ijmb-mkac` | 4.6807 | 4.8438 | 5.0525 |
| `abcijk-ijmc-mkab` | 5.0266 | 5.0038 | 4.9450 |
| `abcijk-ikma-mjbc` | 4.4249 | 4.4646 | 4.8086 |
| `abcijk-ikmb-mjac` | 4.6855 | 5.0153 | 4.9132 |
| `abcijk-ikmc-mjab` | 4.9530 | 4.9838 | 4.9494 |
| `abcijk-jkma-mibc` | 4.3903 | 4.4385 | 4.7487 |
| `abcijk-jkmb-miac` | 4.6907 | 4.6858 | 5.0252 |
| `abcijk-jkmc-miab` | 5.1352 | 5.1609 | 4.9506 |
| `abcs-rc-abrs` | 2.6199 | 2.5856 | 2.7762 |
| `abj-bka-kj` | 5.5291 | 5.4630 | 5.7886 |
| `abjc-cbka-kj` | 12.5713 | 12.6527 | 13.4066 |
| `abjc-kbac-jk` | 3.7291 | 3.7406 | 3.5675 |
| `abjcd-dkbac-jk` | 7.0844 | 7.0693 | 7.5101 |
| `abrs-qb-aqrs` | 2.3810 | 2.2303 | 2.3440 |
| `adbjc-cbdka-kj` | 13.6882 | 13.7666 | 14.0288 |
| `ajb-kba-jk` | 4.7959 | 5.1150 | 4.9641 |
| `ajbc-ckba-jk` | 7.5494 | 7.5918 | 8.0684 |
| `ajbdc-ckbad-jk` | 7.0289 | 7.0704 | 7.6256 |
| `aqrs-pa-pqrs` | 2.1907 | 2.7508 | 3.2866 |
| `ij-ik-kj` | 42.8986 | 47.8036 | 45.4173 |
| `ij-ikl-ljk` | 6.6010 | 6.2889 | 7.0859 |
| `ij-kil-lkj` | 7.7694 | 7.6749 | 8.2942 |
| `ijk-ikl-lj` | 4.2187 | 4.1622 | 4.3395 |
| `ijk-il-jlk` | 5.7875 | 5.7646 | 6.4130 |
| `ijk-ilk-jl` | 4.5661 | 4.0592 | 4.1001 |
| `ijk-ilk-lj` | 4.1553 | 4.1349 | 4.0996 |
| `ijk-ilmk-mjl` | 2.3547 | 2.3489 | 2.2648 |
| `ijkl-imjn-lnkm` | 66.9352 | 67.0429 | 67.1301 |
| `ijkl-imjn-nlmk` | 66.6868 | 66.5558 | 66.3923 |
| `ijkl-imkn-jnlm` | 64.8614 | 65.6954 | 67.5738 |
| `ijkl-imkn-njml` | 65.4245 | 65.6237 | 66.6403 |
| `ijkl-imln-jnkm` | 65.9856 | 65.3512 | 67.1525 |
| `ijkl-imln-njmk` | 65.4039 | 65.3898 | 66.5823 |
| `ijkl-imnj-nlkm` | 66.8085 | 66.8432 | 66.7113 |
| `ijkl-imnk-njml` | 65.5013 | 65.5783 | 66.8626 |
| `ijkl-minj-nlmk` | 79.8453 | 79.9580 | 80.1356 |
| `ijkl-mink-jnlm` | 78.6800 | 78.8386 | 81.8709 |
| `ijkl-minl-njmk` | 80.3233 | 80.3669 | 81.5613 |
| **geomean** | 9.2438 | 9.2822 | 9.6087 |

## 16 MiB, f64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 2.5014 | 2.1953 | 2.2762 |
| `abcijk-eiab-jkec` | 3.8719 | 3.9746 | 3.7689 |
| `abcijk-eiac-jkeb` | 3.6509 | 3.6306 | 3.8213 |
| `abcijk-eibc-jkea` | 3.7594 | 3.8112 | 3.8079 |
| `abcijk-ejab-ikec` | 3.8758 | 3.8861 | 3.8754 |
| `abcijk-ejac-ikeb` | 3.9947 | 3.6474 | 3.8241 |
| `abcijk-ejbc-ikea` | 3.8173 | 3.8826 | 3.8079 |
| `abcijk-ekab-ijec` | 3.8456 | 3.9351 | 3.7981 |
| `abcijk-ekac-ijeb` | 3.8712 | 3.6817 | 3.7769 |
| `abcijk-ekbc-ijea` | 3.8146 | 3.7558 | 3.8321 |
| `abcijk-ijma-mkbc` | 3.7435 | 5.0912 | 3.8040 |
| `abcijk-ijmb-mkac` | 3.6648 | 3.6336 | 3.8540 |
| `abcijk-ijmc-mkab` | 3.8385 | 4.1440 | 3.8191 |
| `abcijk-ikma-mjbc` | 4.0929 | 3.8142 | 3.7986 |
| `abcijk-ikmb-mjac` | 3.6310 | 3.6766 | 3.8217 |
| `abcijk-ikmc-mjab` | 3.8662 | 3.9160 | 3.9019 |
| `abcijk-jkma-mibc` | 3.7585 | 3.7741 | 3.7972 |
| `abcijk-jkmb-miac` | 3.6262 | 4.0094 | 3.8280 |
| `abcijk-jkmc-miab` | 3.8975 | 3.9335 | 3.7387 |
| `abcs-rc-abrs` | 2.0205 | 1.9906 | 2.4169 |
| `abj-bka-kj` | 4.0644 | 4.5519 | 4.4361 |
| `abjc-cbka-kj` | 8.2329 | 8.5416 | 8.6560 |
| `abjc-kbac-jk` | 2.4690 | 2.4191 | 2.5489 |
| `abjcd-dkbac-jk` | 4.5081 | 4.5271 | 4.7837 |
| `abrs-qb-aqrs` | 1.5692 | 1.5277 | 1.6141 |
| `adbjc-cbdka-kj` | 8.1516 | 8.2391 | 8.4938 |
| `ajb-kba-jk` | 2.7390 | 2.7177 | 2.8384 |
| `ajbc-ckba-jk` | 5.1317 | 5.1393 | 5.4469 |
| `ajbdc-ckbad-jk` | 4.4133 | 4.4423 | 4.7232 |
| `aqrs-pa-pqrs` | 1.5982 | 1.6987 | 2.0327 |
| `ij-ik-kj` | 21.9780 | 24.3952 | 25.0959 |
| `ij-ikl-ljk` | 3.5391 | 3.3054 | 3.5047 |
| `ij-kil-lkj` | 4.4322 | 4.4251 | 4.6015 |
| `ijk-ikl-lj` | 2.3214 | 2.4242 | 2.6395 |
| `ijk-il-jlk` | 2.5639 | 2.5146 | 3.0202 |
| `ijk-ilk-jl` | 2.1918 | 2.1779 | 2.3185 |
| `ijk-ilk-lj` | 2.2400 | 2.2269 | 2.3280 |
| `ijk-ilmk-mjl` | 1.7238 | 1.3160 | 1.4738 |
| `ijkl-imjn-lnkm` | 36.2205 | 36.1715 | 37.3360 |
| `ijkl-imjn-nlmk` | 36.2421 | 36.0887 | 36.8738 |
| `ijkl-imkn-jnlm` | 34.1928 | 34.2149 | 34.5467 |
| `ijkl-imkn-njml` | 34.2913 | 34.7388 | 34.9819 |
| `ijkl-imln-jnkm` | 33.7278 | 33.7405 | 34.6544 |
| `ijkl-imln-njmk` | 33.7334 | 33.7750 | 34.7118 |
| `ijkl-imnj-nlkm` | 36.3608 | 36.2854 | 37.2691 |
| `ijkl-imnk-njml` | 34.0395 | 34.2574 | 35.4932 |
| `ijkl-minj-nlmk` | 44.1087 | 44.1326 | 44.9820 |
| `ijkl-mink-jnlm` | 41.1165 | 41.0639 | 41.9841 |
| `ijkl-minl-njmk` | 42.0857 | 42.0863 | 43.2962 |
| **geomean** | 6.0465 | 6.0696 | 6.2304 |

## 16 MiB, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 57.4086 | 57.3945 | 57.7049 |
| `abcijk-eiab-jkec` | 54.3929 | 54.3641 | 56.3886 |
| `abcijk-eiac-jkeb` | 53.4793 | 53.4628 | 54.7096 |
| `abcijk-eibc-jkea` | 54.3957 | 54.4629 | 55.8828 |
| `abcijk-ejab-ikec` | 54.1285 | 54.0559 | 55.6493 |
| `abcijk-ejac-ikeb` | 53.4436 | 53.4936 | 54.7214 |
| `abcijk-ejbc-ikea` | 54.4392 | 54.4641 | 55.8076 |
| `abcijk-ekab-ijec` | 54.1286 | 54.1495 | 55.6247 |
| `abcijk-ekac-ijeb` | 53.3677 | 53.3460 | 54.8248 |
| `abcijk-ekbc-ijea` | 54.3071 | 54.3462 | 55.7708 |
| `abcijk-ijma-mkbc` | 54.3108 | 54.4073 | 55.6545 |
| `abcijk-ijmb-mkac` | 53.4915 | 53.4776 | 54.7792 |
| `abcijk-ijmc-mkab` | 54.1216 | 54.1913 | 55.7228 |
| `abcijk-ikma-mjbc` | 54.4876 | 54.4985 | 55.8877 |
| `abcijk-ikmb-mjac` | 53.4624 | 53.3430 | 54.8041 |
| `abcijk-ikmc-mjab` | 54.1393 | 54.1541 | 55.6295 |
| `abcijk-jkma-mibc` | 54.4514 | 54.4359 | 55.8699 |
| `abcijk-jkmb-miac` | 53.5228 | 53.4305 | 54.7861 |
| `abcijk-jkmc-miab` | 54.4281 | 54.4234 | 56.4578 |
| `abcs-rc-abrs` | 31.8884 | 31.7732 | 30.9497 |
| `abj-bka-kj` | 72.9438 | 73.1264 | 74.1086 |
| `abjc-cbka-kj` | 67.7211 | 67.5709 | 68.9954 |
| `abjc-kbac-jk` | 39.0234 | 38.8952 | 39.4068 |
| `abjcd-dkbac-jk` | 43.1251 | 43.0992 | 44.8759 |
| `abrs-qb-aqrs` | 33.4109 | 33.3971 | 32.5923 |
| `adbjc-cbdka-kj` | 69.4561 | 69.4290 | 76.4146 |
| `ajb-kba-jk` | 64.3170 | 64.3268 | 64.8874 |
| `ajbc-ckba-jk` | 50.7931 | 50.8092 | 52.8475 |
| `ajbdc-ckbad-jk` | 42.8026 | 42.8037 | 44.2613 |
| `aqrs-pa-pqrs` | 31.0397 | 31.1014 | 33.2536 |
| `ij-ik-kj` | 509.3213 | 509.8789 | 519.9161 |
| `ij-ikl-ljk` | 64.9033 | 65.0915 | 66.9225 |
| `ij-kil-lkj` | 76.1569 | 76.2296 | 78.9008 |
| `ijk-ikl-lj` | 59.7332 | 59.8681 | 59.9154 |
| `ijk-il-jlk` | 57.9663 | 57.9253 | 58.5897 |
| `ijk-ilk-jl` | 57.3229 | 57.3267 | 57.7080 |
| `ijk-ilk-lj` | 59.2021 | 59.2110 | 59.5863 |
| `ijk-ilmk-mjl` | 30.9082 | 30.7466 | 30.2229 |
| `ijkl-imjn-lnkm` | 975.7664 | 975.7020 | 994.1717 |
| `ijkl-imjn-nlmk` | 980.4920 | 980.3429 | 997.7795 |
| `ijkl-imkn-jnlm` | 981.2617 | 982.2378 | 989.7108 |
| `ijkl-imkn-njml` | 984.2934 | 983.4490 | 992.4027 |
| `ijkl-imln-jnkm` | 980.1208 | 979.3929 | 986.7536 |
| `ijkl-imln-njmk` | 982.2054 | 982.1862 | 989.2283 |
| `ijkl-imnj-nlkm` | 979.5272 | 978.3232 | 996.6473 |
| `ijkl-imnk-njml` | 983.1306 | 982.4951 | 992.0047 |
| `ijkl-minj-nlmk` | 1182.6648 | 1183.0849 | 1207.3664 |
| `ijkl-mink-jnlm` | 1181.1825 | 1181.0390 | 1194.3427 |
| `ijkl-minl-njmk` | 1186.6507 | 1184.7766 | 1199.3377 |
| **geomean** | 107.2313 | 107.2131 | 109.4211 |

## 16 MiB, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 14.5761 | 14.6333 | 14.7501 |
| `abcijk-eiab-jkec` | 14.0966 | 14.0884 | 14.7597 |
| `abcijk-eiac-jkeb` | 13.6951 | 13.6129 | 13.9931 |
| `abcijk-eibc-jkea` | 13.8524 | 13.9396 | 14.1913 |
| `abcijk-ejab-ikec` | 13.8774 | 13.8618 | 14.3238 |
| `abcijk-ejac-ikeb` | 13.5917 | 13.5869 | 13.9948 |
| `abcijk-ejbc-ikea` | 13.8953 | 13.8697 | 14.1259 |
| `abcijk-ekab-ijec` | 13.8774 | 13.8983 | 14.3410 |
| `abcijk-ekac-ijeb` | 13.5822 | 13.4997 | 14.0223 |
| `abcijk-ekbc-ijea` | 13.8440 | 13.8723 | 14.2158 |
| `abcijk-ijma-mkbc` | 13.8336 | 13.8938 | 14.1435 |
| `abcijk-ijmb-mkac` | 13.5813 | 13.5899 | 13.9484 |
| `abcijk-ijmc-mkab` | 13.8454 | 13.8524 | 14.2026 |
| `abcijk-ikma-mjbc` | 13.8719 | 13.8988 | 14.1651 |
| `abcijk-ikmb-mjac` | 13.6053 | 13.6467 | 14.0824 |
| `abcijk-ikmc-mjab` | 13.8601 | 13.9229 | 14.3173 |
| `abcijk-jkma-mibc` | 13.9221 | 13.8412 | 14.1652 |
| `abcijk-jkmb-miac` | 13.6495 | 13.6597 | 14.0374 |
| `abcijk-jkmc-miab` | 14.0896 | 14.0945 | 14.7658 |
| `abcs-rc-abrs` | 8.3251 | 8.3280 | 8.0148 |
| `abj-bka-kj` | 18.8808 | 18.9308 | 19.3259 |
| `abjc-cbka-kj` | 19.8354 | 19.8971 | 20.3471 |
| `abjc-kbac-jk` | 10.0216 | 10.4617 | 10.7112 |
| `abjcd-dkbac-jk` | 13.3680 | 13.2302 | 13.7701 |
| `abrs-qb-aqrs` | 8.4624 | 8.5002 | 8.3400 |
| `adbjc-cbdka-kj` | 20.6656 | 21.1386 | 21.5150 |
| `ajb-kba-jk` | 16.4372 | 16.3739 | 16.5948 |
| `ajbc-ckba-jk` | 13.3008 | 13.2387 | 13.4778 |
| `ajbdc-ckbad-jk` | 12.8308 | 12.7975 | 13.2880 |
| `aqrs-pa-pqrs` | 8.1074 | 8.0724 | 8.6573 |
| `ij-ik-kj` | 128.5921 | 128.5526 | 131.9318 |
| `ij-ikl-ljk` | 22.7974 | 22.8056 | 23.3986 |
| `ij-kil-lkj` | 26.6291 | 26.4711 | 27.0854 |
| `ijk-ikl-lj` | 15.2038 | 15.2689 | 15.2790 |
| `ijk-il-jlk` | 19.7551 | 19.7222 | 20.0119 |
| `ijk-ilk-jl` | 14.7857 | 14.5926 | 14.6742 |
| `ijk-ilk-lj` | 15.0302 | 15.0389 | 15.1839 |
| `ijk-ilmk-mjl` | 8.3824 | 8.3650 | 8.1026 |
| `ijkl-imjn-lnkm` | 249.1067 | 249.6559 | 255.8896 |
| `ijkl-imjn-nlmk` | 248.7598 | 248.5896 | 254.3451 |
| `ijkl-imkn-jnlm` | 247.7915 | 247.6859 | 251.2756 |
| `ijkl-imkn-njml` | 248.8843 | 248.4700 | 252.1732 |
| `ijkl-imln-jnkm` | 246.9636 | 246.9410 | 250.1629 |
| `ijkl-imln-njmk` | 247.9994 | 248.4913 | 251.4354 |
| `ijkl-imnj-nlkm` | 248.4989 | 248.3824 | 254.2088 |
| `ijkl-imnk-njml` | 248.8649 | 248.6625 | 252.0537 |
| `ijkl-minj-nlmk` | 299.9384 | 299.7031 | 305.7494 |
| `ijkl-mink-jnlm` | 297.9260 | 297.9434 | 301.9826 |
| `ijkl-minl-njmk` | 299.3450 | 299.3555 | 302.5554 |
| **geomean** | 28.2966 | 28.3196 | 28.8914 |

## 16 MiB, c64, 8T (CPU 4-11)

| case | plan (ms) | packed (ms) | upstream (ms) |
|---|---|---|---|
| `abc-bk-akc` | 7.7158 | 7.6373 | 7.6332 |
| `abcijk-eiab-jkec` | 9.0178 | 9.1016 | 9.1204 |
| `abcijk-eiac-jkeb` | 8.3332 | 8.2909 | 9.1618 |
| `abcijk-eibc-jkea` | 8.3727 | 8.3209 | 9.8999 |
| `abcijk-ejab-ikec` | 8.9601 | 9.0708 | 8.9614 |
| `abcijk-ejac-ikeb` | 8.3681 | 8.3032 | 8.6384 |
| `abcijk-ejbc-ikea` | 8.3345 | 8.3609 | 10.1710 |
| `abcijk-ekab-ijec` | 8.9276 | 9.0526 | 8.5084 |
| `abcijk-ekac-ijeb` | 8.3548 | 8.3041 | 9.3909 |
| `abcijk-ekbc-ijea` | 8.3721 | 8.4429 | 10.1981 |
| `abcijk-ijma-mkbc` | 8.3357 | 8.2866 | 10.0169 |
| `abcijk-ijmb-mkac` | 8.3079 | 8.3406 | 8.5954 |
| `abcijk-ijmc-mkab` | 8.8588 | 9.0323 | 8.8998 |
| `abcijk-ikma-mjbc` | 8.4224 | 8.3820 | 9.9961 |
| `abcijk-ikmb-mjac` | 8.2860 | 8.3349 | 8.5725 |
| `abcijk-ikmc-mjab` | 9.0584 | 9.0469 | 9.0495 |
| `abcijk-jkma-mibc` | 8.3992 | 8.3287 | 10.0137 |
| `abcijk-jkmb-miac` | 8.2887 | 8.3328 | 9.1101 |
| `abcijk-jkmc-miab` | 8.9953 | 8.9842 | 9.0504 |
| `abcs-rc-abrs` | 4.6618 | 4.6525 | 4.9108 |
| `abj-bka-kj` | 10.9814 | 10.5521 | 10.8211 |
| `abjc-cbka-kj` | 12.1482 | 12.3364 | 12.1161 |
| `abjc-kbac-jk` | 5.8542 | 5.8387 | 7.6224 |
| `abjcd-dkbac-jk` | 8.8394 | 8.7242 | 8.8849 |
| `abrs-qb-aqrs` | 4.5813 | 4.5816 | 4.6162 |
| `adbjc-cbdka-kj` | 13.4864 | 13.0437 | 13.4368 |
| `ajb-kba-jk` | 8.5890 | 9.0485 | 8.7332 |
| `ajbc-ckba-jk` | 8.5787 | 8.4774 | 36.1858 |
| `ajbdc-ckbad-jk` | 8.3682 | 8.3345 | 27.1458 |
| `aqrs-pa-pqrs` | 4.3974 | 4.4367 | 4.6752 |
| `ij-ik-kj` | 70.8020 | 70.6056 | 74.1333 |
| `ij-ikl-ljk` | 16.0366 | 16.1249 | 16.5791 |
| `ij-kil-lkj` | 18.5311 | 18.5823 | 19.0402 |
| `ijk-ikl-lj` | 7.8594 | 7.8915 | 7.9063 |
| `ijk-il-jlk` | 13.7205 | 13.6327 | 13.8687 |
| `ijk-ilk-jl` | 7.8865 | 7.5042 | 7.6473 |
| `ijk-ilk-lj` | 7.7570 | 7.7591 | 7.8820 |
| `ijk-ilmk-mjl` | 4.9396 | 4.4549 | 4.7098 |
| `ijkl-imjn-lnkm` | 131.1945 | 131.2475 | 137.0725 |
| `ijkl-imjn-nlmk` | 130.1921 | 131.3453 | 135.6810 |
| `ijkl-imkn-jnlm` | 130.6320 | 130.6836 | 134.5705 |
| `ijkl-imkn-njml` | 132.0940 | 130.9742 | 134.2784 |
| `ijkl-imln-jnkm` | 128.5145 | 128.8871 | 132.1873 |
| `ijkl-imln-njmk` | 130.4530 | 130.4038 | 134.1353 |
| `ijkl-imnj-nlkm` | 130.4227 | 130.0280 | 135.5525 |
| `ijkl-imnk-njml` | 131.0104 | 131.2140 | 134.2337 |
| `ijkl-minj-nlmk` | 157.2871 | 157.2774 | 161.7324 |
| `ijkl-mink-jnlm` | 154.8423 | 154.4885 | 157.8869 |
| `ijkl-minl-njmk` | 155.8306 | 155.3959 | 158.8992 |
| **geomean** | 16.5619 | 16.5084 | 18.2822 |
