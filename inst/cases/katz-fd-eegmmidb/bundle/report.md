# katz-fd-eegmmidb

- Katz's fractal dimension of the posterior EEG channel (POz), amplitude-only convention (3.468)
- antropy.katz_fd on the identical signal (3.4679139453)
- NeuroKit2 fractal_katz on the identical signal (3.4679139453)
- the earlier Euclidean-plane convention value (what the shipped op previously returned) (1.6955955784)
- max |katzFD - antropy.katz_fd| (bit-exact) (0)
- max |katzFD - NeuroKit2 fractal_katz| (bit-exact) (0)
- |amplitude-only KFD - earlier Euclidean-plane KFD| -- the size of the convention fix (1.77)
- samples in the analyzed channel (10 s at 160 Hz) (1600)
