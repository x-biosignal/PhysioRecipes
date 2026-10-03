#!/usr/bin/env python3
"""Generate coverage.qmd -- the corpus coverage map -- from every case.json.

The gallery (index.qmd) LISTS the cases; this builds the complementary MAP:
which method is checked against which field-standard reference tool, on what
data, at what fidelity tier. Single source of truth = inst/cases/*/case.json.

Run from the PhysioRecipes root:  python3 tools/build_coverage.py
It (re)writes coverage.qmd. Re-run whenever cases are added or changed.
"""
import json, glob, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# --- external reference-tool families we validate against -------------------
# (pattern -> canonical display name); first match wins, order matters
FAMILIES = [
    (r"mne", "MNE-Python"),
    (r"neurokit", "NeuroKit2"),
    (r"statsmodels", "statsmodels"),
    (r"scipy", "SciPy"),
    (r"\bggir\b", "GGIR"),
    (r"\brhrv\b", "RHRV"),
    (r"lme4|\blmer\b|nlme", "lme4/nlme"),
    (r"\berm\b|partial credit", "eRm"),
    (r"\benergy\b|dcor", "energy (R)"),
    (r"tensorpac", "tensorpac"),
    (r"antropy", "antropy"),
    (r"\bnolds\b", "nolds"),
    (r"fooof|specparam", "FOOOF/specparam"),
    (r"opensim", "OpenSim"),
    (r"\bvegan\b", "vegan (R)"),
    (r"factominer", "FactoMineR"),
    (r"spm1d", "spm1d"),
    (r"openhdemg", "openhdemg"),
    (r"\birr\b|\bicc\b", "irr (ICC)"),
    (r"\bwfdb\b|\.atr|physionet ann", "WFDB annotations"),
    (r"circular", "circular (R)"),
    (r"cancor|canonical corr", "stats::cancor"),
    (r"bailey|lang|uswatte", "Bailey/Lang framework"),
    (r"physiopy|\bbids\b", "physiopy/BIDS"),
    (r"ground.?truth|activity labels|provided.*split|per-trial.*label|benchmark protocol|held-out",
     "dataset ground-truth labels"),
    (r"\br\b reimpl|base[- ]r|base r|stats::|recompute|peng et al", "base-R recompute"),
]

def family_of(refs):
    blob = " ".join(refs).lower()
    fams = []
    for pat, name in FAMILIES:
        if re.search(pat, blob) and name not in fams:
            fams.append(name)
    return fams

def esc(s):
    # table-cell + inline-HTML safe: escape pipes, angle + square brackets, flatten newlines
    return (str(s).replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
            .replace("[", "\\[").replace("]", "\\]").replace("\n", " ").strip())

def aslist(v):
    """Coerce a scalar/None to a list (a case.json field may be a bare string)."""
    if v is None:
        return []
    return v if isinstance(v, list) else [v]

def load():
    rows = []
    for cj in sorted(glob.glob("inst/cases/*/case.json")):
        d = json.load(open(cj))
        cid = d.get("id", os.path.basename(os.path.dirname(cj)))
        val = d.get("validation") or {}
        # data provenance: prefer validation.data, else dataset.record
        data = val.get("data") or ((d.get("dataset") or {}).get("record") or "")
        is_real = "REAL" in data.upper() or bool((d.get("dataset") or {}).get("public"))
        refs = aslist(d.get("reference_tools")) or ([val["reference"]] if val.get("reference") else [])
        ver = d.get("verification") or {}
        if not refs and ver.get("replay_byte_identical"):
            refs = ["byte-identical replay (published finding)"]
        fams = family_of(refs)
        # display reference: matched families, else a short raw reference, else --
        if fams:
            ref_display = "; ".join(fams)
        elif refs:
            r0 = refs[0]
            ref_display = (r0[:46] + "…") if len(r0) > 47 else r0
        else:
            ref_display = "--"
        rows.append(dict(
            id=cid,
            title=d.get("title") or cid,
            modality=aslist(d.get("modality")),
            packages=aslist(d.get("packages")),
            ops=aslist(d.get("opdag")),
            refs=refs,
            families=fams,
            ref_display=ref_display,
            data_real=is_real,
            tier=d.get("status", ""),
            n_claims=len(d.get("claims") or []),
        ))
    return rows

def main():
    rows = load()
    n = len(rows)
    n_real = sum(r["data_real"] for r in rows)
    ops = sorted({o for r in rows for o in r["ops"]})
    pkgs = sorted({p for r in rows for p in r["packages"]})
    fam_count = collections.Counter(f for r in rows for f in r["families"])
    # primary modality bucket for grouping = first modality
    buckets = collections.OrderedDict()
    MOD_ORDER = ["eeg", "ecg", "hrv", "emg", "gait", "kinematics", "kinetics",
                 "biomechanics", "cross-modal", "adl", "wearable", "spectral",
                 "network-physiology", "fnirs", "tms-eeg", "sleep"]
    def bucket_key(r):
        for m in MOD_ORDER:
            if m in r["modality"]:
                return m
        return (r["modality"][0] if r["modality"] else "other")
    for r in sorted(rows, key=lambda r: (bucket_key(r), r["id"])):
        buckets.setdefault(bucket_key(r), []).append(r)

    out = []
    W = out.append
    W("---")
    W('title: "Coverage map"')
    W('subtitle: "What the recipe corpus validates -- every method, its field-standard reference, and the public data it was checked on"')
    W("---")
    W("")
    W("<!-- GENERATED by tools/build_coverage.py from inst/cases/*/case.json -- do not edit by hand. -->")
    W("")
    W("The [gallery](index.qmd) lists the cases; this is the **map**. Each recipe pins a")
    W("method in the ecosystem against an independent reference -- the tool a specialist")
    W("would reach for (MNE-Python, SciPy, GGIR, lme4, `energy`, NeuroKit2), the dataset's")
    W("own ground truth, or an established published finding -- on **public** data, and")
    W("reports the agreement honestly (a machine-precision match where the method is exactly")
    W("defined, a high-correlation *agreement* where independent implementations differ by")
    W("convention, a reference *recovery* where the target is a known physiological result).")
    W("")
    # --- summary callout ----------------------------------------------------
    n_tool = sum(1 for r in rows if r["families"])
    W("::: {.callout-note appearance=\"simple\"}")
    W(f"**{n} cases** &middot; **{n_real} on real public data** &middot; "
      f"**{len(ops)} distinct operations** across **{len(pkgs)} packages** &middot; "
      f"**{n_tool}** reproduce a named independent reference across "
      f"**{len(fam_count)} distinct references**; the remaining **{n - n_tool}** "
      f"reproduce an established finding or reference baseline.")
    W(":::")
    W("")
    # --- reference families -------------------------------------------------
    W("## Validated against independent references")
    W("")
    W("The corpus does not grade itself -- each case reproduces an external reference: a")
    W("third-party tool, the dataset's own ground truth, an independent base-R recomputation,")
    W("or an established published finding. Cases per reference:")
    W("")
    W("| Reference | Cases |")
    W("|---|---:|")
    for name, c in fam_count.most_common():
        W(f"| {esc(name)} | {c} |")
    W("")
    # --- per-modality coverage tables --------------------------------------
    W("## Cases by modality")
    W("")
    all_real = all(r["data_real"] for r in rows)
    tierline = ("Tier: **validated** = validation block + audit re-checks every number; "
                "**verified** = byte-identical replay bundle.")
    if all_real:
        W(tierline + " *Every case runs on a real public recording.*")
    else:
        W(tierline + " Data: **real** = public recording; **sim** = simulated/deterministic.")
    W("")
    hdr = ("| Case | Method(s) | Package(s) | Reference | Tier |", "|---|---|---|---|:--:|") \
        if all_real else \
        ("| Case | Method(s) | Package(s) | Reference | Data | Tier |", "|---|---|---|---|:--:|:--:|")
    for b, rs in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        W(f"### {b} ({len(rs)})")
        W("")
        W(hdr[0]); W(hdr[1])
        for r in rs:
            # strip backticks first: truncating inside a `code span` would leave an
            # unbalanced backtick that breaks the markdown link (and cascades down the table)
            ttl = r["title"].replace("`", "")
            ttl = (ttl[:98].rstrip() + "…") if len(ttl) > 99 else ttl
            link = f"[{esc(ttl)}](inst/cases/{r['id']}/index.qmd)"
            meth = esc(", ".join(f"`{o}`" for o in r["ops"]) or "--")
            pk = esc(", ".join(r["packages"]) or "--")
            ref = esc(r["ref_display"])
            if all_real:
                W(f"| {link} | {meth} | {pk} | {ref} | {r['tier']} |")
            else:
                data = "real" if r["data_real"] else "sim"
                W(f"| {link} | {meth} | {pk} | {ref} | {data} | {r['tier']} |")
        W("")
    W("---")
    W("")
    W("*This map is generated from `inst/cases/*/case.json` by "
      "`tools/build_coverage.py`; re-run it after adding a case. "
      "Every linked case traces each reported number to an artifact and, for verified-tier "
      "cases, replays byte-identically.*")
    W("")

    open("coverage.qmd", "w").write("\n".join(out))
    print(f"wrote coverage.qmd  ({n} cases, {len(ops)} methods, {len(pkgs)} packages, "
          f"{len(fam_count)} reference-tool families)")
    # quick self-check: every case linked, no unmatched references
    unref = [r["id"] for r in rows if not r["refs"]]
    if unref:
        print("WARN: cases with no reference_tools:", unref)
    return 0

if __name__ == "__main__":
    sys.exit(main())
