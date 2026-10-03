# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ecg-hrv-aging-fantasia
- **Dataset**: Fantasia Database, record f1y01 (young, 23 y), resting ECG @ 250 Hz, fixed 10-min window t=300-900 s
- **Hypothesis (pre-registered)**: Fantasia young subject f1y01 has well-defined resting frequency-domain HRV (LF/HF/total power) over the t=300-900 s window.
- **Prereg file hash**: `f491f165e3e832441e0678b0abc6bb9defd451113ec5dde831691367a84a4ee9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `cc1bc6f4e5c93c3acab9652b1792469053431246e209a22e4726deeb2f2e23d6` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `9cd2cc6bedce8c94` (xxhash64); replay all_match = TRUE (byte-identical).
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
