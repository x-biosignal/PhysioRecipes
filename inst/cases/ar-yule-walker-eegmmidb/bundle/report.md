# ar-yule-walker-eegmmidb

- first AR coefficient (lag 1) of the AR(4) Yule-Walker fit (1.18)
- second AR coefficient (lag 2) -- negative (oscillatory dynamics) (-0.29)
- innovation (one-step prediction) variance of the AR fit (348.5)
- max |AR coefficient - statsmodels yule_walker(mle)| (bit-exact) (5e-15)
- |innovation variance - statsmodels variance| (bit-exact) (5e-13)
- the fitted AR(4) is stationary (all roots outside the unit circle; 1 = holds) (yes)
