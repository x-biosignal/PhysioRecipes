# eeg-pli-alpha-eegmmidb

- alpha-band (8-13 Hz) phase-lag index between occipital O1 and Oz -- volume-conduction-robust coupling (far below the PLV) (0.016)
- max |phaseLagIndex - scipy Hilbert-band PLI| (agreement; PLI is sign-sensitive near zero-lag) (4e-03)
- |op PLI - |mean(sign(sin(phase_diff)))|| -- the PLI sign formula, exact given the phases (0)
- PLV of constructed ZERO-LAG (common-source) signals -- PLV counts volume conduction, so it is high (0.99)
- PLI of the SAME zero-lag signals -- PLI correctly DISCOUNTS volume conduction, so it is ~0 (0.01)
- PLI of constructed LAGGED (pi/4-offset) signals -- genuine non-zero-lag coupling, PLI ~ 1 (1.0)
