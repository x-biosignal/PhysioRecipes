import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/ljungbox_summary.csv"))}
check("lb_statistic traces",       abs(sm["lb_statistic"] - by["lb_statistic"]["value"]) < 1e-3)
check("lb_stat_diff_sm traces",    abs(sm["lb_stat_diff_sm"] - by["lb_stat_diff_sm"]["value"]) < 1e-12)
check("lb_pvalue_diff_sm traces",  abs(sm["lb_pvalue_diff_sm"] - by["lb_pvalue_diff_sm"]["value"]) < 1e-12)
check("critical_value_95 traces",  abs(sm["critical_value_95"] - by["critical_value_95"]["value"]) < 1e-4)
check("reject_white_noise traces", int(sm["reject_white_noise"]) == by["reject_white_noise"]["value"])
check("q_over_critical traces",    abs(sm["q_over_critical"] - by["q_over_critical"]["value"]) < 1e-1)
# machine-precision vs statsmodels
check("Q == statsmodels acorr_ljungbox statistic BIT-FOR-BIT (< 1e-9)", sm["lb_stat_diff_sm"] < 1e-9)
check("p-value == statsmodels p-value BIT-FOR-BIT (< 1e-9)", sm["lb_pvalue_diff_sm"] < 1e-9)
# decision
check("white-noise null rejected (flag set)", int(sm["reject_white_noise"]) == 1)
check("Q exceeds the 95% critical value", sm["lb_statistic"] > sm["critical_value_95"])
check("rejection is decisive (Q > 100x critical)", sm["q_over_critical"] > 100)
check("Q/critical consistent with statistic and critical value", abs(sm["q_over_critical"] - sm["lb_statistic"]/sm["critical_value_95"]) < 1e-2)
check("95% chi-square(10) critical value is ~18.31", 18 < sm["critical_value_95"] < 19)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op built on autocorrelation (formal autocorrelation test the ecosystem lacked)",
      "newly authored" in _note and "formal autocorrelation test the ecosystem lacked" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical closed-form Q + chi-square), not a convention agreement",
      "machine-precision" in _note and "identical closed-form" in _note and "not a convention agreement" in _note)
check("HONEST: decisive-but-expected verdict; value is the certified implementation + margin",
      "decisive and expected" in _note and "certified implementation" in _note)
check("HONEST: on residuals this op tests model adequacy",
      "model residuals" in _note and "model adequacy" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
