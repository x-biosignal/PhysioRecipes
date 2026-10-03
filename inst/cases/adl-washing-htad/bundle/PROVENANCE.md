# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-washing-htad
- **Dataset**: HTAD (figshare 6667532), 3 subjects, wrist accelerometer @ ~31 Hz; 7 home tasks (washing/grooming/eating/sweeping/mopping/typing/watch_tv); leave-one-subject-out kNN
- **Hypothesis (pre-registered)**: Under strict leave-one-subject-out on real wrist accelerometry (HTAD, 3 subjects, 7 home tasks), washing hands (ICF d510) is recognised ABOVE the 1/7 chance level (~0.14) -- recall ~0.53, about 3.7x chance -- and 7-task accuracy is ~0.63. Washing carries a wrist-detectable signature, though on only 3 subjects this is a demonstration, not a definitive validation.
- **Prereg file hash**: `7420bbbe55a8f7823ad248c16075b036be4184f59a2ca0015893a0c431dc8296` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `ac751c71ccfb9381e339e47421c93df4f0b53c405d6b7acd03d1cca13c446b25` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `b789aaf95d81a377` (xxhash64); replay all_match = TRUE (byte-identical).
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
