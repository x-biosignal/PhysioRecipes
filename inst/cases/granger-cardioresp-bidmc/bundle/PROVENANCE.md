# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: granger-cardioresp-bidmc
- **Dataset**: BIDMC PPG and Respiration Dataset (Pimentel et al. 2017, PhysioNet), subject bidmc01; simultaneous RESP (impedance pneumography) and PLETH (PPG), decimated 125->25 Hz, a 200 s segment (5001 samples each)
- **Hypothesis (pre-registered)**: On a real simultaneous respiration + PPG recording (BIDMC subject 01), time-domain Granger causality is strong and BIDIRECTIONAL (cardiorespiratory coupling), with the respiration->pulse direction slightly dominant (respiration modulates the peripheral pulse), and grangerCausality reproduces the field-standard statsmodels.tsa.stattools.grangercausalitytests (and an independent numpy OLS) on the real signals.
- **Prereg file hash**: `5e258c31fdbba12984fb3e40752528b49c64e2579a8947239d38b06a7d6767a2` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `cad348cc22fbd032c7d1a430c097e07c6e3759351e8547b5a32de38b59adf339` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `1da8ceef491ad8d5` (xxhash64); replay all_match = TRUE (byte-identical).
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
