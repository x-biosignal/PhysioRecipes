import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/jb_summary.csv"))}
check("jb_statistic traces",              abs(sm["jb_statistic"] - by["jb_statistic"]["value"]) < 1e-4)
check("jb_stat_diff_scipy traces",        abs(sm["jb_stat_diff_scipy"] - by["jb_stat_diff_scipy"]["value"]) < 1e-16)
check("jb_pvalue_diff_scipy traces",      abs(sm["jb_pvalue_diff_scipy"] - by["jb_pvalue_diff_scipy"]["value"]) < 1e-20)
check("critical_value_95 traces",         abs(sm["critical_value_95"] - by["critical_value_95"]["value"]) < 1e-4)
check("reject_normality traces",          int(sm["reject_normality"]) == by["reject_normality"]["value"])
check("descriptive_near_gaussian traces", int(sm["descriptive_near_gaussian"]) == by["descriptive_near_gaussian"]["value"])
# machine-precision
check("JB statistic == scipy.stats.jarque_bera BIT-FOR-BIT (< 1e-9)", sm["jb_stat_diff_scipy"] < 1e-9)
check("JB p-value == scipy p-value BIT-FOR-BIT (< 1e-9)", sm["jb_pvalue_diff_scipy"] < 1e-9)
# decision + the large-N nuance
check("normality rejected (JB > critical)", sm["jb_statistic"] > sm["critical_value_95"])
check("reject_normality flag set", int(sm["reject_normality"]) == 1)
check("descriptive near-Gaussian yet formally rejected (the large-N nuance)",
      int(sm["descriptive_near_gaussian"]) == 1 and int(sm["reject_normality"]) == 1)
check("95% chi-square(2) critical value is ~5.99", 5.9 < sm["critical_value_95"] < 6.0)
check("JB statistic positive and moderate (not an artifact-scale value)", 0 < sm["jb_statistic"] < 1000)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op built on signalMoments (formal normality test the ecosystem lacked)",
      "newly authored" in _note and "formal normality test the ecosystem lacked" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical closed-form JB + chi-square), not a convention agreement",
      "machine-precision" in _note and "identical closed-form" in _note and "not a convention agreement" in _note)
check("HONEST: the large-N nuance (rejects yet descriptively near-Gaussian; effect size not test outcome)",
      "large-n phenomenon" in _note and "effect-size" in _note and "not a test outcome" in _note)
check("HONEST: analogous to Ljung-Box for the ACF (confirmatory partner of the moments)",
      "confirmatory partner" in _note and "ljung-box" in _note)
check("HONEST: scipy.stats cross-tool reference", "scipy.stats.jarque_bera" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
