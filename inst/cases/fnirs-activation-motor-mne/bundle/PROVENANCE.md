# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: fnirs-activation-motor-mne
- **Dataset**: MNE-Python fNIRS motor dataset (public finger-tapping NIRx, converted to SNIRF); 28 source-detector channels, 7.81 Hz; three conditions (Control / Tapping_Left / Tapping_Right), 30 blocks each
- **Hypothesis (pre-registered)**: Running intensityToOD -> mbll -> nirsActivationGLM on the real MNE fnirs_motor finger-tapping recording, the Tapping-vs-Control contrast recovers the canonical fNIRS activation signature: a significant HbO INCREASE (>= half of the 28 channels) with a concurrent HbR DECREASE (most channels), the grand-average HbO response peaking a few seconds after onset.
- **Prereg file hash**: `a750d298706fe1c2f9ea6a01431074122ebbae89b837187b42b08bacdf09d1bd` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `176e3a6a61fc46e5c9daf0e55dae71d2761b5888111f4c77b4687871ed582c00` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
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
