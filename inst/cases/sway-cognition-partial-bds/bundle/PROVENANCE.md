# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-cognition-partial-bds
- **Dataset**: Santos & Duarte (2016) BDS; per-subject eyes-closed-foam COP path length (PhysioMoCap::swayMetrics), Trail Making Test A time and age, complete triples
- **Hypothesis (pre-registered)**: The rank (Spearman) partial correlation of eyes-closed-foam sway and Trail Making Test A time controlling for age is attenuated relative to the marginal Spearman rho (0.532); the newly-authored partialCorrelation reproduces ppcor::pcor.test AND an independent closed-form recompute to machine precision.
- **Prereg file hash**: `414b5de16fdf780dd6c3fb14973edcf0166f5d1f7824e803cef9f2772272ca31` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `b2c9d9429dd19ad1325409fbe87c68b5f1d5c099750ea4a63ee747a0f796f8b9` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `68870d9349a29648` (xxhash64); replay all_match = TRUE (byte-identical).
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
