# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: age-group-sway-bds
- **Dataset**: Santos & Duarte (2016) balance dataset (figshare); foam-surface COP path length (PhysioMoCap::swayMetrics) for older (n=11) vs younger (n=39) subjects
- **Hypothesis (pre-registered)**: Older subjects (n=11) have greater foam-surface COP path length than younger subjects (n=39); the newly-authored twoSampleTTest (Welch) reproduces scipy.stats.ttest_ind(equal_var=FALSE) AND base R t.test BIT-FOR-BIT.
- **Prereg file hash**: `bbadad3976eb2347be3cdd4fb784c46ef9a2d1d1f0c17a882c2eabc4c4e04c5c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `65a9bb557c9e6046881aa80837dc89a96831a4959bbdb85a1da9d23c6ed3ce97` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `397ea97692e06a13` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 8/8 grounded, 0 artifact-mismatch (`verification_report.json`).
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
