import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pacf_summary.csv"))}
check("pacf_lag1 traces",              abs(sm["pacf_lag1"] - by["pacf_lag1"]["value"]) < 1e-6)
check("pacf_lag2 traces",              abs(sm["pacf_lag2"] - by["pacf_lag2"]["value"]) < 1e-6)
check("pacf_lag0 traces",              abs(sm["pacf_lag0"] - by["pacf_lag0"]["value"]) < 1e-9)
check("max_diff_statsmodels traces",   abs(sm["max_diff_statsmodels"] - by["max_diff_statsmodels"]["value"]) < 1e-16)
check("pacf_acf_lag1_identity traces", abs(sm["pacf_acf_lag1_identity"] - by["pacf_acf_lag1_identity"]["value"]) < 1e-12)
check("n_lags traces",                 int(sm["n_lags"]) == by["n_lags"]["value"])
# machine-precision
check("op == statsmodels.tsa.pacf(ldb) BIT-FOR-BIT over lags (< 1e-9)", sm["max_diff_statsmodels"] < 1e-9)
# structure
check("lag-0 PACF is 1 by convention", abs(sm["pacf_lag0"] - 1.0) < 1e-12)
check("lag-1 PACF == lag-1 ACF (the definitional identity, ~0 diff)", sm["pacf_acf_lag1_identity"] < 1e-9)
check("lag-2 PACF strongly negative (oscillatory AR(2)-like, < -0.3)", sm["pacf_lag2"] < -0.3)
check("|PACF| <= 1 at reported lags", abs(sm["pacf_lag1"]) <= 1 and abs(sm["pacf_lag2"]) <= 1)
check("n_lags = lag_max + 1 = 21", int(sm["n_lags"]) == 21)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op building on autocorrelation, completing the ACF/PACF pair",
      "newly authored" in _note and "complete the acf/pacf pair" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical Levinson-Durbin), not a convention agreement",
      "machine-precision" in _note and "identical levinson-durbin" in _note and "not a convention agreement" in _note)
check("HONEST: matches biased ldb/ywm; unbiased yw/ld and ols differ by construction (not the target)",
      "not the target" in _note and "differ by construction" in _note)
check("HONEST: lag-1 = ACF-lag-1 identity + lag-2 negative = oscillatory alpha AR(2) structure",
      "definitional identity" in _note and "oscillatory ar(2)-like process" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
