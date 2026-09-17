# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: te-cardioresp-bidmc
- **Dataset**: BIDMC PPG and Respiration Dataset (Pimentel et al. 2017, PhysioNet), subject bidmc01; RESP + PLETH decimated 125->25 Hz, 200 s (5001 samples each)
- **Hypothesis (pre-registered)**: On real simultaneous respiration + PPG (BIDMC subject 01), the histogram transfer entropy shows directed information flow (respiration -> pulse slightly net-dominant, the model-free complement to the Granger result), transferEntropy reproduces an independent from-scratch numpy transfer entropy, and it recovers a constructed directed coupling (x -> y net TE strongly positive).
- **Prereg file hash**: `a3abd861786ef32b2de32fdcaaa9b6a41f16610f84629fbdcb162b8a5ee5e4e6` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `34d6a34db44613fa69aaa3daac5641f7301a13c11f87ede201ce1ea5cdadd7ef` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `46617f040a0b646c` (xxhash64); replay all_match = TRUE (byte-identical).
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
