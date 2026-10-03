# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ecg-hrv-mitbih
- **Dataset**: MIT-BIH Arrhythmia Database, record 100 (MLII/V5, 360 Hz), full 30-min record
- **Hypothesis (pre-registered)**: MIT-BIH record 100 exhibits a normal resting heart rate.
- **Prereg file hash**: `7367de3afa79bde601cdcd10c227c50036bddcd58ca7c57d76792e4999d8f427` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `70050c8c9f3b455aadaf5f82cc7deb1d6020ce52a4895790e3e6968bb23c1e1d` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `af49efe151cc44b8` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 2/2 grounded, 0 artifact-mismatch (`verification_report.json`).
- **Seed**: 100.

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
