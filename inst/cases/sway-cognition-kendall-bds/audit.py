import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_cognition_kendall_summary.csv"))}
# claims trace to the artifact
check("tau_statistic traces", abs(sm["tau_statistic"] - by["tau_statistic"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("z_statistic traces", abs(sm["z_statistic"] - by["z_statistic"]["value"]) < 1e-4)
check("max_diff_scipy traces (bit-for-bit, == 0)", sm["max_diff_scipy"] == by["max_diff_scipy"]["value"] == 0)
check("max_diff_baser traces (bit-for-bit, == 0)", sm["max_diff_baser"] == by["max_diff_baser"]["value"] == 0)
check("tau_positive traces", int(sm["tau_positive"]) == by["tau_positive"]["value"])
check("pearson_r traces", abs(sm["pearson_r"] - by["pearson_r"]["value"]) < 1e-4)
check("spearman_rho traces", abs(sm["spearman_rho"] - by["spearman_rho"]["value"]) < 1e-4)
check("n traces", int(sm["n"]) == by["n"]["value"])
# double reference: scipy AND base R bit-for-bit
check("kendallTau == scipy.stats.kendalltau BIT-FOR-BIT (|diff| == 0)", sm["max_diff_scipy"] == 0)
check("kendallTau == base R cor.test(kendall) BIT-FOR-BIT (|diff| == 0)", sm["max_diff_baser"] == 0)
# the finding: positive cognitive-motor association, monotonic > linear
check("association is positive (slower TMT-A -> more sway)", sm["tau_statistic"] > 0 and int(sm["tau_positive"]) == 1)
check("highly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("z-statistic is positive and large (consistent with positive tau)", sm["z_statistic"] > 3)
check("rank correlations exceed Pearson (monotonic > linear): spearman > pearson", sm["spearman_rho"] > sm["pearson_r"])
check("all three coefficients agree in sign (positive)", sm["tau_statistic"] > 0 and sm["spearman_rho"] > 0 and sm["pearson_r"] > 0)
check("tau-b is more conservative than Spearman rho (tau < rho, typical)", sm["tau_statistic"] < sm["spearman_rho"])
check("cohort n=158", int(sm["n"]) == 158)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new kendallTau op (third rank-correlation method)",
      "new op" in _note and "kendalltau" in _note)
check("HONEST: sway from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: scipy.stats.kendalltau bit-for-bit",
      "scipy.stats.kendalltau" in _note and "bit-for-bit" in _note)
check("HONEST: base R cor.test(method='kendall') bit-for-bit",
      "cor.test(method='kendall')" in _note)
check("HONEST: monotonic > linear, so a rank correlation is preferred",
      "monotonic" in _note and "rank correlation is preferred" in _note)
check("HONEST: marginal/unadjusted, age a shared correlate (confounding)",
      "marginal" in _note and "age" in _note and "confounding" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "kendalltau" in case["validation"]["reference"].lower() and "cor.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
