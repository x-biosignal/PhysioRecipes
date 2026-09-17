# eeg-wpli-alpha-eegmmidb

- alpha-band (8-13 Hz) weighted phase-lag index (biased) between occipital O1 and Oz (0.11)
- the DEBIASED wPLI (Vinck 2011 Eq. 6) -- low, confirming the O1-Oz alpha coupling is mostly volume conduction (0.011)
- max |weightedPLI - scipy imaginary-cross-spectrum wPLI| (agreement, filtfilt-limited) (7e-03)
- biased wPLI of INDEPENDENT signals -- spuriously positive (the finite-sample bias) (0.038)
- DEBIASED wPLI of the SAME independent signals -- corrected to ~0 (the bias removed) (0.001)
- debiased wPLI of constructed LAGGED signals -- genuine coupling survives debiasing (~1) (1.0)
