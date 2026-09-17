# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: hti-tinn-fantasia
- **Dataset**: Fantasia Database (PhysioNet), record f1y01, a 5-minute RR-interval series (392 intervals, ms)
- **Hypothesis (pre-registered)**: On a real 5-minute RR series (Fantasia f1y01), ecgHRVgeometric reproduces NeuroKit2 hrv_time HTI (HRV_HTI) BIT-FOR-BIT -- an integer-ratio index (interval count / modal histogram height at the 1/128 s standard bin); TINN differs by a documented triangular-interpolation convention (a least-squares triangle base width vs NeuroKit2's fit).
- **Prereg file hash**: `efbfd150de33d91e93efd4b1744c0b313c45afb581ac1152a73871853875a6c2` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `58dcabf2fd69333004a64d5b1be987f90a30ede7918680e12a9ece4120b837fa` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `df83a0d5f1c0600f` (xxhash64); replay all_match = TRUE (byte-identical).
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
