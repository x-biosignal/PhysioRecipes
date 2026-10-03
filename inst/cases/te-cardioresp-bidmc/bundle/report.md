# te-cardioresp-bidmc

- transfer entropy respiration -> PPG pulse (model-free directed info flow, bits) (0.036)
- transfer entropy PPG pulse -> respiration (0.024)
- net transfer entropy (respiration->pulse minus pulse->respiration) -- the directed asymmetry (+0.012)
- max |transferEntropy - independent numpy transfer entropy| over both directions (bit-exact) (6e-17)
- TE in the DRIVING direction of a constructed x->y coupling -- directed recovery (large) (0.67)
- TE in the REVERSE direction of the constructed coupling -- much smaller (directed recovery) (0.06)
