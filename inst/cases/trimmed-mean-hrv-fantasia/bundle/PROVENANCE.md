# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: trimmed-mean-hrv-fantasia
- **Dataset**: Fantasia database (PhysioNet), subject f1y01 (young healthy adult), first 5-minute RR window (392 intervals, ms)
- **Hypothesis (pre-registered)**: On real Fantasia RR intervals, the newly-authored trimmedMean reproduces BOTH scipy.stats.trim_mean AND base R mean(x, trim) BIT-FOR-BIT; and because the RR distribution is right-skewed, the plain mean exceeds the trimmed mean, which exceeds the median (mean > trimmed > median).
- **Prereg file hash**: `6ed6356e7ba84ff212fa030c83ab42dfa2f3304a161dbfc60eaafd9fa2277d01` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `6e317cf801dafefbdda87126b26e1417da8153afff88bc6c17d0aff3bd2c983b` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `03613d280ae8e0e2` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 8/8 grounded, 0 artifact-mismatch (`verification_report.json`).
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
