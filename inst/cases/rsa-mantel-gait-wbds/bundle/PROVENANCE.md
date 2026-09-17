# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: rsa-mantel-gait-wbds
- **Dataset**: WBDS (Fukuchi, Fukuchi & Duarte 2018, figshare 5722711, CC-BY 4.0): sagittal knee + ankle flexion angles (kinematics) and antero-posterior + vertical GRF (kinetics), time-aligned and down-sampled to 150 samples; WBDS01 for the terminal proof, all five subjects (WBDS01-05) for the robustness benchmark
- **Hypothesis (pre-registered)**: The representational geometry of gait kinematics (the sagittal knee + ankle flexion angles) matches that of the kinetics (antero-posterior + vertical GRF): the Mantel correlation between the two Euclidean dissimilarity matrices (RDMs) is substantially > 0 and significant by permutation on real WBDS treadmill-walking data, and representationalSimilarity reproduces the canonical vegan::mantel to machine precision.
- **Prereg file hash**: `659fd5729245750320484edb74d0e0b1724fc96fda4e8c8656aa2992ecb66f92` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `502484a6b25a8f11f6a0be9a8d6c6bab1d280ddfd4aed0a1f62f0ed77096f1e7` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `ca7a25ccdac036c8` (xxhash64); replay all_match = TRUE (byte-identical).
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
