# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ppg-hr-bidmc
- **Dataset**: BIDMC record bidmc01 (PhysioNet), PLETH + II @ 125 Hz, ~8 min ICU recording
- **Hypothesis (pre-registered)**: The PPG (PLETH) pulse rate agrees with the simultaneous ECG (lead II) heart rate on BIDMC record bidmc01 (mean pulse rate within a few bpm of the ECG gold standard).
- **Prereg file hash**: `6aff2c0ffc8fc91cf362743d99c892558adfac5da85eb15f93202271862f0618` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `d04c7e7c4d78e74f41b983e23f5bbd0d45ec5175be96ef7507dc78be94474cb4` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `6bf559863f03e5b5` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 5/5 grounded, 0 artifact-mismatch (`verification_report.json`).
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
