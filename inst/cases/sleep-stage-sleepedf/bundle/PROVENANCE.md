# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sleep-stage-sleepedf
- **Dataset**: Sleep-EDF Expanded (PhysioNet), night SC4001, EEG Fpz-Cz + Pz-Oz @ 100 Hz, 30 s epochs, expert AASM hypnogram
- **Hypothesis (pre-registered)**: On real overnight polysomnography (Sleep-EDF night SC4001), the per-epoch EEG spectra grouped by the expert AASM hypnogram recover the textbook per-stage fingerprints: N3 is the most delta-dominated stage (relative delta ~0.92), the spectrum slows monotonically N1<N2<N3, and N2 carries the sigma-band (spindle) peak.
- **Prereg file hash**: `741f524cf1fc457afa70d8c969ef4d5e998be19606dca88fa7b161223d7f31dd` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `b5187777230eed69b3cc35dd7760ac40d6b0838adae240bc3e2c306ea5d5007d` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `2d1a5ac87d123de5` (xxhash64); replay all_match = TRUE (byte-identical).
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
