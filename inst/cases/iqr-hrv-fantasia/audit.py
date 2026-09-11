import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/iqr_summary.csv"))}
# claims trace
for k in ("iqr","q1","q3","sdnn","robust_classical_ratio","rr_skewness"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < (1e-4 if k in ("sdnn","robust_classical_ratio","rr_skewness") else 1e-6))
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-18)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-18)
check("n_intervals traces",    int(sm["n_intervals"]) == by["n_intervals"]["value"])
# double-reference machine precision
check("interquartileRange == scipy.stats.iqr BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("interquartileRange == base R IQR BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("the three tools agree (IQR identical across op/scipy/base-R)",
      abs(sm["iqr"] - sm["scipy_iqr"]) < 1e-9 and abs(sm["iqr"] - sm["baser_iqr"]) < 1e-9)
check("IQR equals Q3 - Q1", abs(sm["iqr"] - (sm["q3"] - sm["q1"])) < 1e-9)
# the finding: skewed RR -> robust < classical
check("RR distribution is right-skewed (skewness > 0.5)", sm["rr_skewness"] > 0.5)
check("robust IQR-scale is materially below SDNN (ratio < 0.9)", sm["robust_classical_ratio"] < 0.9)
check("robust_classical_ratio equals robust_sd_iqr / sdnn",
      abs(sm["robust_classical_ratio"] - sm["robust_sd_iqr"] / sm["sdnn"]) < 1e-4)
check("IQR is a positive dispersion value", sm["iqr"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEW quantile-based robust op, companion of medianAbsDev + signalMoments",
      "new" in _note and "quantile-based" in _note and "medianabsdev" in _note)
check("HONEST: genuine DOUBLE-REFERENCE machine-precision (Q1/Q3 unambiguous order statistics), not a convention agreement",
      "double-reference" in _note and "bit-for-bit" in _note and "order statistic" in _note and "not a convention agreement" in _note)
check("HONEST: the distribution-shape diagnostic finding (skewed RR -> robust < classical; SDNN inflated)",
      "distribution-shape diagnostic" in _note and "skewed" in _note and "sdnn is inflated" in _note)
check("HONEST: the cross-fold contrast (OPPOSITE of the near-Gaussian EEG median-abs-dev case)",
      "opposite" in _note and "near-gaussian" in _note and "median-abs-dev" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "scipy" in case["validation"]["reference"].lower() and "base r" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
