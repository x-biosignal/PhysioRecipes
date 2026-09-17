# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: mutual-info-cardioresp-bidmc
- **Dataset**: BIDMC PPG and Respiration Dataset (PhysioNet), subject 01, RESP + PLETH decimated to 25 Hz, 200 s (5001 samples each)
- **Hypothesis (pre-registered)**: On real cardiorespiratory signals (BIDMC-01 RESP + PLETH), the newly-authored mutualInformation (histogram estimator, 16 equal-width bins, nats) reproduces sklearn.metrics.mutual_info_score on the identical binning BIT-FOR-BIT; and the mutual information of the real pair (~0.077 nats) exceeds a shuffled-surrogate control (~0.024, the histogram estimator's finite-sample bias) -- a genuine undirected dependence (the respiratory modulation shared by the two signals).
- **Prereg file hash**: `1ded6784d11ff26b624a864524a07f93b3a03b976d6b1022d2888b4116ebcb34` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `3fccf3db514c5ae61608be4c0d6039329d56c849cb5e7da984d7a6111906e642` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `eb6ca2dd324c1570` (xxhash64); replay all_match = TRUE (byte-identical).
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
