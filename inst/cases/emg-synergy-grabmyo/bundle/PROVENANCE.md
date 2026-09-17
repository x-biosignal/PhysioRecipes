# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: emg-synergy-grabmyo
- **Dataset**: GRABMyo v1.1.0, record session1_participant1_gesture10_trial1, first 12 forearm channels @ 2048 Hz
- **Hypothesis (pre-registered)**: A small number of NMF muscle synergies (knee at VAF>=0.90) accounts for most of the GRABMyo forearm EMG variance.
- **Prereg file hash**: `d7d59ead8030aac4db8b96f88f6d5008dc6cc86534b44b75eca20d95d62ae2bb` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `40fb27c45b9c7519b43582c05f3f5426599e840ff536e32dc9da777b9dd1e9a9` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `3d46a7484e47fd37` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 5/5 grounded, 0 artifact-mismatch (`verification_report.json`).
- **Seed**: 42.

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
