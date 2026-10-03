# Provenance -- primary bundle (S001 eyes-closed O1)

Primary substrate run of the group-level Berger-reactivity case: subject S001,
eyes-closed occipital O1 relative band power (reproduces the eeg-alpha anchor).
Self-contained:

- `prereg.json` -- op-DAG frozen BEFORE running (SUBS-02).
- `run_manifest.json` -- op-DAG + env fingerprint + content-addressed output hash.
- `terminal_table.csv` -- relative band power at O1 (S001 eyes-closed).
- `claims.json` / `verification_report.json` -- each band power GROUNDED (SUBS-01).
- `report.md` -- the human-readable finding.

op-DAG: read_edf("O1..") -> butterworth_filter(1,45) -> band_power(relative=TRUE)
sha256(prereg.json) = 87fcaf48f158fb93b3fce2587442c1298a032dddc5afc3eb124fa69b254d8b1e

All 20 runs (10 subjects x {eyes-closed, eyes-open}) are equally frozen +
replayed; their terminals live in `../artifacts/` with hashes in
`secondary_runs.json`. The reactivity panel (`../artifacts/reactivity_panel.csv`)
compares GROUNDED eyes-closed vs eyes-open alpha cells per subject; see audit.py.
