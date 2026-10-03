# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-bandpower-welch-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), all 64 EEG channels, first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On real eyes-closed 64-channel EEG (eegmmidb S002R02), bandPower(method='welch') reproduces scipy.signal.welch (symmetric Hann, nperseg=256, noverlap=128, detrend=False, scaling='density') integrated over the identical EEG-band indices, BIT-FOR-BIT across all 64 channels x 5 bands; and relative alpha power is highest over the posterior (parieto-occipital) region where the eyes-closed alpha rhythm dominates.
- **Prereg file hash**: `25407f14b4c80cbad4ee5dbbae76ea4f08401bb2bc817ffac4225c807adda7f6` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `fd7d2646a3b7af20e48287cb83d59c537dfa1ae2f1cb4fe3cf1d6bc13efd60ce` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `a2dc0d5fb224faf2` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 8/8 grounded, 0 artifact-mismatch (`verification_report.json`).
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
