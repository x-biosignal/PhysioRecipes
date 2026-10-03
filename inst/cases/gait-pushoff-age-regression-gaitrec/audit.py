import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pushoff_age_regression_summary.csv"))}
# claims trace to the artifact
check("slope traces", abs(sm["slope"] - by["slope"]["value"]) < 1e-9)
check("slope_per_decade traces", abs(sm["slope_per_decade"] - by["slope_per_decade"]["value"]) < 1e-6)
check("intercept traces", abs(sm["intercept"] - by["intercept"]["value"]) < 1e-6)
check("r_squared traces", abs(sm["r_squared"] - by["r_squared"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df traces", int(sm["df"]) == by["df"]["value"])
check("max_diff_slope_scipy traces (bit-for-bit, == 0)", sm["max_diff_slope_scipy"] == by["max_diff_slope_scipy"]["value"] == 0)
check("max_diff_slope_lm traces (machine precision, < 1e-9)", abs(sm["max_diff_slope_lm"] - by["max_diff_slope_lm"]["value"]) < 1e-9)
check("slope_negative traces", int(sm["slope_negative"]) == by["slope_negative"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
# double reference: scipy exact, lm machine precision
check("linearRegression == scipy.stats.linregress BIT-FOR-BIT (slope |diff| == 0)", sm["max_diff_slope_scipy"] == 0)
check("linearRegression r-squared == scipy BIT-FOR-BIT (|diff| == 0)", sm["max_diff_r2_scipy"] == 0)
check("linearRegression == base R lm to machine precision (slope |diff| < 1e-9)", sm["max_diff_slope_lm"] < 1e-9)
# the finding: push-off declines with age, modest but significant
check("slope is negative (push-off declines with age)", sm["slope"] < 0 and int(sm["slope_negative"]) == 1)
check("slope_per_decade == slope * 10", abs(sm["slope_per_decade"] - sm["slope"] * 10) < 1e-6)
check("the age effect is highly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("R-squared is modest (age explains < 20% of variance) -- honest", 0 < sm["r_squared"] < 0.2)
check("df = n - 2", int(sm["df"]) == int(sm["n"]) - 2)
check("t-statistic negative and consistent with the negative slope", sm["statistic_t"] < 0)
check("healthy-control cohort (n=208)", int(sm["n"]) == 208)
check("age range honest (young-skewed upper end)", sm["age_min"] <= 20 and sm["age_max"] >= 70)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new linearRegression op (simple OLS)",
      "new op" in _note and "linearregression" in _note)
check("HONEST: push-off from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: scipy.stats.linregress bit-for-bit",
      "scipy.stats.linregress" in _note and "bit-for-bit" in _note)
check("HONEST: base R lm to machine precision",
      "stats::lm" in _note and "machine precision" in _note)
check("HONEST: modest R-squared stated (~9% / about 9%)",
      "9%" in _note or "0.094" in _note)
check("HONEST: young-skewed age distribution noted",
      "young-skewed" in _note)
check("HONEST: cross-sectional association, not causation / not longitudinal",
      "cross-sectional" in _note and "not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R lm)",
      "scipy.stats.linregress" in case["validation"]["reference"].lower() and "lm" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
