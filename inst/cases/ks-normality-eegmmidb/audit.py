import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/ks_summary.csv"))}
check("ks_statistic traces",   abs(sm["ks_statistic"] - by["ks_statistic"]["value"]) < 1e-6)
check("ks_pvalue traces",      abs(sm["ks_pvalue"] - by["ks_pvalue"]["value"]) < 1e-4)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-18)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-18)
check("jb_statistic traces",   abs(sm["jb_statistic"] - by["jb_statistic"]["value"]) < 1e-4)
check("jb_pvalue traces",      abs(sm["jb_pvalue"] - by["jb_pvalue"]["value"]) < 1e-6)
check("tests_disagree traces", int(sm["tests_disagree"]) == by["tests_disagree"]["value"])
check("n_samples traces",      int(sm["n_samples"]) == by["n_samples"]["value"])
# double-reference machine precision
check("ksNormalityTest D == scipy.stats.kstest BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("ksNormalityTest D == base R ks.test BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("the three agree (D identical across op/scipy/base-R)",
      abs(sm["ks_statistic"] - sm["scipy_ks_D"]) < 1e-9 and abs(sm["ks_statistic"] - sm["baser_ks_D"]) < 1e-9)
# the finding: KS accepts, JB rejects -> disagree
check("KS does NOT reject normality (p > 0.05)", sm["ks_pvalue"] > 0.05)
check("Jarque-Bera DOES reject normality (p < 0.05)", sm["jb_pvalue"] < 0.05)
check("the two normality tests reach opposite verdicts (disagree flag set)", int(sm["tests_disagree"]) == 1)
check("D is a valid distance in [0,1]", 0 < sm["ks_statistic"] < 1)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEW empirical-CDF normality test complementary to jarqueBeraTest",
      "new" in _note and ("empirical-cdf" in _note or "distribution-shape" in _note) and "jarqueberatest" in _note)
check("HONEST: genuine machine-precision (D an unambiguous order statistic), not a convention agreement",
      "bit-for-bit" in _note and "order statistic" in _note and "not a convention agreement" in _note)
check("HONEST: the KS-vs-JB disagreement finding (test-dependent normality)",
      "disagree" in _note and "test-dependent" in _note)
check("HONEST: the Lilliefors / anti-conservative p-value caveat (D statistic is exact)",
      "anti-conservative" in _note and "lilliefors" in _note and "d statistic is exact" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "scipy" in case["validation"]["reference"].lower() and "base r" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
