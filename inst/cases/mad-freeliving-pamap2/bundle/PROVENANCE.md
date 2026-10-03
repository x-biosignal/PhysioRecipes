# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: mad-freeliving-pamap2
- **Dataset**: PAMAP2 Physical Activity Monitoring dataset, subject 101 hand-worn IMU accelerometer (x, y, z in g at 100 Hz), a ~62-minute free-living recording (749 non-overlapping 5 s epochs)
- **Hypothesis (pre-registered)**: On a real free-living accelerometer recording (PAMAP2 hand sensor, 100 Hz, 5 s epochs), the newly-authored computeMAD reproduces GGIR::g.applymetrics MAD to machine precision (max |diff| < 1e-9 g, correlation 1.0) across all epochs.
- **Prereg file hash**: `db318b04fef16e92139e2c9aec24f9384db7b7f3ae26c1b50391db21c34ae1c3` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `4fd559f1f8a74c9d19e6af70712e85330fc3be5775227561c07b597903d1526a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `4d5fc75c46c4bee8` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 6/6 grounded, 0 artifact-mismatch (`verification_report.json`).
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
