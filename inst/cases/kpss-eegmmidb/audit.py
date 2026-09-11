import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/kpss_summary.csv"))}
check("kpss_statistic traces",    abs(sm["kpss_statistic"] - by["kpss_statistic"]["value"]) < 1e-6)
check("kpss_stat_diff_sm traces", abs(sm["kpss_stat_diff_sm"] - by["kpss_stat_diff_sm"]["value"]) < 1e-16)
check("sm_critical_5pct traces",  abs(sm["sm_critical_5pct"] - by["sm_critical_5pct"]["value"]) < 1e-4)
check("kpss_stationary traces",   int(sm["kpss_stationary"]) == by["kpss_stationary"]["value"])
check("adf_stationary traces",    int(sm["adf_stationary"]) == by["adf_stationary"]["value"])
check("both_tests_agree traces",  int(sm["both_tests_agree"]) == by["both_tests_agree"]["value"])
# machine-precision (statistic)
check("KPSS statistic == statsmodels kpss BIT-FOR-BIT (< 1e-9)", sm["kpss_stat_diff_sm"] < 1e-9)
# decision + confirmatory pair
check("KPSS statistic below the 5% critical value (fail to reject stationarity)", sm["kpss_statistic"] < sm["sm_critical_5pct"])
check("KPSS says stationary (flag set)", int(sm["kpss_stationary"]) == 1)
check("ADF says stationary (complementary test agrees)", int(sm["adf_stationary"]) == 1)
check("both tests agree the segment is stationary", int(sm["both_tests_agree"]) == 1 and int(sm["kpss_stationary"]) == 1 and int(sm["adf_stationary"]) == 1)
check("KPSS statistic is small and positive (a valid KPSS eta)", 0 < sm["kpss_statistic"] < 0.463)
check("5% KPSS critical value is ~0.463", 0.4 < sm["sm_critical_5pct"] < 0.5)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op adding the complement of adfTest (confirmatory-pair partner)",
      "newly authored" in _note and "complement of adftest" in _note)
check("HONEST: STATISTIC machine-precision (exact deterministic quantity), not a convention agreement",
      "machine-precision" in _note and "exact deterministic quantity" in _note and "not a convention agreement" in _note)
check("HONEST caveat: only the statistic is bit-exact; critical values / p from reference tables",
      "only the statistic is bit-exact" in _note and "reference tables" in _note)
check("HONEST: confirmatory-pair agreement is the finding (can disagree -> long memory)",
      "confirmatory-pair agreement" in _note and "near-unit-root or fractional integration" in _note)
check("HONEST: statsmodels cross-tool reference", "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
