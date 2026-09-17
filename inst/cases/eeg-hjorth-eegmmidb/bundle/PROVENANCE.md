# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-hjorth-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), all 64 EEG channels, first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On real eyes-closed 64-channel EEG (eegmmidb S002R02), eegComplexity's Hjorth mobility + complexity reproduce an independent numpy implementation (matched unbiased variance) bit-for-bit and antropy.hjorth_params to machine precision up to its biased-variance (ddof) convention, across all channels; and mobility is lowest over the posterior (parieto-occipital) region where the eyes-closed alpha rhythm dominates (slow oscillation = low mobility).
- **Prereg file hash**: `59343dee5820fd36c7cad73cdca08fbe23cbac4c028a73def50d11b2c2a10d90` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `7ccfa5d32e3457202ff37eba319c76cfa735ec7f2c28b2a2b1a3402f6a5b3d00` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `26679d2e3fe2364f` (xxhash64); replay all_match = TRUE (byte-identical).
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
