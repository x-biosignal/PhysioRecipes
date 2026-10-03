# ecg-ppg-crosscorr-bidmc

- lag (samples) of the peak ECG-PPG cross-correlation within +/- 0.72 s (49)
- the peak lag in seconds -- the pulse arrival time (heart -> fingertip) (0.39)
- the peak normalized cross-correlation (negative: ECG QRS vs PPG pulse morphology) (-0.33)
- max |crossCorrelation - independent numpy normalized cross-correlation| over all lags (bit-exact) (3e-14)
- peak-lag magnitude from scipy.signal.correlate (within the matched window) -- agrees with the op (49)
- lags in the cross-correlation profile (2*max_lag + 1) (181)
