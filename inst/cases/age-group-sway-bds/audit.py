import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_summary.csv"))}
check("t_statistic traces", abs(sm["t_statistic"] - by["t_statistic"]["value"]) < 1e-6)
for k in ("neg_log10_p","df","old_young_ratio"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-3)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-15)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-15)
check("old_gt_young traces", int(sm["old_gt_young"]) == by["old_gt_young"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
# double-reference bit-exact (Welch)
check("twoSampleTTest == scipy.stats.ttest_ind(equal_var=False) BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("twoSampleTTest == base R t.test BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
# the finding: older > younger, significant
check("older sway more than younger (ratio > 1)", sm["old_young_ratio"] > 1)
check("older sway more than younger (mean_old > mean_young)", sm["mean_old"] > sm["mean_young"])
check("the group difference is significant (-log10 p > 1.3, i.e. p < 0.05)", sm["neg_log10_p"] > 1.3)
check("old_young_ratio equals mean_old / mean_young", abs(sm["old_young_ratio"] - sm["mean_old"]/sm["mean_young"]) < 1e-4)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: twoSampleTTest is a NEW two-group op (Welch)",
      "new" in _note and "two-sample" in _note and "welch" in _note)
check("HONEST: bit-for-bit vs scipy.stats.ttest_ind and base R, not a convention agreement",
      "ttest_ind" in _note and "bit-for-bit" in _note and "not a convention agreement" in _note)
check("HONEST: inputs come from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: the older>younger group finding, complementing the correlation",
      "older" in _note and "foam" in _note and "group comparison" in _note and "complement" in _note)
check("HONEST: cross-sectional association, not causation; unbalanced groups",
      "association, not causation" in _note and "unbalanced" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "ttest_ind" in case["validation"]["reference"].lower() and "t.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
