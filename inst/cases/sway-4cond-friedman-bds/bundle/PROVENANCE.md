# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-4cond-friedman-bds
- **Dataset**: Santos & Duarte (2016) BDS; per-subject mean COP path length (PhysioMoCap::swayMetrics) in each of the four vision x surface quiet-standing conditions, complete blocks only
- **Hypothesis (pre-registered)**: The four vision x surface quiet-standing conditions (Open-Firm, Closed-Firm, Open-Foam, Closed-Foam) differ in COP path length across the 158 subjects measured under all four; the newly-authored friedmanTest reproduces base R stats::friedman.test BIT-FOR-BIT and scipy.stats.friedmanchisquare to machine precision. The per-condition mean ranks increase monotonically Open-Firm < Closed-Firm < Open-Foam < Closed-Foam.
- **Prereg file hash**: `ffc71c2a2b65b9d3e54d08d269790305dac54775e202c3e5610a2dfc50229fb0` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `7d31dbaa2b458835132ab3fd4c88352469bc1f61bd2f4bf257bd55b53714f14c` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `565d7c1095c79a17` (xxhash64); replay all_match = TRUE (byte-identical).
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
