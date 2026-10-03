# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: hra-fantasia
- **Dataset**: Fantasia Database (PhysioNet), subject f1y01 (young healthy adult), the first 5-minute RR window (392 RR intervals, integer ms at 250 Hz)
- **Hypothesis (pre-registered)**: On a real 5-minute RR window (Fantasia f1y01), the newly-authored ecgHRVasymmetry reproduces NeuroKit2 hrv_nonlinear's heart-rate-asymmetry indices (GI/SI/PI + the deceleration/acceleration contributions C1d/C1a/C2d/C2a) BIT-FOR-BIT; and decelerations contribute MORE than accelerations to short-term variability (C1d > C1a), the established HRA signature.
- **Prereg file hash**: `79031516be6e6f4cac1bd51c8063ba566480f5a067584438e03b098b7f4a999e` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `00b541fa25af0e763136eb1e586cf705a859a09717dcca8c18d41fbb3b00bffb` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `c8616af1eb506522` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 9/9 grounded, 0 artifact-mismatch (`verification_report.json`).
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
