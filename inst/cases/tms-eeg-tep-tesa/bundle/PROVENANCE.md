# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: tms-eeg-tep-tesa
- **Dataset**: TESA example TMS-EEG (figshare 3188800), one participant, 150 TMS pulses over left parietal cortex; the baseline-corrected average TEP over 59 channels (time -250..450 ms)
- **Hypothesis (pre-registered)**: Running setTMSpulses + tepAverage on the real TESA TMS-EEG average, all six canonical TEP components (N15/P30/N45/P60/N100/P180) are recovered in the correct temporal ORDER (monotonically increasing median latencies) and with the correct POLARITIES (peak sign matches the expected N/P in the large majority of channels), the N100 (~115 ms) and P180 (~188 ms) at their literature latencies.
- **Prereg file hash**: `30d65c669645eac7f3ec13a1c9aeb50fae8e6855fdb1241ee34a0c2173412ef8` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `c56c359dca2204a99585a16ae85827fe82b86bc966f391052fe2ed3a2b2c2bc6` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
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
