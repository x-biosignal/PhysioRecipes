# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-speed-fda-fukuchi
- **Dataset**: WBDS (figshare 5722711), 42 adults x 8 treadmill speeds; sagittal RKneeAngleZ over the gait cycle (101 pts); 328 subject-speed curves
- **Hypothesis (pre-registered)**: On real WBDS knee-angle gait cycles across 8 treadmill speeds (42 subjects, within-subject centred), function-on-scalar regression recovers the established speed-dependence of the knee: the speed-coefficient curve is significant (curve-wide permutation p<0.001), positive, and peaks at the swing-flexion (~65% cycle) at ~+3.3 deg per speed level; pooled peak knee flexion rises with speed (r~0.63).
- **Prereg file hash**: `abc1d021253e394b1e3f54e167655df3316bd3c603b77586c8de9946ff8fc423` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `296850071c5f2e9ac79a6ebe08c31e38bc88fe46f2ee4a0d44dc2a683c337c54` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `04c78bf2f251c11e` (xxhash64); replay all_match = TRUE (byte-identical).
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
