# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: median-abs-dev-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), the newly-authored medianAbsDev (raw MAD, constant=1) reproduces BOTH scipy.stats.median_abs_deviation AND base R stats::mad(constant=1) BIT-FOR-BIT; and the normal-consistent robust SD estimate (MAD x 1/qnorm(0.75)) closely matches the population SD, indicating a near-Gaussian, artifact-free distribution.
- **Prereg file hash**: `d88dc710540e3ab1f53a6bf30ba530ac934cad67239eb77c9f460061e0e10521` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `6b286d1ad0484e4acebc80a8937300c5d5d9f65be64c50a309fc83f05d3662c3` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `dd270ef2c2f64fc3` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 7/7 grounded, 0 artifact-mismatch (`verification_report.json`).
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
