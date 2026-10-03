# median-abs-dev-eegmmidb

- median absolute deviation (raw, constant=1) of the POz channel -- robust dispersion (33)
- |medianAbsDev - scipy.stats.median_abs_deviation| (bit-exact) (0)
- |medianAbsDev - base R mad(constant=1)| (bit-exact) (0)
- normal-consistent robust SD estimate (MAD x 1/qnorm(0.75)) (48.93)
- classical population standard deviation (from signalMoments) (48.83)
- robust MAD-scale / classical SD -- near 1 for clean near-Gaussian data (1.002)
- samples in the analyzed channel (10 s at 160 Hz) (1600)
