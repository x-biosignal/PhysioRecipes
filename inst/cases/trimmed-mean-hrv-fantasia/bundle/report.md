# trimmed-mean-hrv-fantasia

- 10%-trimmed mean of the RR intervals (robust location) (762)
- 20%-trimmed mean of the RR intervals (moves toward the median) (760)
- |trimmedMean - scipy.stats.trim_mean| (bit-exact) (0)
- |trimmedMean - base R mean(x, trim)| (bit-exact) (0)
- ordinary (untrimmed) mean RR -- inflated by the skew (766)
- median RR (the fully robust location) for the progression (756)
- mean > 10%-trimmed > 20%-trimmed > median (skew ordering) (yes)
- RR intervals in the 5-minute window (392)
