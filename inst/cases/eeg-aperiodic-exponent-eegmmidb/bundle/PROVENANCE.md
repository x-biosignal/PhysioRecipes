# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-aperiodic-exponent-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S001, baseline run R02 (eyes-closed rest), all 64 channels, 160 Hz, ~61 s
- **Hypothesis (pre-registered)**: On the eyes-closed resting EEG of eegmmidb S001 (run R02, 64 channels, 160 Hz), the aperiodic exponent estimated by eegAperiodic (specparam/FOOOF engine, Donoghue et al. 2020) reproduces the canonical Python fooof to a strong cross-tool agreement: the per-channel exponents correlate r ~ 0.98 across the 64 channels, with a small mean absolute difference, and both engines yield physiologically plausible resting exponents (~1.4).
- **Prereg file hash**: `96ad234c4c64d6ce3447202d09f14cbbd962dbd5af8bdbcf62d9bc1338307d7b` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `04762ba77dd58e1405e2f17306886546a1d70af5679989589dda36f2b9b27c1f` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `cc027aaf289589a9` (xxhash64); replay all_match = TRUE (byte-identical).
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
