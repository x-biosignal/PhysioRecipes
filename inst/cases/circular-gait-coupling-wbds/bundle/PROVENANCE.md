# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: circular-gait-coupling-wbds
- **Dataset**: WBDS (Fukuchi, Fukuchi & Duarte 2018, figshare 5722711, CC-BY 4.0): the knee-ankle vector-coding coupling angles (degrees) over one gait cycle of subject WBDS01 (449 angles); all five subjects for the robustness benchmark
- **Hypothesis (pre-registered)**: The vector-coding coupling angles of the knee-ankle pair over a real WBDS gait cycle have a well-defined mean direction and mean resultant length (R-bar), and circularSummary reproduces the canonical `circular` package (mean.circular, rho.circular) to machine precision; the coupling angles are significantly non-uniform (Rayleigh test).
- **Prereg file hash**: `8319d29a162d542fe452efcdfd549efdf25a245ca329f6750a79991aa2f64903` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `9aac44c60b00a82e5a2b15a1a1bd6adb20e2252342a84f433a0745c901ccd5dc` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `59c64f0cfe61bf0a` (xxhash64); replay all_match = TRUE (byte-identical).
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
