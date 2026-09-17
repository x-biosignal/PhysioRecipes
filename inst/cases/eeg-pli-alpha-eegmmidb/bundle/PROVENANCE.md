# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-pli-alpha-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002 baseline run R02 (eyes-closed), occipital channels O1 and Oz, first 10 s at 160 Hz (1600 samples each)
- **Hypothesis (pre-registered)**: On the same real occipital O1-Oz pair whose alpha PLV is 0.92 (near zero phase lag), the phase-lag index (PLI, which is ~0 for zero-lag coupling) is LOW -- the high PLV is dominated by volume conduction / common reference, not lagged neural coupling; phaseLagIndex reproduces an independent scipy Hilbert-band PLI and recovers ground truth with the contrast (constructed zero-lag -> PLI~0 while PLV~1; lagged -> PLI high; independent -> both ~0).
- **Prereg file hash**: `2a6338aab704a432aad90166df3ef573d3ab1fd98e0a3e1df21d2a8afbfaf23c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `a4bc4c2895d1db55177a40e6ced2399aeb092ef758120b9d10f551c48d2840cf` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `c92b97116a5bb468` (xxhash64); replay all_match = TRUE (byte-identical).
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
