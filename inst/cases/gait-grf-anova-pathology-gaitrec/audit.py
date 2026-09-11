import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/grf_anova_summary.csv"))}
# claims trace to the artifact
check("F_statistic traces", abs(sm["F_statistic"] - by["F_statistic"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df1 traces", int(sm["df1"]) == by["df1"]["value"])
check("df2 traces", int(sm["df2"]) == by["df2"]["value"])
check("hc_pathology_ratio traces", abs(sm["hc_pathology_ratio"] - by["hc_pathology_ratio"]["value"]) < 1e-4)
check("max_diff_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("max_diff_baser traces (bit-for-bit, == 0)", sm["max_diff_baser"] == by["max_diff_baser"]["value"] == 0)
check("hc_gt_pathology traces", int(sm["hc_gt_pathology"]) == by["hc_gt_pathology"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
check("k_groups traces", int(sm["k_groups"]) == by["k_groups"]["value"])
# double reference: base R exact, scipy machine precision
check("oneWayAnova == base R oneway.test(var.equal=TRUE) BIT-FOR-BIT (|diff| == 0)", sm["max_diff_baser"] == 0)
check("oneWayAnova == scipy.stats.f_oneway to machine precision (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
# the finding: control flattening shared across pathology classes, large, significant
classes = ["HC","A","K","H","C"]
means = {k: sm[f"mean_{k}"] for k in classes}
ns    = {k: int(sm[f"n_{k}"]) for k in classes}
check("healthy-control mean dynamic range exceeds EVERY pathology class",
      all(means["HC"] > means[k] for k in ["A","K","H","C"]))
pooled = sum(ns[k]*means[k] for k in ["A","K","H","C"]) / sum(ns[k] for k in ["A","K","H","C"])
check("hc_pathology_ratio equals mean_HC / pooled-pathology mean", abs(sm["hc_pathology_ratio"] - means["HC"]/pooled) < 1e-3)
check("control / pathology ratio > 1 (flattening)", sm["hc_pathology_ratio"] > 1)
check("the omnibus group difference is overwhelmingly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("df1 = k - 1 and df2 = n_total - k", int(sm["df1"]) == int(sm["k_groups"]) - 1 and int(sm["df2"]) == int(sm["n_total"]) - int(sm["k_groups"]))
check("n_total = sum of per-class n", int(sm["n_total"]) == sum(ns.values()))
check("five classes (k = 5), large cohort (n_total = 1844)", int(sm["k_groups"]) == 5 and int(sm["n_total"]) == 1844)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new oneWayAnova op (generalisation of twoSampleTTest)",
      "new op" in _note and "onewayanova" in _note)
check("HONEST: dynamic range from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: base R oneway.test(var.equal=TRUE) bit-for-bit",
      "oneway.test" in _note and "bit-for-bit" in _note)
check("HONEST: scipy.stats.f_oneway to machine precision",
      "f_oneway" in _note and "machine precision" in _note)
check("HONEST: flattening is a SHARED signature, not knee-specific",
      "flatten" in _note and "shared" in _note and "not knee-specific" in _note)
check("HONEST: omnibus F driven by the healthy-vs-pathology contrast",
      "driven" in _note and "healthy-vs-pathology" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "f_oneway" in case["validation"]["reference"].lower() and "oneway.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
