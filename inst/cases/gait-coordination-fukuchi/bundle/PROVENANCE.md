# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-coordination-fukuchi
- **Dataset**: WBDS (figshare 5722711), 42 adults, sagittal RHipAngleZ + RKneeAngleZ time-normalised to the gait cycle (101 pts); 328 treadmill + 123 overground trial-cycles
- **Hypothesis (pre-registered)**: On real sagittal (Z-axis flexion) hip and knee gait kinematics (WBDS, 42 adults), the hip and knee move substantially OUT of phase (MARP ~84 deg), and two independent coordination methods agree: vector coding's modal pattern is distal (knee-led, ~0.36), in-phase is a minority (~0.29), not simple lockstep. Between-cycle deviation phase is similar on treadmill and overground (no condition difference claimed).
- **Prereg file hash**: `aca01f89ec0c799b97331d463e8050f6f40a74d3a66fb3f5010a1a86316dedbb` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `4262716dcafbcbfbe0e7ac95c1c932c75633826665f798067b48d6f32c4ce602` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `09c469fe6faa470d` (xxhash64); replay all_match = TRUE (byte-identical).
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
