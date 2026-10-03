# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: cohort-longitudinal-parkinsons-updrs
- **Dataset**: UCI Parkinson's Telemonitoring (Tsanas et al. 2010), 42 early-stage PD patients, 5875 voice recordings over ~6 months
- **Hypothesis (pre-registered)**: In the UCI Parkinson's Telemonitoring cohort (42 patients, ~5875 visits), a random-intercept mixed model total_UPDRS ~ test_time + age + sex + PPE + (1|subject) reproduces lme4::lmer to machine precision, with a positive test_time slope (progression over ~6 months).
- **Prereg file hash**: `b7707ef660ea6872e5d50b309f1723f221e5b1c77eca672311d725aa496b1094` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `c5cc429dde725b5d10979ddd104116c4bf553ff48f96d51fa66bc54b27a41436` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `939fd1e6d587c7e4` (xxhash64); replay all_match = TRUE (byte-identical).
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
