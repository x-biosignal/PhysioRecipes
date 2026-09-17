# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-pushoff-age-regression-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); vertical-GRF push-off peak (3rd landmark of PhysioMoCap::grfLandmarks) regressed on age in healthy controls, shod, standardised speed, initial-presentation baseline sessions
- **Hypothesis (pre-registered)**: In GaitRec healthy controls (n=208, ages 15-78), the vertical-GRF push-off peak declines with age (negative OLS slope); the newly-authored linearRegression reproduces base R stats::lm and scipy.stats.linregress bit-for-bit for the slope, R-squared and slope p-value.
- **Prereg file hash**: `a6db83000668d840235ddc7642b42a021ac5beb2505673bece5da2ba82d32d5c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `1390c7e25ee2ac07793b6c240c93e7d7c0ed11b58860704d5b2c11e294402095` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `1ecffe4cd4966794` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 10/10 grounded, 0 artifact-mismatch (`verification_report.json`).
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
