# gait-pushoff-age-regression-gaitrec

- OLS slope of push-off peak on age (BW per year; negative = decline) (-0.00120)
- push-off decline per decade of age (BW) (-0.012)
- OLS intercept (modelled push-off at age 0, extrapolated) (1.144)
- R-squared: fraction of push-off variance explained by age (0.094)
- -log10(two-sided slope p): the age effect is highly significant (5.2)
- residual degrees of freedom (n - 2) (206)
- |linearRegression slope - scipy.stats.linregress slope| (bit-for-bit) (0)
- |linearRegression slope - base R lm slope| (machine precision, < 1e-9) (<1e-9)
- the slope is negative (push-off peak declines with age) (yes)
- healthy-control subjects regressed (208)
