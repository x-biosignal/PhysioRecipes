# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-permutation-entropy-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S001, baseline run R02 (eyes-closed rest), all 64 channels, 160 Hz
- **Hypothesis (pre-registered)**: On the eyes-closed resting EEG of eegmmidb S001 (run R02, 64 channels, 160 Hz), the permutation entropy (Bandt-Pompe, order 3, delay 1) computed by eegComplexity reproduces the canonical Python antropy.perm_entropy to machine precision on every channel: the per-channel values correlate 1.0 with a max absolute difference below 1e-9, and the entropies are physiologically plausible (normalized, ~0.9).
- **Prereg file hash**: `1b538d1e81f5ce63c2ef8adc5c387cf78e0aea3e243063f4be6bc706487095dd` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `af9f971e28621a08bdc73cd6aaf1ca0186ba3eeb5e6d4604b6de15aa007384fc` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `a410030635ec2335` (xxhash64); replay all_match = TRUE (byte-identical).
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
