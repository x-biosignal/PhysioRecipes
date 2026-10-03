# sway-retest-icc-bds

- ICC(2,1): single-trial test-retest reliability of COP path length (0.83)
- ICC(2,k): reliability of the average of the 3 trials (0.93)
- ICC(1,1) (one-way random) for context (0.82)
- ICC(3,1) (two-way mixed, consistency) for context (0.84)
- max |intraclassCorrelation - pingouin.intraclass_corr| over the 6 forms (machine precision, < 1e-9) (<1e-9)
- max |intraclassCorrelation - psych::ICC(lmer=FALSE)| over the 6 forms (machine precision) (<1e-9)
- single-trial reliability is good (ICC(2,1) > 0.75) (yes)
- 3-trial-average reliability is excellent (ICC(2,k) > 0.9) (yes)
- subjects with 3 trials (163)
- repeated trials per subject (3)
