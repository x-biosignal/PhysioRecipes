# eeg-plv-alpha-eegmmidb

- alpha-band (8-13 Hz) phase-locking value between occipital O1 and Oz -- posterior alpha phase synchronization (0.92)
- the same PLV re-computed by an independent scipy Hilbert-band pipeline (0.92)
- max |phaseLockingValue - scipy Hilbert-band PLV| (phase-robust agreement, up to the filtfilt convention) (8e-05)
- |op PLV - |mean(exp(i*phase_diff))|| -- the PLV summation formula, exact given the phases (0)
- PLV of constructed phase-locked signals (fixed offset) -- ground-truth recovery, near 1 (0.995)
- PLV of constructed independent (drifting-phase) signals -- ground-truth recovery, near 0 (0.009)
