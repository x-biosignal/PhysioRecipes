# Provenance -- primary bundle (S001 rest, sensorimotor C3/C4)

Primary substrate run of the motor-ERD case: subject S001, REST condition,
absolute band power at C3/C4. Self-contained:

- `prereg.json` -- op-DAG frozen BEFORE running (SUBS-02).
- `run_manifest.json` -- op-DAG + env fingerprint + content-addressed output hash.
- `terminal_table.csv` -- absolute band power per channel (alpha col = mu 8-13 Hz).
- `claims.json` / `verification_report.json` -- each C3 band power GROUNDED (SUBS-01).
- `report.md` -- the human-readable finding.

op-DAG: butterworth_filter(1,45) -> band_power(relative=FALSE)
sha256(prereg.json) = 00aa46f49ab5af9a81d400de237db9666605200130134372ff9a4affe63295f4

Data prep (documented provenance, not part of the frozen op-DAG): for each
subject the movement runs R03/R07/R11 are segmented by the dataset's own EDF+
annotations (T0=rest; T1/T2=fists=movement) and concatenated per condition;
source EDF sha256 are in `../artifacts/data_sources.json`. All 10 runs are
frozen + replayed; the ERD panel (`../artifacts/erd_panel.csv`) compares
GROUNDED movement vs rest mu/beta cells per subject; see audit.py.
