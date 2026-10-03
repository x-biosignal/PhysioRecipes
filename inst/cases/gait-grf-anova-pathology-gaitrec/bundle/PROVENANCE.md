# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-anova-pathology-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); vertical-GRF dynamic range (peak1 - trough via PhysioMoCap::grfLandmarks) across the five gait classes, shod, standardised walking speed, initial-presentation baseline sessions
- **Hypothesis (pre-registered)**: The vertical-GRF dynamic range (loading peak minus mid-stance trough) differs across the five GaitRec gait classes -- healthy control (n=208), ankle (n=483), knee (n=499), hip (n=364) and calcaneus (n=290) pathology; the newly-authored oneWayAnova reproduces base R stats::oneway.test(var.equal=TRUE) BIT-FOR-BIT and scipy.stats.f_oneway to machine precision. Healthy controls have a larger dynamic range than the pooled pathology classes.
- **Prereg file hash**: `f6c47047a77fba7b70ff99fdc48d3a0d2f64ae2179699436211169ab19a02b43` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `ef6c28159d82a47c973a8e110ae5bf33086bb1ed2db1d095d1bddf9f1a052ba9` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `8da87da02b437e74` (xxhash64); replay all_match = TRUE (byte-identical).
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
