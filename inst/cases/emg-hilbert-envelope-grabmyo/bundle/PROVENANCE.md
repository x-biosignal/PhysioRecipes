# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: emg-hilbert-envelope-grabmyo
- **Dataset**: GRABMyo forearm surface EMG (Pradhan et al. 2022, PhysioNet), session1 participant1 gesture10 trial1; 32 channels x 10240 samples at 2048 Hz
- **Hypothesis (pre-registered)**: On a real 32-channel forearm surface-EMG gesture (GRABMyo), the Hilbert amplitude envelope computed by emgEnvelope(method='hilbert') reproduces the canonical scipy.signal.hilbert (the analytic-signal magnitude) to machine precision on every channel, and the envelope shows clear burst activity (peak/mean modulation > 1) -- the gesture's muscle activation.
- **Prereg file hash**: `a2ceeb66fbbe25440dfc955259527169d9fdc7e005e29840999a0298b9e22c15` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `363e2d2e9e214dfe93f05b37b2381a43ace8e912ebff0c3f3e46ae837382f4c1` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
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
