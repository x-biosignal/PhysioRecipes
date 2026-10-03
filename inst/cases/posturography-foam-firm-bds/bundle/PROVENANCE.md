# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: posturography-foam-firm-bds
- **Dataset**: Santos & Duarte (2016) balance dataset (figshare); COP path length (PhysioMoCap::swayMetrics) on eyes-open foam vs eyes-open firm surface for 50 subjects
- **Hypothesis (pre-registered)**: Across 50 subjects, center-of-pressure path length during quiet standing is greater on a foam surface than on a firm surface (paired difference > 0); the newly-authored pairedTTest reproduces scipy.stats.ttest_rel AND base R t.test(paired=TRUE) BIT-FOR-BIT.
- **Prereg file hash**: `e93b426beaa4cbc835b50f031ddf9942391c2dd0b7d866bee26a36a5a0a3c1da` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `ec1c133f71a6015d897aaa5684d73fe22b62e90aa4177aa2793627ffb76f9e8a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `ec327bfc7658a7a1` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 8/8 grounded, 0 artifact-mismatch (`verification_report.json`).
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
