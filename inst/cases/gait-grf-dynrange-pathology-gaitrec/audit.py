import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/grf_summary.csv"))}
check("t_statistic traces", abs(sm["t_statistic"] - by["t_statistic"]["value"]) < 1e-6)
for k in ("neg_log10_p","df"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-2)
check("control_patient_ratio traces", abs(sm["control_patient_ratio"] - by["control_patient_ratio"]["value"]) < 1e-4)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-15)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-15)
check("control_gt_patient traces", int(sm["control_gt_patient"]) == by["control_gt_patient"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
# double-reference bit-exact
check("twoSampleTTest == scipy.stats.ttest_ind(equal_var=False) BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("twoSampleTTest == base R t.test BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
# the finding: control DR > patient DR, large, significant
check("control dynamic range > patient (ratio > 1)", sm["control_patient_ratio"] > 1)
check("control mean DR > patient mean DR", sm["mean_control_dr"] > sm["mean_patient_dr"])
check("the group difference is overwhelmingly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("control_patient_ratio equals mean_control_dr / mean_patient_dr", abs(sm["control_patient_ratio"] - sm["mean_control_dr"]/sm["mean_patient_dr"]) < 1e-4)
check("large cohort (n_total = 707)", int(sm["n_total"]) == 707)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: REUSES the certified twoSampleTTest (new finding, not a new op)",
      "reuses" in _note and "twosamplettest" in _note and "not a new op" in _note)
check("HONEST: dynamic range from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: bit-for-bit vs scipy.stats.ttest_ind and base R",
      "ttest_ind" in _note and "bit-for-bit" in _note)
check("HONEST: the flattened-double-hump pathological-gait finding (inferential certification)",
      "flatten" in _note and "double-hump" in _note and "dynamic range" in _note and "inferential" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "ttest_ind" in case["validation"]["reference"].lower() and "t.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
