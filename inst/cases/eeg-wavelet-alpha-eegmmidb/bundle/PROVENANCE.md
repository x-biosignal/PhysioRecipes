# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-wavelet-alpha-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S001, eyes-closed baseline run R02, occipital channel O1, first 10 s (1600 samples) at 160 Hz
- **Hypothesis (pre-registered)**: The Morlet-wavelet scalogram of eyes-closed occipital (O1) EEG (eegmmidb S001R02) is dominated by the alpha rhythm (peak power ~10 Hz), and waveletTransform reproduces MNE-Python's tfr_array_morlet in time-frequency structure (correlation ~1) up to a normalization convention.
- **Prereg file hash**: `456a2f7da3abe3a5bdfc4f20fe268616e1ff8fd389d9beb95250e7fae9e3e331` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `c3c21e01eea67eba0b15c141b13cecd807a144031d4fd801d749b9172293a7a9` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `45e9b7a4b99f5a62` (xxhash64); replay all_match = TRUE (byte-identical).
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
