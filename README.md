# PhysioRecipes

A growing, **version-controlled database of reproducible analysis case studies**
built on the PhysioExperiment ecosystem and public data. Each entry is a
self-contained scientific unit — a *proposition*, the *question and goal* it
answers, the *challenge and the ecosystem approach* that solves it, and the
*conclusion, figures and tables* — backed end-to-end by the reproducibility
substrate so that every reported number traces to an artifact and the whole
pipeline replays byte-identically.

The collection is published as an **x-biosignal resource**: a Quarto gallery
(one page per case) plus a companion R data package that ships the verified run
bundles (so a reader can re-run or audit any case).

## Why

1. **Track record.** Demonstrate, on public gold-standard datasets, that the
   ecosystem reproduces established analyses — and does so reproducibly.
2. **A reusable corpus.** Each case is a recipe others can lift and adapt.
3. **A research pipeline.** Reproduction routinely surfaces *important open
   questions* (e.g. metric definitions on which tools legitimately disagree).
   Cases that raise a significant unresolved question are **escalated to a
   paper**, carrying the same substrate-grade rigor (see `SCHEMA.md` →
   *Escalation*).

## The unit

Every case follows the same structure — defined in [`SCHEMA.md`](SCHEMA.md) and
scaffolded by [`TEMPLATE.qmd`](TEMPLATE.qmd):

| Section | What it holds |
|---|---|
| **Proposition** | the central claim the case establishes |
| **Question & goal** | what is asked and why it matters |
| **Challenge & approach** | the difficulty, and the ecosystem op-DAG that resolves it |
| **Data** | the public dataset + citation |
| **Results** | figures/tables, every number traced to an artifact |
| **Conclusion** | the verified claims (GROUNDED / not) |
| **Open questions** | unresolved questions — the escalation queue to papers |
| **Reproduce** | the frozen op-DAG + byte-identical replay + verification badge |

## Layout

```
PhysioRecipes/
├── README.md            # this file
├── SCHEMA.md            # the case-unit contract (metadata + narrative sections)
├── TEMPLATE.qmd         # copy this to start a new case
├── _quarto.yml          # gallery site config
└── cases/
    └── <id>/
        ├── index.qmd    # the narrative unit (renders to one gallery page)
        ├── case.json    # structured DB record (validates against SCHEMA.md)
        └── bundle/      # the substrate run bundle (prereg/manifest/opdag/claims/verification)
```

## Status

Bootstrapping. First worked case: [`cases/ecg-hrv-mitbih`](cases/ecg-hrv-mitbih)
(ECG/HRV on the MIT-BIH Arrhythmia Database). Gallery rendering and the companion
data package run in CI once a handful of cases exist; public release to
`x-biosignal` follows the ecosystem's develop→verify→publish flow.
