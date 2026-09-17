# PhysioAgent provenance bundle -- verified replay

Produced by re-executing this case's frozen op-DAG spec through the
PhysioAgent certified loop (validate -> freeze -> execute -> verify -> replay).

- **Case**: eeg-spectrogram-scipy-eegmmidb
- **Dataset**: EEG Motor Movement/Imagery Database (eegmmidb, PhysioNet), subject S002, baseline run R02 (eyes-closed), channel POz (posterior), first 10 s at 160 Hz (1600 samples)
- **Hypothesis (pre-registered)**: On a real eyes-closed posterior EEG channel (eegmmidb S002R02, POz), spectrogram reproduces scipy.signal.spectrogram (symmetric Hann, nperseg=256, noverlap=128, detrend=False, scaling='density', mode='psd') BIT-FOR-BIT over the full frequency x time matrix; and the time-frequency view shows the alpha rhythm dominates every time window (peak power in 8-13 Hz throughout) while its amplitude waxes and wanes across time (a modulation the averaged Welch PSD cannot show).
- **Prereg file hash**: `d7b0423e679dcb9f3eaaf6d6dc2e9f8539a1b16004bedb28c8420124455647a9` (sha256 of `prereg.json`; bound in `case.json` verification).
- **Freeze hash (SUBS-02 identity)**: `83b533ae0a17349e95e80c104620949cd2759449997445bb2ad07ec0803ac644` (canonical-plan digest, recorded in `prereg.json`'s freeze block).
- **Terminal artifact hash (SUBS-03)**: `3dff03377fb18d9a` (xxhash64); replay all_match = TRUE (byte-identical).
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
