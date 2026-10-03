# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: csi-cvi-fantasia
- **Dataset**: Fantasia Database (PhysioNet), subject f1y01 (young healthy adult), the first 5-minute RR window (392 RR intervals, integer ms at 250 Hz)
- **Hypothesis (pre-registered)**: On a real 5-minute RR window (Fantasia f1y01), the newly-authored ecgHRVautonomic reproduces NeuroKit2 hrv_nonlinear's Toichi cardiac autonomic indices (CSI, CVI, CSI_Modified) BIT-FOR-BIT; the indices are physiologic (CSI ~ 1.5, CVI ~ 4.8), and the Cardiac Vagal Index is higher in young than old subjects (parasympathetic decline with age).
- **Prereg file hash**: `651cb647a9a5c9eb3df657ec7369278e144d0acc4e1d797d3dbe8e614340b1c2` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `f92c703e146058208fd6a113f6c2def1502504494c07c276c412d3d270192390` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `a31c2746d980e785` (xxhash64); replay all_match = TRUE (byte-identical).
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
