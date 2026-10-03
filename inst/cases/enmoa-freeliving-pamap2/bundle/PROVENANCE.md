# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: enmoa-freeliving-pamap2
- **Dataset**: PAMAP2 Physical Activity Monitoring dataset, subject 101 hand-worn IMU accelerometer (x, y, z in g at 100 Hz), a ~62-minute free-living recording (749 non-overlapping 5 s epochs)
- **Hypothesis (pre-registered)**: On a real free-living accelerometer recording (PAMAP2 hand sensor, 100 Hz, 5 s epochs), the newly-authored computeENMOa reproduces GGIR::g.applymetrics ENMOa to machine precision (max |diff| < 1e-9 g, correlation 1.0); and ENMOa >= ENMO at every epoch (ENMOa retains the sub-1 g dips ENMO truncates).
- **Prereg file hash**: `f41c4f05b1086b223429d7cd99ef89134f40ebb711a9e1c18c618b7cccd4d6a9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `1956aa066cf18b19931a58ed2f7ca9f3cc3ef0ba3e54346e5a3e7445803cf1c3` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `f059ee4d87b60cef` (xxhash64); replay all_match = TRUE (byte-identical).
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
