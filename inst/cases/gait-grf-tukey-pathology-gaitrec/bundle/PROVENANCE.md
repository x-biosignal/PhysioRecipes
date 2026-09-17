# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-tukey-pathology-gaitrec
- **Dataset**: GaitRec (Horsak et al. 2020); Tukey HSD of the vertical-GRF dynamic range (peak1 - trough via PhysioMoCap::grfLandmarks) across the five gait classes
- **Hypothesis (pre-registered)**: In the Tukey HSD post-hoc of the vertical-GRF dynamic range across GaitRec's five gait classes, healthy controls differ significantly from all four pathology classes while the pathology classes do not differ from one another; the newly-authored tukeyHSD reproduces base R stats::TukeyHSD and scipy.stats.tukey_hsd to machine precision.
- **Prereg file hash**: `60a7b9556aa67205ecb080ff8c0b13f5a7f96653aca8cd5f0b79fb4fa852ea07` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `45b279e6e8537fd2f9d78e33f6005b4299be8d82053a35ffd0ac31106decb5d0` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `b9891d9c82fcacad` (xxhash64); replay all_match = TRUE (byte-identical).
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
