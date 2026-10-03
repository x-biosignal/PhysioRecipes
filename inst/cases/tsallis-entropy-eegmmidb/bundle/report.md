# tsallis-entropy-eegmmidb

- Tsallis entropy at q=2 (collision-order) of the POz amplitude distribution (0.89)
- Tsallis entropy at q=1 -- exactly the Shannon entropy (the family's special case) (2.32)
- max |tsallisEntropy - NeuroKit2 entropy_tsallis| over q = {0.5, 1, 2, 3} (bit-exact family) (9e-16)
- |Tsallis(q=2) - Renyi(alpha=2)| -- the two generalizations diverge (non-additive vs additive) (1.28)
- |Tsallis(q=1) - Renyi(alpha=1)| -- both recover Shannon, so they coincide at 1 (~0) (0)
- Tsallis S_q is non-increasing in q (1 = holds) (yes)
