import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/promp_summary.csv"))}
cur  = list(csv.DictReader(open("artifacts/promp_curves.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("cor_mean traces",   abs(s["cor_mean_vs_ensemble"]     - by["cor_mean"]["value"])   < 5e-3)
check("band_cover traces", abs(s["band_coverage_2sd"]        - by["band_cover"]["value"]) < 5e-3)
check("via_shrink traces", abs(s["viapoint_sd_shrink_ratio"] - by["via_shrink"]["value"]) < 5e-2)
check("via_pull traces",   abs(s["viapoint_mean_pull_deg"]   - by["via_pull"]["value"])   < 0.1)
check("n_subjects traces", int(s["n_subjects"])              == by["n_subjects"]["value"])

# --- reference recovery: the three defining ProMP properties ----------------
check("ProMP mean recovers the ensemble average (r > 0.999)", s["cor_mean_vs_ensemble"] > 0.999)
check("+/-2 SD band is calibrated (0.90 <= coverage <= 0.99)", 0.90 <= s["band_coverage_2sd"] <= 0.99)
check("conditioning shrinks uncertainty at the via-point (ratio < 0.5)", s["viapoint_sd_shrink_ratio"] < 0.5)
check("conditioning pulls the mean toward the via-point (> 5 deg)", s["viapoint_mean_pull_deg"] > 5)
# the ProMP mean equals the ensemble mean column-for-column
mx = max(abs(float(r["promp_mean"]) - float(r["ensemble_mean"])) for r in cur)
check("ProMP mean == ensemble mean pointwise (<1 deg)", mx < 1.0)
# conditioning propagates: the conditioned mean differs from prior away from the via-point too
off = [abs(float(r["cond_mean"]) - float(r["promp_mean"])) for r in cur if int(r["pct_cycle"]) < 40]
check("conditioning propagates along the cycle (learned covariance)", max(off) > 1.0)

# --- honest scope -----------------------------------------------------------
check("open question flags within-subject / mixture limits",
      any("stride" in q["q"] or "mixture" in q["q"] for q in case["open_questions"]))

print("\nRESULT:", "PASS -- ProMP properties recovered; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
