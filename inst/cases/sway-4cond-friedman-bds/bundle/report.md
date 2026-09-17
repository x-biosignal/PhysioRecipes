# sway-4cond-friedman-bds

- tie-corrected Friedman chi-square of COP path length across the four vision x surface conditions (420.1)
- -log10(omnibus p): the conditions differ overwhelmingly (90.0)
- Friedman degrees of freedom (k - 1) (3)
- |friedmanTest Q - scipy.stats.friedmanchisquare Q| (machine precision, < 1e-9) (<1e-9)
- |friedmanTest Q - base R friedman.test Q| (bit-for-bit) (0)
- mean rank of the Open-Firm condition (the best-balance condition, lowest rank) (1.31)
- mean rank of the Closed-Foam condition (the worst-balance condition, highest rank) (3.92)
- mean ranks increase monotonically Open-Firm < Closed-Firm < Open-Foam < Closed-Foam (yes)
- subjects with all four conditions (complete blocks) (158)
- number of quiet-standing conditions compared (4)
