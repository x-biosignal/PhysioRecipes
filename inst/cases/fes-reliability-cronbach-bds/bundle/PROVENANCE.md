# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: fes-reliability-cronbach-bds
- **Dataset**: Santos & Duarte (2016) BDS; the 7 Falls Efficacy Scale items (FES_1..FES_7) across the cohort
- **Hypothesis (pre-registered)**: The 7 Falls Efficacy Scale items in the BDS cohort (n=163) have good internal-consistency reliability (Cronbach's alpha > 0.8); the newly-authored cronbachAlpha reproduces the psych package (psych::alpha raw_alpha) bit-for-bit and pingouin.cronbach_alpha to machine precision.
- **Prereg file hash**: `14fb8752fbde806fca2af9ddb35e4ef8b24feb098afa94d98895648fe8d63cd7` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `d44a9a930a874cfa6a84d554686874f77924e8064d0467f6b539c06ad5f2bde3` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `b245b0be6a763f14` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 7/7 grounded, 0 artifact-mismatch (`verification_report.json`).
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
