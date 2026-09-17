# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-har-ucihar
- **Dataset**: UCI HAR smartphone accelerometer (Anguita 2013), 30 subjects @ 50 Hz, 6 activities, provided subject-disjoint train (7352) / test (2947) split
- **Hypothesis (pre-registered)**: On the UCI HAR benchmark (Anguita 2013), adlFeatures descriptors + a kNN classifier (trainADL) reach ~0.83 six-class accuracy on the provided subject-disjoint test split, recovering posture (laying) perfectly and locomotion above chance.
- **Prereg file hash**: `9761adb073c5995ed465fb77c2bb450b46b2e1a2225136bb856014ff40d632a1` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `3687017987a5aa4d871502d514ed14fdfa8e074558139f59d35f18fb3418d66b` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `153423ce05ac2174` (xxhash64); replay all_match = TRUE (byte-identical).
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
