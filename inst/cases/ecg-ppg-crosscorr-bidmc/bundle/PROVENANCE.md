# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ecg-ppg-crosscorr-bidmc
- **Dataset**: BIDMC PPG and Respiration Dataset (Pimentel et al. 2017, PhysioNet), subject bidmc01; simultaneous lead-II ECG and fingertip PPG at 125 Hz, 4 min (30000 samples each)
- **Hypothesis (pre-registered)**: On a real simultaneous ECG + PPG recording (BIDMC subject 01), the time-lagged cross-correlation between the ECG and the fingertip PPG peaks at a lag of a few hundred milliseconds -- the pulse arrival time -- and crossCorrelation reproduces an independent from-scratch normalized cross-correlation to machine precision, with the peak lag matching scipy.signal.correlate.
- **Prereg file hash**: `86cd344d1620633acc065b39b30173bf9ec7e0612657f8ca6d68a6afffaee39b` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `2f0ac71c7cd20f953267e2d161a92e38d3345e344a8bb83573ed8d3ae93ae4c4` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `f474896aa1ba3996` (xxhash64); replay all_match = TRUE (byte-identical).
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
