# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: iqr-hrv-fantasia
- **Dataset**: Fantasia database (PhysioNet), subject f1y01 (young healthy adult), first 5-minute RR window (391 intervals, ms)
- **Hypothesis (pre-registered)**: On real Fantasia RR intervals, the newly-authored interquartileRange (type-7 quantiles) reproduces BOTH scipy.stats.iqr AND base R IQR BIT-FOR-BIT; and because the RR distribution is right-skewed and heavy-tailed, the robust IQR-based SD estimate is materially below SDNN -- the opposite of the near-Gaussian EEG where the robust scale matched the SD.
- **Prereg file hash**: `752748b0c6272f7843642fb69f1d12daaa03cec129369a5c238fb39bf7a37e25` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `b036e0b9963ce4563f68756c7e3c9069371d817f12e8f998248e5a268ada46d2` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `7cab630243dbf278` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 9/9 grounded, 0 artifact-mismatch (`verification_report.json`).
- **Seed**: 1.

## Files
- `prereg.json` -- frozen confirmatory plan (sha256 above).
- `run_manifest.json` -- op-DAG + content-addressed output hashes + environment fingerprint.
- `terminal_table.csv` -- the terminal statistic table (content-addressed).
- `benchmark_table.csv` -- the external-reference comparison table (when the spec carries a reference).
- `claims.json` / `verification_report.json` -- claim registry + grounding verdicts.
- `scientific_report.json` -- two-stage scientific-gate verdict.
- `report.md` -- human-readable report citing only artifact-backed numbers.

HONESTY: the bundle certifies reproducibility and auditability (grounded claims,
frozen pre-registration, byte-identical replay), not scientific correctness or
appropriateness -- those remain expert judgement.
