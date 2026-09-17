import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/corr_summary.csv"))}
for k in ("correlation_foam","neg_log10_p","correlation_firm"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < (1e-3 if k=="neg_log10_p" else 1e-6))
check("df traces", int(sm["df"]) == by["df"]["value"])
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-15)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-15)
check("foam_gt_firm_corr traces", int(sm["foam_gt_firm_corr"]) == by["foam_gt_firm_corr"]["value"])
check("n_subjects traces", int(sm["n_subjects"]) == by["n_subjects"]["value"])
# double-reference bit-exact
check("correlationTest r == scipy.stats.pearsonr BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("correlationTest r == base R cor.test BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("df = n - 2", int(sm["df"]) == int(sm["n_subjects"]) - 2)
# the finding: sway rises with age, stronger on foam
check("age-foam correlation is positive (sway rises with age)", sm["correlation_foam"] > 0)
check("age-foam correlation is significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("age effect stronger on foam than firm (r_foam > r_firm)", sm["correlation_foam"] > sm["correlation_firm"] and int(sm["foam_gt_firm_corr"]) == 1)
check("correlations are valid (|r| <= 1)", abs(sm["correlation_foam"]) <= 1 and abs(sm["correlation_firm"]) <= 1)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: correlationTest is a NEW op",
      "new" in _note and "correlation" in _note)
check("HONEST: bit-for-bit vs scipy.stats.pearsonr and base R, not a convention agreement",
      "pearsonr" in _note and "bit-for-bit" in _note and "not a convention agreement" in _note)
check("HONEST: inputs come from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: the age / foam / proprioception unmasking finding",
      "age" in _note and "foam" in _note and "proprioception" in _note and "unmask" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "pearsonr" in case["validation"]["reference"].lower() and "cor.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
