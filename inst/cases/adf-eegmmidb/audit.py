import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/adf_summary.csv"))}
check("adf_statistic traces",         abs(sm["adf_statistic"] - by["adf_statistic"]["value"]) < 1e-6)
check("adf_stat_diff_sm traces",      abs(sm["adf_stat_diff_sm"] - by["adf_stat_diff_sm"]["value"]) < 1e-16)
check("sm_critical_5pct traces",      abs(sm["sm_critical_5pct"] - by["sm_critical_5pct"]["value"]) < 1e-4)
check("reject_unit_root traces",      int(sm["reject_unit_root"]) == by["reject_unit_root"]["value"])
check("margin_below_critical traces", abs(sm["margin_below_critical"] - by["margin_below_critical"]["value"]) < 1e-2)
check("n_obs traces",                 int(sm["n_obs"]) == by["n_obs"]["value"])
# machine-precision (statistic)
check("ADF statistic == statsmodels adfuller BIT-FOR-BIT (< 1e-9)", sm["adf_stat_diff_sm"] < 1e-9)
# decision
check("ADF statistic is below the 5% critical value (unit root rejected)", sm["adf_statistic"] < sm["sm_critical_5pct"])
check("reject_unit_root flag set (stationary)", int(sm["reject_unit_root"]) == 1)
check("rejection is decisive (margin > 10 below critical)", sm["margin_below_critical"] < -10)
check("margin equals statistic minus critical", abs(sm["margin_below_critical"] - (sm["adf_statistic"] - sm["sm_critical_5pct"])) < 1e-3)
check("5% Dickey-Fuller critical value is ~ -2.86", -3.0 < sm["sm_critical_5pct"] < -2.7)
check("n_obs = N - 1 - lag = 1600 - 1 - 1 = 1598", int(sm["n_obs"]) == 1598)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op adding the stationarity test the ecosystem lacked",
      "newly authored" in _note and "formal stationarity test the ecosystem lacked" in _note)
check("HONEST: STATISTIC is machine-precision (exact OLS quantity), not a convention agreement",
      "exact ols regression quantity" in _note and "not a convention agreement" in _note)
check("HONEST caveat: only the statistic is bit-exact; critical values / p from MacKinnon tables",
      "only the statistic is bit-exact" in _note and "mackinnon response-surface reference tables" in _note)
check("HONEST: decisive-but-expected stationarity verdict justifies the companion folds' assumption",
      "decisive-but-expected verdict" in _note and "justifies the stationarity assumption" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
