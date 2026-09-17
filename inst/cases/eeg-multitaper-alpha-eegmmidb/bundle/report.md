# eeg-multitaper-alpha-eegmmidb

- dominant frequency of the multitaper spectrum -- the alpha rhythm (Hz) (10.5)
- fraction of 0-45 Hz multitaper power in the alpha band (8-13 Hz) (0.46)
- max |eegMultitaper DPSS tapers - scipy.signal.windows.dpss| (machine precision) (6e-14)
- max |eegMultitaper PSD - independent scipy+numpy multitaper reconstruction| (machine precision) (1e-10)
- correlation of the multitaper PSD with MNE psd_array_multitaper (structure, up to the one-sided factor-of-2) (0.99)
- number of DPSS tapers averaged (2*NW-1 for NW=4) (7)
