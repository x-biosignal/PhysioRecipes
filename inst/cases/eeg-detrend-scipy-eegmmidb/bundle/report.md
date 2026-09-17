# eeg-detrend-scipy-eegmmidb

- max |detrendSignal - scipy.signal.detrend| over the linear and constant types (bit-exact) (1e-12)
- the linear trend removed from Fpz (least-squares slope, uV/sample) (0.014)
- sub-1-Hz Welch power of the RAW Fpz signal (dominated by the drift) (1284)
- sub-1-Hz power after LINEAR detrend -- the trend's low-frequency leakage removed (59)
- sub-1-Hz power after CONSTANT (mean) detrend -- the trend's leakage remains (112)
- extra sub-1-Hz power removed by LINEAR vs CONSTANT detrend -- why the type matters (47%)
