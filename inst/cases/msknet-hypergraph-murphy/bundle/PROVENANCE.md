# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: msknet-hypergraph-murphy
- **Dataset**: Human musculoskeletal hypergraph (Murphy et al. 2018, PLoS Biology, CC-BY 4.0), bundled in PhysioMSKNet: the bone-by-muscle incidence matrix (173 x 270) + the cortical-homunculus correspondence data
- **Hypothesis (pre-registered)**: Building the whole-body muscle-bone hypergraph (bones = vertices, muscles = hyperedges) reproduces Murphy et al. 2018: 173 bones and 270 muscles, and a muscle's structural impact corresponds to its cortical motor-homunculus representation (R^2 ~ 0.52, significant).
- **Prereg file hash**: `de3a3ff48dc2737bf61eefb6f1b4e59f421113ed1b79ee85b519f997d71bd164` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `b06278c5077f1f30f9256a044db3fd7df37285ae7ce3ac0d6fd3f8cd45b044f0` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
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
