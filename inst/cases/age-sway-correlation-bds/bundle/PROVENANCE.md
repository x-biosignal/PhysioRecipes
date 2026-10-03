# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: age-sway-correlation-bds
- **Dataset**: Santos & Duarte (2016) balance dataset (figshare); age vs COP path length (PhysioMoCap::swayMetrics) on eyes-open foam and firm surfaces for 50 subjects
- **Hypothesis (pre-registered)**: Across 50 subjects (ages 18-75), foam-surface COP path length increases with age (positive Pearson correlation); the correlation is stronger on foam than on firm ground; and the newly-authored correlationTest reproduces scipy.stats.pearsonr AND base R cor.test BIT-FOR-BIT.
- **Prereg file hash**: `cbacb70a5f6b1c95d55875c5919f9dd08f487bd895b0433abce7e6fa735a8674` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `c204097c8357638e6f53b7d7d9baf5390616ca291f21e4e716c39abb32a4797c` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `2e5c7b714fab07be` (xxhash64); replay all_match = TRUE (byte-identical).
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
