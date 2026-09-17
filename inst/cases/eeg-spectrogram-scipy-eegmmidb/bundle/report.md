# eeg-spectrogram-scipy-eegmmidb

- max |spectrogram - scipy.signal.spectrogram| over all 129 x 11 (freq x time) cells (bit-exact) (7e-13)
- frequency bins in the spectrogram (window_size/2 + 1) (129)
- time windows in the spectrogram (10 s, 256-sample windows, 50% overlap) (11)
- median peak-power frequency across time windows -- the alpha rhythm (~11 Hz) (11.25)
- time windows whose peak power is in the alpha band (8-13 Hz) -- all of them (sustained rhythm) (11)
- coefficient of variation of alpha power across time -- the waxing/waning the averaged PSD hides (58%)
- mean alpha-band power across time windows at POz (2465)
