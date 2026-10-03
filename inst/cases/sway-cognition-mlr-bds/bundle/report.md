# sway-cognition-mlr-bds

- OLS coefficient of age (cm of sway per year, adjusted for TMT-A) (1.59)
- -log10(p) of the age coefficient: highly significant (7.7)
- OLS coefficient of TMT-A (adjusted for age) (0.12)
- p of the TMT-A coefficient (non-significant; equals the partial-correlation p) (0.55)
- model R-squared: fraction of sway variance explained by age + TMT-A (0.276)
- -log10 of the overall model F-test p-value (10.9)
- max |multipleRegression coef - base R lm coef| (bit-for-bit) (0)
- max |multipleRegression coef - statsmodels OLS coef| (machine precision) (<1e-9)
- age is significant (p<0.001) and TMT-A is not (p>0.05) in the joint model (yes)
- subjects in the regression (complete cases) (158)
