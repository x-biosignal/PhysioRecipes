# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sparc-ldlj-smoothness-wbds
- **Dataset**: WBDS (Fukuchi et al. 2018, figshare) gait knee angular-speed cycle, subject 01, time-normalized to 101 points; treated as a movement speed profile at a nominal 100 Hz
- **Hypothesis (pre-registered)**: On a real WBDS gait knee angular-speed cycle, the shipped PhysioMoCap sparc and ldlj reproduce an independent Python reimplementation of the Balasubramanian et al. (2015) reference algorithm BIT-FOR-BIT; and SPARC becomes more negative (less smooth) when the movement is corrupted with noise.
- **Prereg file hash**: `7f796ecd62d708dfa3cdffe2b59c455c417f6b848d3ab1e7aad08472fd5e49be` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `ebc2ca4442e074ecc7b2304b08c84fdbfaaec734fc822692d320059b4bdce7e1` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `e6d021b8e8033c78` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 7/7 grounded, 0 artifact-mismatch (`verification_report.json`).
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
