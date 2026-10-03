# gait-grf-tukey-pathology-gaitrec

- Tukey mean difference of the ankle vs healthy-control dynamic range (BW) (-0.142)
- -log10 of the ankle-vs-healthy adjusted p (a representative significant pair) (10.8)
- adjusted p of knee vs ankle (a representative non-significant pathology-pathology pair) (0.83)
- the smallest of the six pathology-pathology adjusted p-values (all > 0.05: none differ) (0.61)
- max |tukeyHSD adjusted p - base R TukeyHSD p| across all 10 pairs (machine precision) (<1e-9)
- max |tukeyHSD adjusted p - scipy.stats.tukey_hsd p| across all 10 pairs (machine precision) (<1e-9)
- number of healthy-vs-pathology pairs that are significant (all 4) (4)
- number of pathology-pathology pairs that are significant (none) (0)
- total pairwise comparisons (5 choose 2) (10)
- total subjects across the five classes (1844)
