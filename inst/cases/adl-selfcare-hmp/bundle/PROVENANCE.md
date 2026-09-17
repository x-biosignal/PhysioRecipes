# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-selfcare-hmp
- **Dataset**: HMP (UCI #283), 13 subjects, single tri-axial wrist accelerometer @ 32 Hz; 7 activities grouped into 5 classes (grooming/drinking/eating/walking/walking_upstairs); leave-one-subject-out kNN
- **Hypothesis (pre-registered)**: Under leave-one-subject-out on real single-wrist accelerometry (HMP, 13 subjects, 5 classes), self-care windows are recognised as SOME self-care activity ~0.94 of the time and 5-class accuracy is ~0.60; grooming (d520) and drinking (d560) are recognised cross-subject (recall ~0.77 / ~0.81), but eating (d550) is NOT distinguished (recall ~0) -- confused with other hand-to-mouth gestures.
- **Prereg file hash**: `2f425da2bd0f5c01eb3763858c4dc3f7c49cef6769b791badb138d2c95a77f56` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `47760b4db2de8bad04b5d39c85a630dbc910c6ec067ab7355eee4d3263a852e5` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `1ce7ea096b94c2fd` (xxhash64); replay all_match = TRUE (byte-identical).
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
