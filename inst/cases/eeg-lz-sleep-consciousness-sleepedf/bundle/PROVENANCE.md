# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-lz-sleep-consciousness-sleepedf
- **Dataset**: Sleep-EDF Expanded (PhysioNet sleep-edfx), subject SC4001, EEG Fpz-Cz at 100 Hz; 60-s fixed-length concatenated EEG for each stage (Wake / N2 / N3 / REM) from the expert hypnogram
- **Hypothesis (pre-registered)**: On a real overnight EEG (Sleep-EDF SC4001, Fpz-Cz), the Lempel-Ziv complexity of the cortex is LOWEST in deep sleep (N3) and higher in wake and REM -- the consciousness/complexity gradient -- and eegComplexity's Lempel-Ziv measure reproduces the canonical Python antropy.lziv_complexity to machine precision.
- **Prereg file hash**: `b79b8deae2d75e758c4d612fbc740cf74bacd4a606a3939001a21009dfb9c344` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `e58579f533b385bda4dce968bf81ea6597b5b82cef516cb6223deb8ec58cd686` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `cb27a7954e6cc6bf` (xxhash64); replay all_match = TRUE (byte-identical).
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
