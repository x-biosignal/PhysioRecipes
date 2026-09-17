# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-dynrange-pathology-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); vertical-GRF dynamic range (peak1 - trough via PhysioMoCap::grfLandmarks) in healthy controls vs knee-pathology patients, shod, standardised walking speed
- **Hypothesis (pre-registered)**: The vertical-GRF dynamic range (loading peak minus mid-stance trough) is greater in healthy controls (n=208) than in knee-pathology patients (n=499); the certified twoSampleTTest reproduces scipy.stats.ttest_ind(equal_var=FALSE) AND base R t.test BIT-FOR-BIT.
- **Prereg file hash**: `7b8e5d14c513274290480404bf74039903d7648dac0b817938f810dc4e70d7b8` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `752bd3e4a0ac0b49805ea690fb40c8d6a0b8634f994ef72f9e1ff461352eeb4a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `6c2e806329f75319` (xxhash64); replay all_match = TRUE (byte-identical).
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
