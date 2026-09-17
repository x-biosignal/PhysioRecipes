# autocorrelation-eegmmidb

- autocorrelation at lag 1 of the POz signal (0.86)
- autocorrelation at lag 2 -- lower than lag 1 (decaying) (0.57)
- autocorrelation at lag 0 -- exactly 1 (the ACF identity) (1)
- max |autocorrelation - statsmodels.tsa.acf| over lags 0..30 (bit-exact) (2e-16)
- decorrelation time -- first lag where the ACF drops below 1/e (3 samples)
- number of ACF values returned (lags 0..lag_max) (31)
