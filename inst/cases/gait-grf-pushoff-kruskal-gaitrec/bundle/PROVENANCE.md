# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-pushoff-kruskal-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); vertical-GRF push-off peak (3rd landmark of PhysioMoCap::grfLandmarks) across the five gait classes, shod, standardised speed, initial-presentation baseline sessions
- **Hypothesis (pre-registered)**: The vertical-GRF push-off peak differs across the five GaitRec gait classes -- healthy control (n=208), ankle (n=483), knee (n=499), hip (n=364), calcaneus (n=290); the newly-authored kruskalTest reproduces base R stats::kruskal.test BIT-FOR-BIT and scipy.stats.kruskal to machine precision. Healthy controls have the largest push-off (highest mean rank) and calcaneus pathology the smallest (lowest mean rank).
- **Prereg file hash**: `7d7f560fbe8d95b1684155139a1d75fdca9159b0c376ed8a6a9d691da3f13651` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `fe778acfb1968ea6ab78638f3e982476eb8e8be32a3caccda4299f701e469b74` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `cfeb4379c1a3ecfb` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 10/10 grounded, 0 artifact-mismatch (`verification_report.json`).
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
