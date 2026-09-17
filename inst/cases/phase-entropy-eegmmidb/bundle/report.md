# phase-entropy-eegmmidb

- phase entropy at k=4 sectors (delay 1) of the POz SODP (1.24)
- phase entropy at k=6 -- higher than k=4 (finer angular resolution) (1.29)
- phase entropy at k=8 -- higher still (more sectors) (1.30)
- max |phaseEntropy - NeuroKit2 entropy_phase| over k (bit-exact) (4e-16)
- PhasEn increases with the sector count k (1 = holds) (yes)
- PhasEn lies below the NeuroKit2 normalization ceiling 1/ln(2) = 1.443 (1 = holds) (yes)
