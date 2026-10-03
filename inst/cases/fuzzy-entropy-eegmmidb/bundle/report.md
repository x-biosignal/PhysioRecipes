# fuzzy-entropy-eegmmidb

- fuzzy entropy at m=2, r=0.2 of the POz signal (0.95)
- fuzzy entropy at m=3 -- lower than m=2 (non-increasing in dimension) (0.70)
- max |fuzzyEntropy - NeuroKit2 entropy_fuzzy| over the (dimension, r) family (bit-exact) (4e-15)
- crisp sample entropy at the same m=2, r=0.2 (the reference FuzzyEn generalizes) (1.33)
- |FuzzyEn - SampEn| at m=2 -- the soft membership counts partial matches the crisp step rejects (0.38)
- FuzzyEn is non-increasing in the embedding dimension (1 = holds) (yes)
