# gait-grf-variance-levene-gaitrec

- Levene (Brown-Forsythe) F-statistic for variance homogeneity across the five classes (3.42)
- -log10(Levene p): the class variances differ significantly (2.06)
- between-groups degrees of freedom (k - 1) (4)
- within-groups degrees of freedom (N - k) (1839)
- |leveneTest F - scipy.stats.levene F| (machine precision, < 1e-9) (<1e-9)
- |leveneTest F - car::leveneTest F| (machine precision, < 1e-9) (<1e-9)
- classical Bartlett-test p (normality-sensitive): non-significant, for contrast (0.079)
- the robust Levene test finds the class variances differ (p < 0.05) (yes)
- Levene and Bartlett disagree (Bartlett ns while Levene significant) (yes)
- total subjects across the five classes (1844)
