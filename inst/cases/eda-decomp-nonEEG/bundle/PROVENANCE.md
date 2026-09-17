# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eda-decomp-nonEEG
- **Dataset**: PhysioNet Non-EEG (Birjandtalab 2016), Subject 1 EDA channel, Empatica E4 @ 8 Hz, 18343 samples
- **Hypothesis (pre-registered)**: On real Empatica-E4 EDA (PhysioNet Non-EEG, Subject 1), PhysioEDA's highpass phasic/tonic split reproduces NeuroKit2's highpass split like-for-like (phasic r ~0.96, tonic r ~1.0).
- **Prereg file hash**: `8f2c575d96c833282b19aeaf07ea2d69f7609dd2acc282b4ac225c87a5f14182` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `d505b1a123c711ed2ebcc43b04fc91606bfcb49048e61396fde689b8a53b7276` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 2/2 grounded, 0 artifact-mismatch (`verification_report.json`).
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
