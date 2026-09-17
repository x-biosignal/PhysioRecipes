# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-freeliving-pamap2
- **Dataset**: PAMAP2 (UCI #231), subject 101, hand IMU +-16g acceleration @ 100 Hz; the first 374500 gap-free samples (749 five-second epochs, ~1.04 h), converted to g
- **Hypothesis (pre-registered)**: PhysioWearable's computeENMO reproduces GGIR::g.applymetrics's ENMO on the identical hand-acceleration signal to MACHINE PRECISION (max absolute difference far below 1e-6 g, correlation 1.0 over the 749 five-second epochs); and the free-living summary built on that ENMO series yields a negative Rowlands intensity gradient (~-1.19), ~28.6 MVPA minutes, and an activity-to-sedentary fragmentation (ASTP ~0.113) on this ~1 h recording.
- **Prereg file hash**: `ee72c48453bfba9c2e358a3feddb0d222970786ec81a67cbb775de975ceb003c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `7a3d1e55a7d746193dea19a79e7409cfe1d38cfc7ff8db7ffdb3d0b02c23ad8a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `93b9d0e5ca1f753f` (xxhash64); replay all_match = TRUE (byte-identical).
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
