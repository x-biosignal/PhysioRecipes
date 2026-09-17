# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: gait-inverse-dynamics-fukuchi
- **Dataset**: WBDS (figshare 5722711), 5 subjects (WBDS01-05), self-selected-speed treadmill walking; inputs = right-limb sagittal joint-centre markers + right-belt GRF, reference = the dataset's own knt joint moments
- **Hypothesis (pre-registered)**: Driving inverseDynamics2D (Newton-Euler, de Leva inertia) with real WBDS markers + GRF recovers the sagittal ankle/knee/hip moments, validated against the dataset's own moments (knt) with the textbook distal-to-proximal accuracy gradient: ankle r~0.97 (physiological push-off peak), knee r~0.85, hip r~0.77 (5 subjects).
- **Prereg file hash**: `39cb1a0e1b22f378cfb057ab4029761e54164882e5391ea36410bca7e5a7dad9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `5ed4f52567f8af173dbb8a08b45a531c2eaae2d8885a398c304206c0d0360aa4` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `5140e5fdfb7754a8` (xxhash64); replay all_match = TRUE (byte-identical).
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
