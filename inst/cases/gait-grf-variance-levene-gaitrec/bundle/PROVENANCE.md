# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-variance-levene-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); Levene's test of the vertical-GRF dynamic-range variance across the five gait classes
- **Hypothesis (pre-registered)**: The five GaitRec gait classes differ in the variance of their vertical-GRF dynamic range; the robust Levene (Brown-Forsythe) test is significant while the normality-sensitive Bartlett test may not be. The newly-authored leveneTest reproduces scipy.stats.levene(center='median') and car::leveneTest(center=median) to machine precision.
- **Prereg file hash**: `1de81a67c036c53f3fc0c6f94f077370944ad8539e341d3980db78bb8fecc06f` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `050f1cbd29861564129d62b6143480d44a6a48ef52d0f52802a68df5568023c3` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `cb1191a51f54595f` (xxhash64); replay all_match = TRUE (byte-identical).
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
