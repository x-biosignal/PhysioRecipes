# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-coherence-scipy-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), the eight parieto-occipital channels (PO7, PO3, POz, PO4, PO8, O1, Oz, O2), first 10 s at 160 Hz
- **Hypothesis (pre-registered)**: On the eight parieto-occipital channels of real eyes-closed EEG (eegmmidb S002R02), eegCoherence's magnitude-squared coherence reproduces scipy.signal.coherence (symmetric Hann, matched window length + overlap, detrend=False) band-averaged over 8-13 Hz, BIT-FOR-BIT across all channel pairs; and the posterior alpha-band coherence is high (the eyes-closed alpha rhythm is spatially synchronized), peaking between adjacent occipital channels.
- **Prereg file hash**: `6bb6804dcc78e5bd29508be4952df175cd80575575a522d7d23daa54b6b57f98` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `334a9120e66a830ffbfd5455b976e24d8356fd5c82c720670b3bfe9cf2ccce73` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `0bafa4529c19cf71` (xxhash64); replay all_match = TRUE (byte-identical).
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
