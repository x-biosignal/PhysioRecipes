# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ecg-pvc-mitbih
- **Dataset**: MIT-BIH Arrhythmia Database record 106, 2027 cardiologist-annotated beats (520 PVCs), MLII @ 360 Hz
- **Hypothesis (pre-registered)**: On MIT-BIH record 106, classifying the cardiologists' reference beats by prematurity + QRS morphology (ecgDetectPVC) recovers the V (PVC) beats precisely (PPV ~0.99) with high recall on isolated ectopy (F1 ~0.98).
- **Prereg file hash**: `42f7760a53d0e03dc0ce08beac9619a3ac55d3fa6e4e1615bf32ee8c819e9fd9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `1e6a1dc62cd1c5075b55c6acec6e3ee5e16742f0b7716b1784856064d89473ce` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `6cf7b3d3fc43b23c` (xxhash64); replay all_match = TRUE (byte-identical).
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
