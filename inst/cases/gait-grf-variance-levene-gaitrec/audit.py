import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/levene_summary.csv"))}
# claims trace to the artifact
check("f_statistic traces", abs(sm["f_statistic"] - by["f_statistic"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df1 traces", int(sm["df1"]) == by["df1"]["value"])
check("df2 traces", int(sm["df2"]) == by["df2"]["value"])
check("max_diff_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("max_diff_car traces (machine precision, < 1e-9)", abs(sm["max_diff_car"] - by["max_diff_car"]["value"]) < 1e-9)
check("bartlett_p traces", abs(sm["bartlett_p"] - by["bartlett_p"]["value"]) < 1e-4)
check("variances_differ traces", int(sm["variances_differ"]) == by["variances_differ"]["value"])
check("bartlett_disagrees traces", int(sm["bartlett_disagrees"]) == by["bartlett_disagrees"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
# double reference: scipy + car, machine precision
check("leveneTest == scipy.stats.levene to machine precision (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("leveneTest == car::leveneTest to machine precision (< 1e-9)", sm["max_diff_car"] < 1e-9)
# the finding: variances differ (robust), bartlett disagrees, HC most variable
check("robust Levene finds variances differ (p < 0.05)", sm["levene_p"] < 0.05 and int(sm["variances_differ"]) == 1)
check("classical Bartlett does NOT at 0.05 (p > 0.05)", sm["bartlett_p"] > 0.05)
check("Levene and Bartlett disagree", int(sm["bartlett_disagrees"]) == 1 and sm["levene_p"] < 0.05 < sm["bartlett_p"])
sds = {k: sm[f"sd_{k}"] for k in ["HC","A","K","H","C"]}
check("healthy controls are the MOST variable (largest SD)", max(sds, key=sds.get) == "HC")
check("pathology classes are tighter (all pathology SD < HC SD)", all(sds[k] < sds["HC"] for k in ["A","K","H","C"]))
check("5 groups (df1=4), large cohort (n=1844)", int(sm["df1"]) == 4 and int(sm["n"]) == 1844)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new leveneTest op",
      "new op" in _note and "levenetest" in _note)
check("HONEST: dynamic range from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: scipy.stats.levene to machine precision",
      "scipy.stats.levene" in _note and "machine precision" in _note)
check("HONEST: car::leveneTest to machine precision",
      "car::levenetest(center=median)" in _note and "machine precision" in _note)
check("HONEST: robust vs classical disagree, robust preferred",
      "disagree" in _note and "robust levene is preferred" in _note)
check("HONEST: pathology flattens AND constrains the GRF",
      "flattens" in _note and "constrains" in _note)
check("HONEST: Bartlett reported for contrast only, not a competing claim",
      "contrast, not as a competing claim" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + car)",
      "scipy.stats.levene" in case["validation"]["reference"].lower() and "car::levenetest" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
