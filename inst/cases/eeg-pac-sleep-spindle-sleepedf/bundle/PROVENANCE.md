# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-pac-sleep-spindle-sleepedf
- **Dataset**: Sleep-EDF Expanded (PhysioNet sleep-edfx), subject SC4001, EEG Fpz-Cz at 100 Hz; the first 30 min of concatenated NREM (N2+N3) epochs (from the expert hypnogram)
- **Hypothesis (pre-registered)**: On the NREM (N2+N3) EEG of one real overnight polysomnogram (Sleep-EDF SC4001, Fpz-Cz), the amplitude of the sleep-spindle band (12-15 Hz) is coupled to the phase of the slow oscillation (0.5-1.25 Hz): the Tort modulation index is well above a circular-shift surrogate null, and phaseAmplitudeCoupling reproduces the canonical Python tensorpac to machine precision.
- **Prereg file hash**: `a45a7cf7fa6a3b178225bbade6ff7e7ab3f0c6c22200457f14bda64d8dbee51f` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `d3d0b654765e39bc4b87cf1eeb3685f28c659bcce70458f33b19829e504dfc04` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `7f7a0d8e469e61e9` (xxhash64); replay all_match = TRUE (byte-identical).
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
