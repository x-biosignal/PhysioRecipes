# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: adl-upperlimb-use-dsads
- **Dataset**: DSADS (UCI #256), subject p1, right-arm + left-arm accelerometers @ 25 Hz, 19 activities x 60 five-second segments, converted to g
- **Hypothesis (pre-registered)**: On real dual-arm accelerometry from a HEALTHY subject (DSADS p1, 19 activities), the two arms are used near-symmetrically: the bilateral use ratio is close to 1 and the magnitude ratio close to 0 (the affected/unaffected asymmetry a stroke arm would show is absent).
- **Prereg file hash**: `29010095687847081222c055dea5dc1d3cfbba4970cccfcede1521c21a8d371c` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `bae5a07d7b948402e92d2068fcc388ae220bf055f6493b73156b0001abb14d72` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `9ca870e520d095f0` (xxhash64); replay all_match = TRUE (byte-identical).
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
