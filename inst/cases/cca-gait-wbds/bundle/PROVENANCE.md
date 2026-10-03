# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: cca-gait-wbds
- **Dataset**: WBDS (Fukuchi, Fukuchi & Duarte 2018, figshare 5722711, CC-BY 4.0): sagittal knee + ankle flexion angles (kinematics) and antero-posterior + vertical GRF (kinetics), time-aligned to 450 samples; WBDS01 for the terminal proof, all five subjects for the robustness benchmark (the SAME blocks as the dCor and RSA cases)
- **Hypothesis (pre-registered)**: The gait kinematics (sagittal knee + ankle flexion angles) and kinetics (antero-posterior + vertical GRF) have a strong linear canonical relationship: the first canonical correlation is substantially > 0 on real WBDS treadmill-walking data, and cca reproduces base R's stats::cancor to machine precision.
- **Prereg file hash**: `a37599c07687a378a36e670eaf180d7c1e783243a800978dbb646c650cfd7fb3` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `be1aafa471cd9139ad95a65ec31faee1048a08e5bc5a81e39c44df9335bee5fe` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `d9be5f49b912bcc9` (xxhash64); replay all_match = TRUE (byte-identical).
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
