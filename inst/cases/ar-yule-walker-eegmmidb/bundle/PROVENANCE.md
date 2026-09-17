# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ar-yule-walker-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), the newly-authored arYuleWalker (Durbin-Levinson on the biased ACF) reproduces statsmodels.regression.yule_walker(method='mle') BIT-FOR-BIT for both the AR coefficients and the innovation variance; and the fitted AR(4) is stationary (all roots of the AR polynomial lie outside the unit circle).
- **Prereg file hash**: `4148e55c8f1871cef3309f3da5ccb4db28be0e8e4d1f1adba7a2abd6e6052bf8` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `f31e456b2fda8730906388a1d0b1c0b7537604c4d74378c32cc24439904ae214` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `3c0b0e4e5fb91253` (xxhash64); replay all_match = TRUE (byte-identical).
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
