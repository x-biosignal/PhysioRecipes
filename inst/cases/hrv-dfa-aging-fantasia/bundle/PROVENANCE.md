# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: hrv-dfa-aging-fantasia
- **Dataset**: Fantasia (Iyengar et al. 1996, PhysioNet): young (f1y01-05) and elderly (f1o01-05) healthy subjects; RR intervals derived from the ECG (readWFDB -> ecgDetectRpeaks -> ecgRRintervals), physiologically filtered to 300-2000 ms
- **Hypothesis (pre-registered)**: The short-term DFA scaling exponent (alpha1) of RR intervals is HIGHER in elderly than in young healthy subjects (loss of fractal complexity with aging) on the real Fantasia recordings, and ecgDFA reproduces an independent standard-DFA implementation to machine precision.
- **Prereg file hash**: `cc9011a4b14697cc5ae413cf80a6e24f30a529cd7d6840f8d1e83902d8c47ea2` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `914f01a7654173c2a456f4592f3d1aace0720a5055b81ad02d947ecfd776ff2c` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `daed3d426c5b9255` (xxhash64); replay all_match = TRUE (byte-identical).
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
