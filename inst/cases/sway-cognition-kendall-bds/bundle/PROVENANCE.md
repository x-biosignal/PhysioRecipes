# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-cognition-kendall-bds
- **Dataset**: Santos & Duarte (2016) BDS; per-subject eyes-closed-foam COP path length (PhysioMoCap::swayMetrics) vs Trail Making Test part A time, complete pairs
- **Hypothesis (pre-registered)**: In the BDS cohort (n=158), eyes-closed-foam COP path length is positively associated with Trail Making Test A time (slower processing speed -> more sway); the newly-authored kendallTau reproduces base R stats::cor.test(method='kendall') AND scipy.stats.kendalltau BIT-FOR-BIT for the tau-b statistic and the normal-approximation p-value.
- **Prereg file hash**: `0976bf8c54fb8acce4c48ac8563ad79dbf09789125bc5424d9e0edd83665293e` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `4d49931fa227e833c00177ddc8ec0a93868780387b36ba71d5920ff074170c05` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `dde8e045e609451c` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 9/9 grounded, 0 artifact-mismatch (`verification_report.json`).
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
