# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-plv-alpha-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002 baseline run R02 (eyes-closed), occipital channels O1 and Oz, first 10 s at 160 Hz (1600 samples each)
- **Hypothesis (pre-registered)**: On real eyes-closed occipital EEG (eegmmidb S002R02, channels O1 and Oz), the alpha-band (8-13 Hz) phase-locking value is high (the posterior alpha rhythm is phase-synchronized across neighbouring occipital sites), phaseLockingValue reproduces an independent scipy Hilbert-band PLV, and it recovers ground truth on constructed signals (phase-locked -> PLV ~ 1, independent -> PLV ~ 0).
- **Prereg file hash**: `92d41615a992ddc9aa30630135a4852d3eb84ecf6ec4349f84e4735c11d3eb2e` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `aca78bd49a24ddd581e33e01e8f64866958618926945f7591bd6b314057cbd60` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `bfd7737fa5270e21` (xxhash64); replay all_match = TRUE (byte-identical).
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
