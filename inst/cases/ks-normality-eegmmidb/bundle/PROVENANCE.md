# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: ks-normality-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), the newly-authored ksNormalityTest reproduces BOTH scipy.stats.kstest AND base R ks.test D statistic BIT-FOR-BIT; and KS does NOT reject normality (its p-value exceeds 0.05) even though Jarque-Bera does -- the moment-based and CDF-based normality tests disagree.
- **Prereg file hash**: `079c1b3593d7d94bcf6303754bbce5f8fb0a83fe4f767c01888d562408033181` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `572b4ca90271a695d58e9eb20cad035fd15b0be676225a934cfee9fb2ba13e7a` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `474814269f5cc0fb` (xxhash64); replay all_match = TRUE (byte-identical).
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
