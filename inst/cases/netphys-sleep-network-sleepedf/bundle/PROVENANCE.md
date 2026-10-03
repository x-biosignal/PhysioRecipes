# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: netphys-sleep-network-sleepedf
- **Dataset**: Sleep-EDF Expanded (PhysioNet sleep-edfx), subject SC4001; 6 physiological node signals at 1 Hz over the ~6.7 h scored sleep period, with the hypnogram grouped Wake / Light / Deep / REM
- **Hypothesis (pre-registered)**: Building a 6-node time-delay-stability network (EEG delta/alpha/sigma + EOG/EMG/respiration) from one real overnight polysomnogram and splitting it by sleep stage, the network RECONFIGURES: it is most integrated in REM (most surrogate-significant links) and least in wake/light sleep, the EEG-delta rhythm is the persistent hub, and the link set turns over between wake and REM.
- **Prereg file hash**: `fe7f112fe0131bda5793ff6b5911bcc49ffebd20f81dce5e2fc820e226dd43fb` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `01550aa0ebcd0b283557f45f999d7220b8df450191755eac443f17e152bf930c` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `{}` (xxhash64); replay all_match = TRUE (byte-identical).
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
