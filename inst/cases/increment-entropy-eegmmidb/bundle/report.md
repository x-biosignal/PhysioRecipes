# increment-entropy-eegmmidb

- increment entropy at m=2, q=4 of the POz signal (bits) (4.27)
- increment entropy at m=3 -- lower than m=2 (non-increasing in dimension) (3.51)
- increment entropy at m=4 -- lower still (monotone family) (3.01)
- max |incrementEntropy - NeuroKit2 entropy_increment| over the (dimension, q) family (bit-exact) (9e-16)
- distinct increment-words realized at m=2, q=4 (out of (2q+1)^m = 81 possible) (33)
- IncrEn is non-increasing in the embedding dimension (1 = holds) (yes)
