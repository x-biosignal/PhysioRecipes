# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: crossmodal-dcor-gait-wbds
- **Dataset**: WBDS (Fukuchi, Fukuchi & Duarte 2018, figshare 5722711, CC-BY 4.0): sagittal knee + ankle flexion angles (kinematics, marker-derived, translation-invariant) and antero-posterior + vertical GRF (kinetics), time-aligned and down-sampled to 450 samples; WBDS01 for the terminal proof, all five subjects (WBDS01-05) for the robustness benchmark
- **Hypothesis (pre-registered)**: Gait kinematics (sagittal knee + ankle flexion angles) and kinetics (antero-posterior + vertical ground reaction force) are statistically dependent: their distance correlation (Szekely, Rizzo & Bakirov 2007) is substantially > 0 and significant by permutation on real WBDS treadmill-walking data, and distanceCorrelation reproduces the canonical energy::dcor to machine precision.
- **Prereg file hash**: `8723d8ad979ea3ce57ab9e3d99045d4c4bc02966aede99decac50627946a6527` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `d539f157fbd36975a7b4741dc31d27bad91ecf069640c89fdff0423b425af142` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `bd35eb6c9aef7f25` (xxhash64); replay all_match = TRUE (byte-identical).
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
