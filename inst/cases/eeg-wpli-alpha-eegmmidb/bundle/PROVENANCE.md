# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-wpli-alpha-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002 baseline run R02 (eyes-closed), occipital channels O1 and Oz, first 10 s at 160 Hz (1600 samples each)
- **Hypothesis (pre-registered)**: On the real occipital O1-Oz pair, the debiased wPLI is low (consistent with the PLI case -- the alpha coupling is mostly volume conduction); weightedPLI reproduces an independent scipy imaginary-cross-spectrum wPLI; and the debiasing works -- for INDEPENDENT signals the biased wPLI is spuriously positive but the debiased wPLI is ~0, while genuine lagged coupling stays ~1.
- **Prereg file hash**: `a2293ac09727c01b74bf723296f57ca21a82daddd06764c6d3ef9108a0da9501` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `a9fd73b64818c9f0d7d30ccc0e8678781c465b54ee73f2f497b5c9cf3719dbf0` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `cb744d5cf76a86a6` (xxhash64); replay all_match = TRUE (byte-identical).
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
