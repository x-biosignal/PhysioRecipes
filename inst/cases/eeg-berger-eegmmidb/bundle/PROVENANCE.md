# Provenance -- primary bundle (eyes-closed O1)

This bundle is the primary substrate run of the Berger-effect case: the
eyes-closed occipital-O1 relative band power, which reproduces the established
eeg-alpha anchor. It is self-contained:

- `prereg.json` -- the op-DAG frozen BEFORE running (SUBS-02).
- `run_manifest.json` -- op-DAG + env fingerprint + content-addressed output hash.
- `terminal_table.csv` -- relative band power at O1 (eyes-closed), the op-DAG output.
- `claims.json` / `verification_report.json` -- each band power resolved to the
  terminal cell and GROUNDED (SUBS-01).
- `report.md` -- the human-readable finding.

op-DAG: read_edf(channels="O1..") -> butterworth_filter(low=1,high=45) -> band_power(relative=TRUE)
sha256(prereg.json) = 0d121716cffb66320061d7a40e9c6f2ebf8511f85ee3a7596648ff757fe18116

The eyes-open O1/Oz and eyes-closed Oz runs are equally frozen + replayed;
their terminals live in `../artifacts/` with hashes in `secondary_runs.json`.
The Berger contrast (`../artifacts/berger_contrast.csv`) compares GROUNDED
eyes-closed vs eyes-open alpha cells; see `audit.py`.
