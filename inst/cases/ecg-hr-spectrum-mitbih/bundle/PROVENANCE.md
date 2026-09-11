# Provenance -- primary bundle (record 117, bradycardia)

Primary substrate run of the HR-spectrum case: record 117 (the bradycardic
end of the panel). Self-contained:

- `prereg.json` -- the op-DAG frozen BEFORE running (SUBS-02).
- `run_manifest.json` -- op-DAG + env fingerprint + content-addressed output hash.
- `terminal_table.csv` -- time-domain HRV per lead (channel 1 = MLII), op-DAG output.
- `claims.json` / `verification_report.json` -- the two headline quantities
  (mean HR, mean RR) resolved to the terminal cell and GROUNDED (SUBS-01).
- `report.md` -- the human-readable finding.

op-DAG: ecgDetectRpeaks(pan_tompkins) -> ecgRRintervals -> ecgHRVtime(rhythm_check=FALSE)
sha256(prereg.json) = f027dea40d4809b04a1d72b60221ea0158173b65023ee0424604b8371bdaf698

The other three records (115/103/234) are equally frozen + replayed; their
terminals live in `../artifacts/` with hashes in `secondary_runs.json`. The
HR spectrum (`../artifacts/ecg_hr_spectrum.csv`) compares GROUNDED mean-HR/mean-RR
cells across records; see `audit.py`.
