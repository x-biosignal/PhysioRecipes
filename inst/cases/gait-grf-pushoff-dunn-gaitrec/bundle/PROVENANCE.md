# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-pushoff-dunn-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); Dunn's test (Bonferroni) of the vertical-GRF push-off peak (grfLandmarks 3rd landmark) across the five gait classes
- **Hypothesis (pre-registered)**: In Dunn's post-hoc of the vertical-GRF push-off peak across GaitRec's five gait classes, healthy controls differ from all four pathology classes AND -- unlike the dynamic range -- several pathology-pathology pairs also differ; the newly-authored dunnTest reproduces the PMCMRplus package and scikit_posthocs.posthoc_dunn to machine precision.
- **Prereg file hash**: `a9101687aca85e9fda2678be5d972d14512724259b5d909300e693a2e6a01103` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `eff6d473810afc8b9198af015a697a2fee20ea88b91e74d0b6d78d935cfad342` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `a1a85e524a825d4e` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 10/10 grounded, 0 artifact-mismatch (`verification_report.json`).
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
