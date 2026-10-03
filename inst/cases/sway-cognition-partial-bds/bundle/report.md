# sway-cognition-partial-bds

- rank (Spearman) partial correlation of sway and TMT-A controlling for age (0.201)
- -log10(two-sided p) of the age-adjusted association: still significant (1.93)
- degrees of freedom (n - 2 - k, one covariate) (155)
- |partialCorrelation - ppcor::pcor.test| (machine precision, < 1e-9) (<1e-9)
- |partialCorrelation - closed-form recompute| (machine precision, < 1e-9) (<1e-9)
- linear (Pearson) partial correlation controlling for age -- vanishes (0.048)
- p of the linear partial correlation (non-significant) (0.55)
- marginal (unadjusted) Spearman rho of sway and TMT-A (0.532)
- the partial correlation is attenuated relative to the marginal (age accounts for much of the link) (yes)
- subjects with sway, TMT-A and age (complete triples) (158)
