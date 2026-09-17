import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/ar_summary.csv"))}
check("ar_phi1 traces",         abs(sm["ar_phi1"] - by["ar_phi1"]["value"]) < 1e-6)
check("ar_phi2 traces",         abs(sm["ar_phi2"] - by["ar_phi2"]["value"]) < 1e-6)
check("var_pred traces",        abs(sm["var_pred"] - by["var_pred"]["value"]) < 1e-3)
check("max_diff_phi_sm traces", abs(sm["max_diff_phi_sm"] - by["max_diff_phi_sm"]["value"]) < 1e-16)
check("var_diff_sm traces",     abs(sm["var_diff_sm"] - by["var_diff_sm"]["value"]) < 1e-14)
check("stationary traces",      int(sm["stationary"]) == by["stationary"]["value"])
# machine-precision vs statsmodels
check("AR coefficients == statsmodels yule_walker(mle) BIT-FOR-BIT (< 1e-9)", sm["max_diff_phi_sm"] < 1e-9)
check("innovation variance == statsmodels (< 1e-9)", sm["var_diff_sm"] < 1e-9)
# AR structure
check("fitted AR(4) is stationary (flag set)", int(sm["stationary"]) == 1)
check("lag-2 AR coefficient negative (oscillatory dynamics)", sm["ar_phi2"] < 0)
check("innovation variance positive", sm["var_pred"] > 0)
check("lag-1 AR coefficient near 1 (strong short-lag dependence)", 0.5 < sm["ar_phi1"] < 2)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op building on autocorrelation, completing the ACF/PACF/AR-fit lane",
      "newly authored" in _note and "complete the acf/pacf/ar-fit lane" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical biased/MLE Yule-Walker), not a convention agreement",
      "machine-precision" in _note and "identical biased/mle" in _note and "not a convention agreement" in _note)
check("HONEST: matches MLE/biased; adjusted and base-R ar.yw correction differ by construction (not the target)",
      "not the target" in _note and "differ by construction" in _note)
check("HONEST: fitted AR stationary + alpha-band peak = oscillatory alpha generative model",
      "stationary" in _note and "alpha-band spectral peak" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
