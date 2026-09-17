# pacf-eegmmidb

- partial autocorrelation at lag 1 -- equals the lag-1 autocorrelation (0.86)
- partial autocorrelation at lag 2 -- strongly negative (oscillatory AR(2)-like alpha structure) (-0.63)
- partial autocorrelation at lag 0 -- 1 by convention (1)
- max |partialAutocorrelation - statsmodels.tsa.pacf(ldb)| over lags (bit-exact) (6e-15)
- |PACF(lag 1) - ACF(lag 1)| -- the definitional identity (~0) (0)
- number of PACF values returned (lags 0..lag_max) (21)
