# poincare-hrv-fantasia

- Poincare SD1 -- short-term (beat-to-beat) RR variability, a parasympathetic proxy (ms) (57.7)
- Poincare SD2 -- long-term RR variability (analytical closed-form, ms) (86.8)
- SD1/SD2 ratio -- the Poincare cloud's short-to-long axis ratio (0.67)
- max |ecgHRVpoincare - independent numpy analytical closed-form| over SD1/SD2/ratio (bit-exact) (0)
- |ecgHRVpoincare SD1 - NeuroKit2 SD1| -- bit-exact (SD1 = universal SDSD/sqrt(2)) (0)
- |independent numpy paired-projection SD2 - NeuroKit2 SD2| -- bit-exact (identifies NeuroKit2's SD2 convention) (0)
- |op SD2 (analytical closed-form) - NeuroKit2 SD2 (paired projection)| -- a documented ~0.2 ms convention gap (O(1/n)) (0.17)
- mean Poincare SD1 across the 5 young subjects (short-term HRV) (55.7522)
- mean Poincare SD1 across the 5 old subjects -- markedly lower (age-related vagal decline) (35.3069)
