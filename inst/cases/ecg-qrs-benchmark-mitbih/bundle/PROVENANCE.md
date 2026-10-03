# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ecg-qrs-benchmark-mitbih
- **Dataset**: MIT-BIH Arrhythmia Database, record 100 (MLII, 360 Hz, full 30-min), with .atr cardiologist beat annotations
- **Hypothesis (pre-registered)**: On MIT-BIH record 100 the pan_tompkins detector matches the cardiologist .atr beat annotations at F1 >= 0.95 under the AAMI EC57 tolerance.
- **Prereg file hash**: `9d268f9c3498ad26439131107024b9312b60e2312c133846ed797f15ca4515d9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `0bf8c0840e27510e99071f6d34ec7c19309f4e47377831e520a166978e59f6cf` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `fef94730ac146eb2` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 3/3 grounded, 0 artifact-mismatch (`verification_report.json`).
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
