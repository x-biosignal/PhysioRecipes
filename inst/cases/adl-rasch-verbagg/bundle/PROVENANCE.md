# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-rasch-verbagg
- **Dataset**: lme4::VerbAgg, 316 persons x 24 three-category verbal-aggression items (a labelled stand-in for a polytomous ADL/IADL response matrix)
- **Hypothesis (pre-registered)**: On the VerbAgg Partial Credit Model benchmark (316 persons x 24 three-category items), pcm_measure's JMLE item locations and person measures reproduce the eRm CML reference (Spearman/Pearson agreement ~ 1.0), with a person separation reliability of ~0.86.
- **Prereg file hash**: `a6e104bd333ad3fddbb98dd67fe95bf07b0e85870b7d77c59969ef29382b2899` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `49827c4bec26b5de355d3edb69ccb86973ff09ff7ac1cda4a6a3fc4bbdfcca17` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `48e91ae7804cc87c` (xxhash64); replay all_match = TRUE (byte-identical).
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
