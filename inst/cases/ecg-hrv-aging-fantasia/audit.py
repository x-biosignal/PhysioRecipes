import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, statistics
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
grp  = {r["metric"]: r for r in csv.DictReader(open("artifacts/hrv_group_summary.csv"))}
ps   = list(csv.DictReader(open("artifacts/hrv_per_subject.csv")))

def col(group, m):
    out = []
    for r in ps:
        if r["group"] != group: continue
        v = r[m]
        if v in ("", "NA"): continue
        out.append(float(v))
    return out

# --- claims trace to the group-summary artifact ------------------------------
check("totpow_young traces",   abs(float(grp["total_power"]["young_median"])   - by["totpow_young"]["value"])   < 1e-2)
check("totpow_elderly traces", abs(float(grp["total_power"]["elderly_median"]) - by["totpow_elderly"]["value"]) < 1e-2)
check("totpow_p traces",       abs(float(grp["total_power"]["wilcox_p"]) - by["totpow_p"]["value"]) < 1e-6)
check("hf_p traces",           abs(float(grp["hf"]["wilcox_p"])          - by["hf_p"]["value"])     < 1e-6)
check("lfhf_p traces",         abs(float(grp["lf_hf_ratio"]["wilcox_p"]) - by["lfhf_p"]["value"])   < 1e-4)

# --- re-derive the medians from the per-subject rows -------------------------
for m in ("total_power", "hf", "mean_hr"):
    ym = statistics.median(col("young", m)); em = statistics.median(col("elderly", m))
    check(f"{m}: young median re-derives",   abs(ym - float(grp[m]["young_median"]))   < 1e-2)
    check(f"{m}: elderly median re-derives", abs(em - float(grp[m]["elderly_median"])) < 1e-2)

# --- the headline direction + magnitude finding ------------------------------
check("total power: young median > elderly median",
      float(grp["total_power"]["young_median"]) > float(grp["total_power"]["elderly_median"]))
check("HF power: young median > elderly median",
      float(grp["hf"]["young_median"]) > float(grp["hf"]["elderly_median"]))
check("magnitude indices significant (p < 0.05)",
      float(grp["total_power"]["wilcox_p"]) < 0.05 and float(grp["hf"]["wilcox_p"]) < 0.05)

# --- honest scope: balance ratios + mean HR do NOT separate (p >= 0.05) ------
check("LF/HF ratio does NOT separate the groups (p >= 0.05)", float(grp["lf_hf_ratio"]["wilcox_p"]) >= 0.05)
check("HFnu does NOT separate the groups (p >= 0.05)",        float(grp["hf_nu"]["wilcox_p"])      >= 0.05)
check("resting mean HR does NOT separate the groups (p >= 0.05)", float(grp["mean_hr"]["wilcox_p"]) >= 0.05)

# --- honest scope: one elderly record flagged/excluded from frequency HRV ----
n_eld_freq = len(col("elderly", "total_power"))
n_eld_hr   = len(col("elderly", "mean_hr"))
check("one elderly record excluded from frequency HRV (9 vs 10)", n_eld_freq == 9 and n_eld_hr == 10)
check("excluded record (f1o09) has NA frequency metrics",
      any(r["subject"] == "f1o09" and r["hf"] in ("", "NA") for r in ps))

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
