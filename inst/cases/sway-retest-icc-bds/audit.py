import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/icc_summary.csv"))}
# claims trace to the artifact
for m in ("icc2_single", "icc2k_average", "icc1_single", "icc3_single"):
    check(f"{m} traces", abs(sm[m] - by[m]["value"]) < 1e-6)
check("max_diff_psych traces (machine precision, < 1e-9)", abs(sm["max_diff_psych"] - by["max_diff_psych"]["value"]) < 1e-9)
check("max_diff_pingouin traces (machine precision, < 1e-9)", abs(sm["max_diff_pingouin"] - by["max_diff_pingouin"]["value"]) < 1e-9)
check("good_single traces", int(sm["good_single"]) == by["good_single"]["value"])
check("excellent_average traces", int(sm["excellent_average"]) == by["excellent_average"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
check("k traces", int(sm["k"]) == by["k"]["value"])
# double reference: psych + pingouin, machine precision
check("intraclassCorrelation == pingouin.intraclass_corr to machine precision (< 1e-9)", sm["max_diff_pingouin"] < 1e-9)
check("intraclassCorrelation == psych::ICC(lmer=FALSE) to machine precision (< 1e-9)", sm["max_diff_psych"] < 1e-9)
# the finding: reliable single trial, better average
check("single-trial reliability is good (ICC(2,1) > 0.75)", sm["icc2_single"] > 0.75 and int(sm["good_single"]) == 1)
check("3-trial-average reliability is excellent (ICC(2,k) > 0.9)", sm["icc2k_average"] > 0.9 and int(sm["excellent_average"]) == 1)
check("averaging trials raises reliability (ICC(2,k) > ICC(2,1)) -- Spearman-Brown", sm["icc2k_average"] > sm["icc2_single"])
check("all ICC values are sane (0 < ICC < 1)", all(0 < sm[m] < 1 for m in ("icc1_single","icc2_single","icc3_single","icc2k_average")))
check("trial means present and positive (habituation trend documented)", sm["trial_mean_1"] > 0 and sm["trial_mean_3"] > 0)
check("design: 163 subjects x 3 trials", int(sm["n"]) == 163 and int(sm["k"]) == 3)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new intraclassCorrelation op",
      "new op" in _note and "intraclasscorrelation" in _note)
check("HONEST: sway from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: pingouin.intraclass_corr to machine precision",
      "pingouin.intraclass_corr" in _note and "machine precision" in _note)
check("HONEST: psych::ICC(lmer=FALSE) to machine precision + lmer=TRUE REML caveat",
      "psych::icc(lmer=false)" in _note and "lmer=true" in _note and "reml" in _note)
check("HONEST: good single-trial, excellent average, Spearman-Brown",
      "good test-retest reliability" in _note and "spearman-brown" in _note)
check("HONEST: within-session, NOT across days",
      "within-session" in _note and "not across days" in _note)
check("HONEST: two-tool cross reference (psych + pingouin)",
      "psych::icc(lmer=false)" in case["validation"]["reference"].lower() and "pingouin.intraclass_corr" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
