# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: emg-network-grabmyo
- **Dataset**: GRABMyo (PhysioNet v1.1.0), session1 participant1, forearm EMG channels 1-10 @ 2048 Hz; split-half reproducibility of four connectivity estimators
- **Hypothesis (pre-registered)**: On real GRABMyo forearm EMG (10-muscle set), the ecosystem's inter-muscle coordination network reproduces across two independent data halves: coherence edges and topology reproduce near-perfectly (edge r ~0.99, node-strength r ~0.997), and the partial-coherence, wPLI, and directed-Granger EDGES reproduce too (r >= 0.83) -- the connectivity structure is signal, not split-specific noise.
- **Prereg file hash**: `e1a309326e70b0c70494d4982788d3f215be2b8c610d3e12b4cb4b05ef6d212a` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `487a0ed5635939db9336fe14cd13b4bd5fe2c2720cd0ed057bcf778127db84e3` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `7528cfb0de83f008` (xxhash64); replay all_match = TRUE (byte-identical).
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
