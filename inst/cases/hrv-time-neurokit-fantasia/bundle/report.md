# hrv-time-neurokit-fantasia

- mean NN interval (MeanNN), reproducing NeuroKit2 hrv_time bit-for-bit (765.9 ms)
- SDNN (sd of NN intervals) -- reproduces NeuroKit2 bit-for-bit (73.7 ms)
- RMSSD (root-mean-square of successive differences) -- reproduces NeuroKit2 bit-for-bit (81.5 ms)
- max |ecgHRVtime - NeuroKit2 hrv_time| over MeanNN, SDNN, RMSSD (bit-exact) (0)
- pNN50 gap vs NeuroKit2 -- the ONLY divergence, a documented denominator convention (N-1 vs N) (0.10 pt)
- nn50 count (successive |diff| > 50 ms) -- IDENTICAL in both tools, proving the pNN50 gap is denominator-only (146)
