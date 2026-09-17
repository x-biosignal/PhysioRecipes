# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adf-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), the newly-authored adfTest reproduces the statsmodels.tsa.stattools.adfuller(autolag=None) statistic BIT-FOR-BIT; and the statistic lies well below the 5% Dickey-Fuller critical value, rejecting the unit-root null in favour of stationarity.
- **Prereg file hash**: `8fc10473d5725e5b36666a238c56286d7e62508211d48444d09e8e6164c2a199` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `fb12ab9146a2ec5827391bb09689a2b67a75303826f781b1d762238d8bfa9717` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `9d5ba99edf5d4ff0` (xxhash64); replay all_match = TRUE (byte-identical).
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
