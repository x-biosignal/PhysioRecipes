# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: sway-4cond-nemenyi-bds
- **Dataset**: Santos & Duarte (2016) BDS; Nemenyi post-hoc of per-subject COP path length (PhysioMoCap::swayMetrics) across the four vision x surface conditions, complete blocks (n=158)
- **Hypothesis (pre-registered)**: In the Nemenyi post-hoc of COP path length across the four BDS conditions, all condition pairs differ, but the vision effect (eyes-open vs eyes-closed) is much weaker on firm ground than on foam; the newly-authored nemenyiTest reproduces PMCMRplus::frdAllPairsNemenyiTest and scikit_posthocs.posthoc_nemenyi_friedman to machine precision.
- **Prereg file hash**: `9917e444fcdf143e1458be0b9059da3b0d0fc20944092cfe0b450332224b6bf0` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `5cee2042d0c6fdfb98a842be45c3b7479b5d03e4f1a23ee33d810d5eb9b317c2` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `ac11051d7a7d6590` (xxhash64); replay all_match = TRUE (byte-identical).
- **Claims (SUBS-01)**: 9/9 grounded, 0 artifact-mismatch (`verification_report.json`).
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
