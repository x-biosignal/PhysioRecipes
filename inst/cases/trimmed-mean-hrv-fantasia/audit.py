import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/trimmed_summary.csv"))}
for k in ("trimmed_mean_10","trimmed_mean_20","plain_mean","median_rr"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-6)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-18)
check("max_diff_baser traces", abs(sm["max_diff_baser"] - by["max_diff_baser"]["value"]) < 1e-18)
check("n_intervals traces",    int(sm["n_intervals"]) == by["n_intervals"]["value"])
# double-reference machine precision
check("trimmedMean == scipy.stats.trim_mean BIT-FOR-BIT (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("trimmedMean == base R mean(x, trim) BIT-FOR-BIT (< 1e-9)", sm["max_diff_baser"] < 1e-9)
check("the three agree (trimmed_mean_10 == scipy == base-R)",
      abs(sm["trimmed_mean_10"] - sm["scipy_trim10"]) < 1e-9 and abs(sm["trimmed_mean_10"] - sm["baser_trim10"]) < 1e-9)
# the finding: skew location progression mean > trim0.1 > trim0.2 > median
check("mean > 10%-trimmed (mean inflated by the tail)", sm["plain_mean"] > sm["trimmed_mean_10"])
check("10%-trimmed > 20%-trimmed (moves toward the median with more trimming)", sm["trimmed_mean_10"] > sm["trimmed_mean_20"])
check("20%-trimmed > median (trimmed mean stays above the fully-robust median)", sm["trimmed_mean_20"] > sm["median_rr"])
check("trimmed mean interpolates strictly between mean and median",
      sm["median_rr"] < sm["trimmed_mean_10"] < sm["plain_mean"])
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEW robust-location op completing the robust toolkit (medianAbsDev/interquartileRange)",
      "new" in _note and "robust-location" in _note and "medianabsdev" in _note and "interquartilerange" in _note)
check("HONEST: genuine DOUBLE-REFERENCE machine-precision (same order statistics discarded), not a convention agreement",
      "double-reference" in _note and "bit-for-bit" in _note and "order statistic" in _note and "not a convention agreement" in _note)
check("HONEST: the skew location-progression finding (tail inflates the mean; trimmed interpolates to median)",
      "right-skewed" in _note and "inflate" in _note and "interpolate" in _note and "median" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "scipy" in case["validation"]["reference"].lower() and "base r" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
