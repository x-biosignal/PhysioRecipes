# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: emg-fatigue-ebied
- **Dataset**: Ebied et al. 2021 (Zenodo 5189275) subject 1, 8-channel sEMG @ 200 Hz, 6 kg load, 120 s sustained contraction, 50 Hz notch
- **Hypothesis (pre-registered)**: Under a sustained 6 kg elbow-flexion hold, the EMG median frequency declines from start to end (fatigue index < 1), reproducing the De Luca (1984) myoelectric-fatigue law on subject 1 of the Ebied et al. (2021) cohort.
- **Prereg file hash**: `3fe7502a0573d38534045abaa7fa81813a0dc0201af1387e7bb57ac667aa7aa4` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `1653c7a0f7ec5bac963f66b7e48ceeb3e665a2598f5245b08fd8e5f5cd91f308` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `da52dc6bebf62060` (xxhash64); replay all_match = TRUE (byte-identical).
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
