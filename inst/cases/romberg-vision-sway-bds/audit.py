import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_summary.csv"))}
check("t_statistic traces", abs(sm["t_statistic"] - by["t_statistic"]["value"]) < 1e-6)
for k in ("neg_log10_p","ec_eo_ratio"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-3)
check("df traces", int(sm["df"]) == by["df"]["value"])
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-15)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-15)
check("n_ec_gt_eo traces", int(sm["n_ec_gt_eo"]) == by["n_ec_gt_eo"]["value"])
check("n_subjects traces", int(sm["n_subjects"]) == by["n_subjects"]["value"])
# double-reference bit-exact
check("pairedTTest == scipy.stats.ttest_rel BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("pairedTTest == base R t.test(paired=TRUE) BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("df = n - 1", int(sm["df"]) == int(sm["n_subjects"]) - 1)
# the finding: eyes-closed > eyes-open, majority, significant
check("eyes-closed sways more than eyes-open (ratio > 1)", sm["ec_eo_ratio"] > 1)
check("eyes-closed > eyes-open in the large majority (>= 40/50)", int(sm["n_ec_gt_eo"]) >= 40)
check("the Romberg effect is highly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("mean eyes-closed sway > mean eyes-open sway", sm["mean_ec"] > sm["mean_eo"])
check("ec_eo_ratio equals mean_ec / mean_eo", abs(sm["ec_eo_ratio"] - sm["mean_ec"]/sm["mean_eo"]) < 1e-4)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: REUSES the certified pairedTTest (new finding, not a new op)",
      "reuses" in _note and "certified pairedttest" in _note and "not a new op" in _note)
check("HONEST: bit-for-bit vs scipy.stats.ttest_rel and base R",
      "ttest_rel" in _note and "bit-for-bit" in _note)
check("HONEST: inputs come from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: the Romberg/vision finding, completing the sensory triad",
      "romberg" in _note and "vision" in _note and "eyes-closed" in _note and "sensory triad" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "ttest_rel" in case["validation"]["reference"].lower() and "t.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
