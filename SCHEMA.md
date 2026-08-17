# PhysioRecipes case-unit schema

A case is **one self-contained, reproducible scientific unit**. It has two
faces that must agree: a human-readable narrative (`index.qmd`) and a machine
record (`case.json`). Both follow the contract below. The rule that governs
everything: **every number in the narrative traces to an artifact in the
bundle**, and **the pipeline replays byte-identically** — no figure or claim
exists that the substrate has not verified.

## Narrative sections (`index.qmd`)

A case is a **user-facing case study** — a reader learns what the ecosystem
reproduces, whether they can trust it for their own work, and how to apply the
same recipe to their own hypothesis. It is NOT a provenance dump. Procedural
detail (checksums, the frozen recipe, replay hashes) lives in `bundle/` /
`artifacts/` and is pointed to by ONE closing line — it must NOT fill the prose.
`agent/CASE_RESTYLE_SPEC.md` is the working spec; `eeg-berger-eegmmidb` is the
gold reference. In order:

0. **Top badge** (a `>` blockquote), plain language, three bolded parts:
   **What this case shows** (the finding in one sentence) · **What reproduces, and
   what doesn't** (HONEST scoping — what the ecosystem reproduces here and what it
   does *not*, with the reason; never a salesy "why you can trust it") · **How to
   read it** (what the figure/table numbers mean).
0b. **"The recipe you'll learn"** — a `::: {.callout-tip}` with **Workflow** (the
   reusable step sequence), **Way of thinking** (the judgment calls that make it
   valid), **Ecosystem usage** (which functions, chained by role I/O →
   preprocessing → analysis via the shared data model). State the transferable
   recipe up front; the last section delivers it.
1. **Proposition** — one sentence: the central claim. Plain, no jargon.
2. **Question & goal** — **the question the source dataset was created to answer**,
   cited (MIT-BIH → evaluating beat detectors + cardiac dynamics; eegmmidb/BCI2000
   → decoding movement, its eyes-open/closed runs establishing the resting
   baseline; …). Do not invent a question the data was not collected to address.
3. **Challenge & approach** — the difficulty + the ecosystem recipe (named tools,
   plain language — "the three steps", not "op-DAG").
4. **Data** — the public dataset + citation; link `data_sources.json` as "the
   exact recordings used" (drop "sha256-pinned" phrasing from the prose).
5. **Results** — the **figure** (`![caption](artifacts/figure.png)`, a
   pre-generated PNG committed under `artifacts/` — the gallery CI renders with
   Quarto only, no R/data, so figures are built ahead by `agent/make_recipe_figures.R`
   or `agent/fig_<id>.R`, never at render) + a one-line *"How to read this:"* + the
   tables. Every value traces to an artifact; no un-sourced decimals.
6. **Conclusion** — plain; end on the transferable takeaway.
7. **Open questions** — unresolved questions; mark paper-worthy ones with
   `escalate: <target>` (the research queue).
8. **Using this in your own analysis** — the tutorial that delivers the recipe:
   the general steps, a **step | function | package** table + why they chain
   (shared data model), **how to choose the parameters** (case-specific), how to
   apply it to the reader's own hypothesis (link sibling cases), the runnable
   ```r recipe (not executed at render), and ONE closing "audit" line pointing
   technical readers to `bundle/` (verified) or the artifacts + `audit.py`
   (validated) for the full machine-checkable record.

## Machine record (`case.json`)

```jsonc
{
  "id": "ecg-hrv-mitbih",           // kebab-case; matches the directory
  "title": "…",                      // gallery card title
  "modality": ["ecg", "hrv"],        // controlled tags
  "packages": ["PhysioECG", "PhysioIO"],   // ecosystem packages exercised
  "dataset": {
    "name": "MIT-BIH Arrhythmia Database",
    "url": "https://physionet.org/content/mitdb/",
    "public": true,
    "citation": "Moody GB, Mark RG. IEEE Eng Med Biol Mag. 2001;20(3):45-50."
  },
  "proposition": "…",                // = narrative §1
  "opdag": ["ecgDetectRpeaks", "ecgHRVtime"],   // the frozen recipe (registry tool names)
  "claims": [                        // = verification_report.json, condensed
    { "id": "…", "statement": "…", "value": 0.0, "artifact": "…", "status": "GROUNDED" }
  ],
  "verification": {                  // reproducibility badge
    "n_claims": 2, "n_grounded": 2,
    "prereg_hash": "…", "replay_byte_identical": true
  },
  "open_questions": [
    { "q": "…", "escalate": "paper:HRV-reproducibility" }   // or null if none
  ],
  "reference_tools": ["RHRV 5.0.0"], // cross-tool comparators, if any
  "bundle": "bundle/",               // path to the substrate run bundle
  "status": "draft" | "verified" | "escalated"
}
```

## Status tiers

- **`verified`** — backed by a substrate run **bundle**: pre-registered, every
  claim GROUNDED in `verification_report.json`, op-DAG replays byte-identically.
  The strongest tier. Requires `bundle/` and a `verification` block.
- **`validated`** — backed by **real public-data validation** against a reference
  (cross-tool agreement, reference recovery, or ground-truth match) but without a
  substrate replay bundle. Requires a `validation` block and `artifacts/`; every
  claim still traces to a real-data artifact. Honest, one notch below `verified`.
- **`draft`** — work in progress; not published to the gallery.

A `validated` case carries a `validation` object instead of `verification`:

```jsonc
"validation": {
  "reference": "NeuroKit2 0.2.x",           // the comparator / ground truth
  "data": "REAL — <dataset, record>",        // must say REAL and cite the source
  "artifacts": ["artifacts/<file>.csv"],
  "all_pass": true                            // every claim's PASS/agreement holds
}
```

## Embargo — unresolved questions are NOT published

Per policy, a case that raises a **genuinely unresolved question destined for a
paper is embargoed**: it is *not* placed under `inst/cases/` and is *never*
synced to the public repo until the paper is out. Such cases live in the private,
un-synced `physio-ecosystem/recipes-embargo/` (outside the `Physio*` glob, so the
publisher never sees them). Enforcement: **no case under `inst/cases/` may set
`open_questions[].escalate`** — `tools/validate_case.py` fails the public gate if
one does. When a paper publishes, the case may be moved into `inst/cases/` with
`status: verified/validated` and the escalation cleared (linking the paper).

## The bundle (`bundle/`)

The substrate run bundle — the same shape the PhysioAgent executor emits and that
`PhysioLake::physioPutBundle()` stores with lineage:

- `prereg.json` — the frozen pre-registration (SUBS-02); its sha256 is the
  `prereg_hash`. Freezing *before* running is what makes the result
  HARKing-proof.
- `run_manifest.json` — seed, environment fingerprint, output hash (SUBS-03).
- `opdag.*` / `proposal.json` — the typed operation DAG that was executed.
- `terminal_table.csv` — the terminal artifact the claims read from.
- `claims.json` + `verification_report.json` — claim→artifact verification
  (SUBS-01); a case is `verified` only when every claim is GROUNDED.
- `PROVENANCE.md` — dataset, environment, and script trail.

## Escalation to a paper

Reproduction routinely exposes questions worth publishing (a metric definition on
which mature tools disagree by an order of magnitude; a public dataset where the
ecosystem finds something references miss). When an `open_questions[].escalate`
is set, the case is promoted: it seeds a manuscript that reuses this bundle as
its evidence and inherits the substrate's integrity guarantees (every figure
traced, pre-registered, replayable). The case's `status` becomes `escalated` and
links the paper. This keeps the corpus and the publication pipeline on one spine.

## Invariants (a case is not accepted unless)

- The dataset is **public**.
- Every reported number traces to a bundle artifact (`n` un-sourced decimals = 0).
- The op-DAG **replays byte-identically** (`replay_byte_identical: true`).
- Every headline claim is **GROUNDED** in `verification_report.json`.
- Sole author throughout is **Yusuke Matsui**; no AI attribution anywhere.
