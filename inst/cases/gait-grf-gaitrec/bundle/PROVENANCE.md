# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-grf-gaitrec
- **Dataset**: GaitRec (figshare collection 4788012), processed vertical GRF (F_V_PRO left+right); HC self-selected speed + standardised footwear (208 subjects) vs K at initial presentation + standardised footwear (499 subjects); per-subject stance-normalised body-weight curves (101 pts).
- **Hypothesis (pre-registered)**: On real GaitRec vertical GRF, time-normalised to the stance phase in body-weight units, the knee-pathology cohort (K) shows the classic reduced weight-acceptance modulation versus healthy controls (HC): a lower loading (first) peak and a raised mid-stance trough -- a flatter double hump.
- **Prereg file hash**: `62dbf2d7069e1ae2a67af8d1cfea71a3f17a12b9c659db3bf2acd88bb36f722a` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `7502c402d609bd4bd722afdeb4b1786d742e0d61f7384dcee7d7218c0f186235` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `06af0226ecad4f93` (xxhash64); replay all_match = TRUE (byte-identical).
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
