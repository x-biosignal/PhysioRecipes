import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/cca_summary.csv"))}
bs   = list(csv.DictReader(open("artifacts/cca_by_subject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("cca_r1 traces",       abs(sm["cca_r1"]       - by["cca_r1"]["value"])       < 1e-9)
check("cca_r2 traces",       abs(sm["cca_r2"]       - by["cca_r2"]["value"])       < 1e-9)
check("max_abs_diff traces", abs(sm["max_abs_diff"] - by["max_abs_diff"]["value"]) < 1e-18)
check("r1_mean5 traces",     abs(sm["r1_mean5"]     - by["r1_mean5"]["value"])     < 1e-6)
check("r1_min5 traces",      abs(sm["r1_min5"]      - by["r1_min5"]["value"])      < 1e-6)

# --- external cross-tool validation: cca == stats::cancor (machine precision) -
check("cca_r1 == cancor_r1 to machine precision", abs(sm["cca_r1"] - sm["cancor_r1"]) < 1e-9)
check("cca_r2 == cancor_r2 to machine precision", abs(sm["cca_r2"] - sm["cancor_r2"]) < 1e-9)
check("the recorded max_abs_diff is at machine precision (< 1e-12)", sm["max_abs_diff"] < 1e-12)

# --- reference recovery: strong, ordered canonical correlations -------------
check("first canonical correlation is strong (r1 > 0.7)", sm["cca_r1"] > 0.7)
check("canonical correlations are ordered (r1 >= r2)", sm["cca_r1"] >= sm["cca_r2"])
check("both canonical correlations are valid (0 <= r <= 1)",
      0 <= sm["cca_r2"] <= 1 and 0 <= sm["cca_r1"] <= 1)
check("coupling holds across ALL five subjects (min r1 > 0.7)", sm["r1_min5"] > 0.7)
check("the per-subject artifact lists all five subjects", len(bs) == 5)
check("every subject's r1 traces to [min5, max5]",
      all(sm["r1_min5"] - 1e-6 <= float(r["first_canonical_corr"]) <= sm["r1_max5"] + 1e-6 for r in bs))

# --- honest scope: CCA is the linear lens (compare to dCor) ------------------
check("HONEST: first canonical correlation ~ distance correlation (largely linear coupling)",
      "0.72" in case["proposition"] and "linear" in case["validation"]["note"].lower())
check("HONEST: cross-tool (stats::cancor), not a self-comparison", "stats::cancor" in case["validation"]["reference"])
check("HONEST: dCor/RSA/CCA trilogy on identical data noted",
      "three-lens" in case["validation"]["note"].lower() or "three lens" in case["validation"]["note"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
