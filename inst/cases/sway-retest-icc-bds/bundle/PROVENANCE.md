# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-retest-icc-bds
- **Dataset**: Santos & Duarte (2016) BDS; COP path length (PhysioMoCap::swayMetrics) across 3 repeated eyes-open-firm quiet-standing trials, 163 subjects
- **Hypothesis (pre-registered)**: The COP path length has good single-trial test-retest reliability across 3 repeated eyes-open-firm quiet-standing trials in the BDS cohort (ICC(2,1) > 0.75), and the 3-trial average is more reliable still; the newly-authored intraclassCorrelation reproduces psych::ICC(lmer=FALSE) and pingouin.intraclass_corr to machine precision.
- **Prereg file hash**: `9e0c117a79d7ecd750a4b97910d3053b7720a116a89bcba9eb62a1c3cd1c7160` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `cb0e957e38451679c4dcde44488c232ff82ccbd55e3e3545a6084aa3a1727985` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `574b1a344c841f88` (xxhash64); replay all_match = TRUE (byte-identical).
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
