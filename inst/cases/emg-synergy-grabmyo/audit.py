import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
ps   = {r["item"]: r["value"] for r in csv.DictReader(open("artifacts/pipeline_summary.csv"))}
vaf  = {int(r["n_synergies"]): r for r in csv.DictReader(open("artifacts/vaf_analysis.csv"))}
icc  = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/synergy_split_half_icc_pooled.csv"))}
cors = sorted([abs(float(r["correlation"]))
               for r in csv.DictReader(open("artifacts/synergy_split_half_stability.csv"))], reverse=True)

# --- claims trace ------------------------------------------------------------
check("vaf_4syn traces to vaf_analysis (n=4)", abs(float(vaf[4]["vaf_nmf"]) - by["vaf_4syn"]["value"]) < 1e-3)
check("optimal_n traces", int(float(ps["optimal_n_synergies"])) == by["optimal_n"]["value"])
check("pooled_icc traces", abs(icc["pooled_icc_a1"] - by["pooled_icc"]["value"]) < 1e-3)
check("icc_ci_lo traces", abs(icc["pooled_ci_lo"] - by["icc_ci_lo"]["value"]) < 1e-3)
check("splithalf_min_r traces (min correlation)", abs(min(cors) - by["splithalf_min_r"]["value"]) < 1e-3)

# --- the reliability finding: all four synergies reproduce -------------------
check("four split-half correlations present", len(cors) == 4)
check("ALL four synergies reproduce (weakest >= 0.80)", min(cors) >= 0.80)
check("pooled ICC indicates good agreement (>= 0.75)", icc["pooled_icc_a1"] >= 0.75)
check("ICC CI is consistent (lo < value < hi)",
      icc["pooled_ci_lo"] < icc["pooled_icc_a1"] < icc["pooled_ci_hi"])

# --- honest scope: parsimony (2-synergy knee), not a weak 4th ----------------
check("optimal_n = 2 (VAF knee) is the parsimony basis", int(float(ps["optimal_n_synergies"])) == 2)
check("open question frames the single-run 4th-synergy as an artifact",
      "artifact" in case["open_questions"][0]["q"].lower() and "single-run" in case["open_questions"][0]["q"].lower())

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
