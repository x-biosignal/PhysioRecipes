# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: phase-entropy-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), the newly-authored phaseEntropy reproduces NeuroKit2 entropy_phase BIT-FOR-BIT across the sector count k; it increases with k (finer angular resolution); and it lies below the 1/ln(2) normalization ceiling implied by NeuroKit2's base-2/natural-log convention.
- **Prereg file hash**: `d09f862354bd17e64c5019462ebf592e3b7a240b4b0da970d905c5be6997b75c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `1a06a0817b4a5a12857ef63b805819549f6ae5e0d73f1b045013d01fd526aaba` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `e34c3f73936759fe` (xxhash64); replay all_match = TRUE (byte-identical).
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
