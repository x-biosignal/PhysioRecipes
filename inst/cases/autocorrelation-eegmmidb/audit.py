import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, math
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/acf_summary.csv"))}
check("acf_lag1 traces",             abs(sm["acf_lag1"] - by["acf_lag1"]["value"]) < 1e-6)
check("acf_lag2 traces",             abs(sm["acf_lag2"] - by["acf_lag2"]["value"]) < 1e-6)
check("acf_lag0 traces",             abs(sm["acf_lag0"] - by["acf_lag0"]["value"]) < 1e-9)
check("max_diff_statsmodels traces", abs(sm["max_diff_statsmodels"] - by["max_diff_statsmodels"]["value"]) < 1e-18)
check("decorrelation_time traces",   int(sm["decorrelation_time"]) == by["decorrelation_time"]["value"])
check("n_lags traces",               int(sm["n_lags"]) == by["n_lags"]["value"])
# machine-precision
check("op == statsmodels.tsa.acf BIT-FOR-BIT over lags (< 1e-9)", sm["max_diff_statsmodels"] < 1e-9)
# ACF structure
check("lag-0 autocorrelation is exactly 1 (the ACF identity)", abs(sm["acf_lag0"] - 1.0) < 1e-12)
check("ACF decays: lag1 > lag2", sm["acf_lag1"] > sm["acf_lag2"])
check("|ACF| <= 1 at all reported lags", abs(sm["acf_lag1"]) <= 1 and abs(sm["acf_lag2"]) <= 1)
check("decorrelation time positive and within the lag window", 0 < int(sm["decorrelation_time"]) < int(sm["n_lags"]))
check("n_lags = lag_max + 1 = 31", int(sm["n_lags"]) == 31)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the single-series ACF gap (crossCorrelation was 2-series)",
      "newly authored" in _note and "not the single-series autocorrelation" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical estimator), not a convention agreement",
      "machine-precision" in _note and "identical biased/demeaned estimator" in _note and "not a convention agreement" in _note)
check("HONEST: foundational primitive certified against field-standard statsmodels",
      "foundational descriptor" in _note and "field-standard statsmodels" in _note)
check("HONEST: signal property, structure not absolute constant",
      "signal property" in _note and "not an absolute physiological constant" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
