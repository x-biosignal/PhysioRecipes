# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-detrend-scipy-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel Fpz (frontopolar, the largest linear drift), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real drifting frontopolar EEG channel (eegmmidb S002R02, Fpz), detrendSignal reproduces scipy.signal.detrend BIT-FOR-BIT for both the linear (least-squares line) and constant (mean) types; and the linear detrend removes a low-frequency trend that constant (mean) removal leaves in -- so the sub-1-Hz spectral power is markedly lower after linear than after constant detrending.
- **Prereg file hash**: `27f112c543be06e452a3d17175c8ee0a0597bdd76e887905bbcf7fced22a70fd` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `09490ec19ff13ca163b384cbada72bf3a587079d3ebe970384ec4b2aea186a8b` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
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
