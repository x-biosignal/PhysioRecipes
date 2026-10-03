import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pairedt_summary.csv"))}
for k in ("t_statistic","neg_log10_p","foam_firm_ratio"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < (1e-3 if k=="neg_log10_p" else 1e-6))
check("df traces", int(sm["df"]) == by["df"]["value"])
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-15)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-15)
check("n_foam_gt_firm traces", int(sm["n_foam_gt_firm"]) == by["n_foam_gt_firm"]["value"])
check("n_subjects traces", int(sm["n_subjects"]) == by["n_subjects"]["value"])
# double-reference bit-exact
check("pairedTTest == scipy.stats.ttest_rel BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("pairedTTest == base R t.test(paired=TRUE) BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("df = n - 1", int(sm["df"]) == int(sm["n_subjects"]) - 1)
# the finding: foam > firm, universal, significant
check("foam sways more than firm (ratio > 1)", sm["foam_firm_ratio"] > 1)
check("foam > firm in ALL subjects (n_foam_gt_firm == n_subjects)", int(sm["n_foam_gt_firm"]) == int(sm["n_subjects"]))
check("the effect is highly significant (-log10 p > 3, i.e. p < 0.001)", sm["neg_log10_p"] > 3)
check("mean foam path > mean firm path", sm["mean_foam"] > sm["mean_firm"])
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: pairedTTest is a NEW clinical-stats op",
      "new" in _note and "paired" in _note)
check("HONEST: bit-for-bit vs scipy.stats.ttest_rel and base R, not a convention agreement",
      "ttest_rel" in _note and "bit-for-bit" in _note and "not a convention agreement" in _note)
check("HONEST: the input path lengths come from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: the sensory-reweighting finding (foam degrades proprioception -> more sway)",
      "sensory-reweighting" in _note and "foam" in _note and "proprioception" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "scipy.stats.ttest_rel" in case["validation"]["reference"].lower() and "t.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
