# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: hrv-lomb-fantasia
- **Dataset**: Fantasia Database (PhysioNet), young subject f1y01; the RR-interval tachogram (channel, rr_ms, time_sec; 8710 beats) derived offline from the real ECG (readWFDB -> ecgDetectRpeaks -> ecgRRintervals, 300-2000 ms) and git-tracked
- **Hypothesis (pre-registered)**: On a real RR tachogram (Fantasia young subject f1y01), the Lomb-Scargle periodogram computed by ecgHRVfreq(method='lomb') reproduces scipy.signal.lombscargle to machine precision (both the raw periodogram and the integrated VLF/LF/HF band powers), and the autonomic balance is HF-dominant (LF/HF < 1) as expected for a healthy young adult at rest.
- **Prereg file hash**: `e003fd3ad308324f8b52d9c5a0b9b32f2f9a92ea1675000a0c50ce9fd45247f0` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `376448fd444d45ab2b88d25ee8a506d414155ed75cbab9d2824dc14443c701d5` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `de9f50bb81171a51` (xxhash64); replay all_match = TRUE (byte-identical).
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
