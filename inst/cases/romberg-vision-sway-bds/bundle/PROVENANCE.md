# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: romberg-vision-sway-bds
- **Dataset**: Santos & Duarte (2016) balance dataset (figshare); COP path length (PhysioMoCap::swayMetrics) on eyes-closed vs eyes-open foam surface for 50 subjects
- **Hypothesis (pre-registered)**: Across 50 subjects, foam-surface COP path length is greater with eyes closed than eyes open (paired difference > 0); pairedTTest reproduces scipy.stats.ttest_rel AND base R t.test(paired=TRUE) BIT-FOR-BIT.
- **Prereg file hash**: `a6e744df36a8f57f61c262ff0abf14218803df7c8a39b95f69283000526f5b8a` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `280721d36b392fd89d8537a815bd7a96041d3bc425a2d0a5a52829a65ddd089d` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `57f7d9d128fead71` (xxhash64); replay all_match = TRUE (byte-identical).
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
