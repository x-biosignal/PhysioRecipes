# gait-grf-anova-pathology-gaitrec

- one-way ANOVA omnibus F-statistic of the vertical-GRF dynamic range across the five gait classes (73.4)
- -log10(omnibus p): the group difference is overwhelmingly significant (57.0)
- between-groups degrees of freedom (k - 1) (4)
- within-groups degrees of freedom (N - k) (1839)
- |oneWayAnova F - scipy.stats.f_oneway F| (machine precision; multi-group SS accumulation diverges at the last ULP) (<1e-9)
- |oneWayAnova F - base R oneway.test(var.equal=TRUE) F| (bit-for-bit) (0)
- mean healthy-control dynamic range / mean pooled-pathology dynamic range (the effect size) (1.65)
- healthy controls have a larger vGRF dynamic range than the pooled pathology classes (group means) (yes)
- total subjects across the five classes (1844)
- number of gait classes compared (5)
