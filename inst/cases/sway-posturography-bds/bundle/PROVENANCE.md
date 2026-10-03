# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-posturography-bds
- **Dataset**: Santos & Duarte (2016) public balance dataset (figshare), subject 1, eyes-open firm-surface trial, 60 s quiet standing, force-plate center of pressure at 100 Hz
- **Hypothesis (pre-registered)**: On a real 60-s quiet-standing center-of-pressure trial, PhysioMoCap::swayMetrics reproduces an independent Python reimplementation of the Prieto et al. (1996) formulas BIT-FOR-BIT (path length, mean velocity, 95% confidence ellipse/circle area, sway area, mean/RMS distance); and the 95% confidence ellipse contains approximately 95% of the COP samples.
- **Prereg file hash**: `a5c5bdb2439735a1a8e825760db714724ae4f1f8a5c5367eaa88633605e8428e` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `e2b378f82a5fd8d092c6dc0de845061419e8f0fdfcbb98767e9d163b1b75de30` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `9a8f9c305db50f3a` (xxhash64); replay all_match = TRUE (byte-identical).
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
