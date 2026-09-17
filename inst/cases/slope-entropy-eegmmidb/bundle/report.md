# slope-entropy-eegmmidb

- slope entropy at m=2 (thresholds 0.1/45 deg) of the POz signal (bits) (1.26)
- slope entropy at m=3 -- higher than m=2 (increasing in dimension) (2.43)
- slope entropy at m=4 -- higher still (unnormalized, grows with pattern length) (3.57)
- max |slopeEntropy - NeuroKit2 entropy_slope| over the embedding dimension (bit-exact) (9e-16)
- distinct slope patterns realized at m=3 (out of 5^(m-1) = 25 possible) (18)
- SlopEn INCREASES with the embedding dimension (1 = holds; contrast with normalized entropies) (yes)
