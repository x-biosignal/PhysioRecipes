import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/mlr_summary.csv"))}
# claims trace to the artifact
check("coef_age traces", abs(sm["coef_age"] - by["coef_age"]["value"]) < 1e-6)
check("neg_log10_p_age traces", abs(sm["neg_log10_p_age"] - by["neg_log10_p_age"]["value"]) < 1e-2)
check("coef_tmt traces", abs(sm["coef_tmt"] - by["coef_tmt"]["value"]) < 1e-6)
check("p_tmt traces", abs(sm["p_tmt"] - by["p_tmt"]["value"]) < 1e-4)
check("r_squared traces", abs(sm["r_squared"] - by["r_squared"]["value"]) < 1e-6)
check("neg_log10_fp traces", abs(sm["neg_log10_fp"] - by["neg_log10_fp"]["value"]) < 1e-2)
check("max_diff_coef_lm traces (bit-for-bit, == 0)", sm["max_diff_coef_lm"] == by["max_diff_coef_lm"]["value"] == 0)
check("max_diff_coef_statsmodels traces (machine precision, < 1e-9)", abs(sm["max_diff_coef_statsmodels"] - by["max_diff_coef_statsmodels"]["value"]) < 1e-9)
check("age_dominant traces", int(sm["age_dominant"]) == by["age_dominant"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
# double reference: lm bit-for-bit, statsmodels machine precision
check("multipleRegression == base R lm BIT-FOR-BIT (coef |diff| == 0)", sm["max_diff_coef_lm"] == 0)
check("multipleRegression == statsmodels OLS to machine precision (< 1e-9)", sm["max_diff_coef_statsmodels"] < 1e-9)
# the finding: age dominant, TMT adds nothing
check("age coefficient is highly significant (-log10 p > 3)", sm["neg_log10_p_age"] > 3)
check("TMT-A coefficient is NOT significant (p > 0.05)", sm["p_tmt"] > 0.05)
check("age_dominant flag agrees (age sig, TMT not)", int(sm["age_dominant"]) == 1 and sm["neg_log10_p_age"] > 3 and sm["p_tmt"] > 0.05)
check("the overall model is significant (-log10 Fp > 3)", sm["neg_log10_fp"] > 3)
check("model explains a modest fraction (0.1 < R2 < 0.5)", 0.1 < sm["r_squared"] < 0.5)
check("age coefficient is positive (more sway with age)", sm["coef_age"] > 0)
check("TMT-A p equals the partial-correlation p (~0.5545, internal consistency)", abs(sm["p_tmt"] - 0.5545181048) < 1e-4)
check("cohort n=158", int(sm["n"]) == 158)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new multipleRegression op",
      "new op" in _note and "multipleregression" in _note)
check("HONEST: sway from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: base R lm bit-for-bit",
      "stats::lm" in _note and "bit-for-bit" in _note)
check("HONEST: statsmodels OLS to machine precision",
      "statsmodels ols" in _note and "machine precision" in _note)
check("HONEST: cognition adds essentially nothing beyond age",
      "adds essentially nothing" in _note and "age" in _note)
check("HONEST: coefficient t-test equals the partial-correlation test",
      "partial-correlation test" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (base R lm + statsmodels)",
      "stats::lm" in case["validation"]["reference"].lower() and "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
