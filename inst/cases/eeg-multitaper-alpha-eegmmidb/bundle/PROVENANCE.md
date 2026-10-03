# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-multitaper-alpha-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S001 baseline run R02 (eyes-closed), occipital channel O1, first 10 s at 160 Hz (1600 samples) -- the same git-tracked PhysioExperiment the sibling wavelet case uses
- **Hypothesis (pre-registered)**: On real eyes-closed occipital EEG (eegmmidb S001R02, O1), eegMultitaper's DPSS tapers reproduce scipy.signal.windows.dpss to machine precision and its full multitaper PSD reproduces an independent scipy+numpy reconstruction of the same non-adaptive algorithm to machine precision, and it agrees with MNE psd_array_multitaper in structure (up to a one-sided normalization); the PSD is dominated by the alpha rhythm (~10 Hz peak).
- **Prereg file hash**: `8c2c3f8c2ba0e924a5611b033284ddf1a4ef67d64deec2a202d9cfbfd697a458` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `9e0a5293be3892939e7ac5e21bb10d156e58ee557e03872af8a4a91bfc96db2d` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `9c55673e07411282` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 6/6 grounded, 0 artifact-mismatch (`verification_report.json`).
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
