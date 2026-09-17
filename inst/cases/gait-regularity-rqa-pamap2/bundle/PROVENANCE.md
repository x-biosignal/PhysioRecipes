# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-regularity-rqa-pamap2
- **Dataset**: PAMAP2 (UCI #231), subject 101, ankle IMU +-16g acceleration vector magnitude @ 100 Hz; walking / running / vacuuming / ironing, first 2500 valid samples each
- **Hypothesis (pre-registered)**: On real ankle-acceleration magnitude (PAMAP2 subject 101), rhythmic locomotion is quasi-periodic and deterministic while aperiodic activity is not: recurrence determinism (DET) orders running > walking >> ironing, and approximate entropy orders ironing >> walking -- each stride recurs, so walking's DET is high (~0.92) and its entropy low (~0.46), whereas ironing's DET is low (~0.38) and its entropy high (~1.28).
- **Prereg file hash**: `a981d0946c0d6af50623415efe896cce55743dd38a918d11f08cacb9b36ce9da` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `90e1e0433b34de3597e4dafc8a3e0fa7c7845b9f13534ace6c1b59129aac79b1` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `407eaf29cdd66577` (xxhash64); replay all_match = TRUE (byte-identical).
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
