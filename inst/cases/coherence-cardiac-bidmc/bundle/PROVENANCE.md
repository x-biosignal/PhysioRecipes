# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: coherence-cardiac-bidmc
- **Dataset**: BIDMC PPG and Respiration Dataset (Pimentel et al. 2017, PhysioNet), subject bidmc01; simultaneous PLETH (PPG) and lead-II (ECG) at 125 Hz, first 4 min (30000 samples)
- **Hypothesis (pre-registered)**: On a real simultaneous PPG + ECG recording (BIDMC subject 01), the magnitude-squared coherence between the optical PPG and the electrical ECG has a strong peak at the heart-rate frequency (both sense the same cardiac rhythm), and coherence reproduces the canonical scipy.signal.coherence to machine precision.
- **Prereg file hash**: `e5e9ec9b90a81da30afe7a243fd3cc0dd63446dd3b595f0ddef43cab5fff14ed` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `5f9f7b2fb5581bc3a26e179496bcdd01f3899645bd1b7f9230f222f3b7f0cf74` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `d9b66d7d9f5a26e4` (xxhash64); replay all_match = TRUE (byte-identical).
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
