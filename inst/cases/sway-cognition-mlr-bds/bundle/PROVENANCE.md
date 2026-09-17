# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-cognition-mlr-bds
- **Dataset**: Santos & Duarte (2016) BDS; multiple OLS of per-subject eyes-closed-foam COP path length (PhysioMoCap::swayMetrics) on age and TMT-A, n=158
- **Hypothesis (pre-registered)**: In a multiple OLS regression of eyes-closed-foam sway on age and Trail Making Test A, age is a strong significant predictor while TMT-A's independent contribution is not significant; the newly-authored multipleRegression reproduces base R stats::lm and statsmodels OLS bit-for-bit / to machine precision.
- **Prereg file hash**: `85cdc74fc99e24947e349cddf20a0068b4d3632d0faa8fa9322c7deb828f3edd` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `f4dbae9d85374e931d6de784d6e42c98044ce95d1121d1e99c203894e8f2692d` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `8d76f53543b3ee7a` (xxhash64); replay all_match = TRUE (byte-identical).
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
