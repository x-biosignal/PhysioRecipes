# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: poincare-hrv-fantasia
- **Dataset**: Fantasia Database (PhysioNet), subject f1y01 (young healthy adult), the first 5-minute RR window (time <= 300 s, 392 RR intervals), RR in integer ms derived at 250 Hz
- **Hypothesis (pre-registered)**: On a real 5-minute RR window (Fantasia f1y01, a young healthy adult), ecgHRVpoincare's SD1/SD2/ratio reproduce an independent from-scratch numpy implementation of the analytical closed-form (Brennan 2001, unbiased n-1 variance) BIT-FOR-BIT, and NeuroKit2 hrv_nonlinear: SD1 bit-for-bit (the universal SDSD/sqrt(2)); SD2 up to a documented ~0.2 ms convention (the op uses the analytical closed-form SD2^2 = 2*SDNN^2 - 0.5*SDSD^2; NeuroKit2 uses the geometric paired-projection std((RR_n+RR_n+1)/sqrt(2)), which an independent numpy paired projection reproduces bit-for-bit).
- **Prereg file hash**: `f6b679f5df05fec611aff372ea98dfef11ed856ff4c269c8a43b5622ace606f1` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `fb76a4dbf43b444805fa81e4b130731a7b43505aa35208f65835789f0b0daa71` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `90ede085667d7311` (xxhash64); replay all_match = TRUE (byte-identical).
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
