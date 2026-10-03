# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: hrv-time-neurokit-fantasia
- **Dataset**: Fantasia Database (PhysioNet), record f1y01, a 5-minute RR-interval series (392 intervals, ms)
- **Hypothesis (pre-registered)**: On a real 5-minute RR series (Fantasia f1y01), ecgHRVtime reproduces NeuroKit2 hrv_time BIT-FOR-BIT for the three core time-domain metrics (MeanNN, SDNN, RMSSD); pNN50 differs ONLY by a documented denominator convention (ecgHRVtime divides the nn50 count by the number of successive differences N-1, NeuroKit2 by the number of intervals N), with the nn50 count itself identical.
- **Prereg file hash**: `94497a8c94394f5949ad89310bd3bc60efb46fff88b0289c3e4b0366f4c76624` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `3ad1862eef91166383f9e5264807d6ec265e5b5394644b515639dbee47a69b6a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `772ea6123683f2ec` (xxhash64); replay all_match = TRUE (byte-identical).
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
