# hrv-lomb-fantasia

- Lomb-Scargle LF-band power (0.04-0.15 Hz) of the real RR tachogram (ms^2) (920)
- Lomb-Scargle HF-band power (0.15-0.4 Hz) -- respiratory/vagal (ms^2) (1915)
- LF/HF ratio -- the sympatho-vagal balance (HF-dominant when < 1) (0.48)
- HF power in normalized units (100*HF/(LF+HF)) -- vagal fraction (%) (67.6)
- max |ecgHRVfreq Lomb periodogram - scipy.signal.lombscargle| (machine precision, rel ~1e-10) (5e-08)
- max |op band power - scipy-integrated band power| over VLF/LF/HF (machine precision) (3e-11)
