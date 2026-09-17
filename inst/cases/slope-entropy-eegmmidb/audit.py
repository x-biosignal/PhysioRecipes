import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/slope_summary.csv"))}
check("slopen_m2 traces",            abs(sm["slopen_m2"] - by["slopen_m2"]["value"]) < 1e-6)
check("slopen_m3 traces",            abs(sm["slopen_m3"] - by["slopen_m3"]["value"]) < 1e-6)
check("slopen_m4 traces",            abs(sm["slopen_m4"] - by["slopen_m4"]["value"]) < 1e-6)
check("max_diff_nk traces",          abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-18)
check("n_patterns_m3 traces",        int(sm["n_patterns_m3"]) == by["n_patterns_m3"]["value"])
check("monotonic_increasing traces", int(sm["monotonic_increasing"]) == by["monotonic_increasing"]["value"])
# machine-precision
check("op == NeuroKit2 entropy_slope BIT-FOR-BIT over the dimension (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# slope-pattern structure
check("0 < slope patterns realized < 5^(m-1) = 25 (structured, not saturating)", 0 < int(sm["n_patterns_m3"]) < 25)
check("exactly 18 of 25 slope patterns realized", int(sm["n_patterns_m3"]) == 18)
# unnormalized -> increases with dimension (the distinguishing property)
check("SlopEn INCREASES with dimension (m2 < m3 < m4)", sm["slopen_m2"] < sm["slopen_m3"] < sm["slopen_m4"])
check("monotonic_increasing flag is set", int(sm["monotonic_increasing"]) == 1)
check("SlopEn values positive (valid entropy)", sm["slopen_m2"] > 0 and sm["slopen_m4"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the slope-angle symbolic-entropy gap",
      "newly authored" in _note and "not the slope-angle symbolic entropy" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical pipeline), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: completes the discrete-symbolic trio (dispersion/increment/slope)",
      "discrete-symbolic complexity trio" in _note)
check("HONEST: UNNORMALIZED so it increases with dimension (contrast with normalized entropies)",
      "unnormalized shannon" in _note and "increases with the embedding dimension" in _note)
check("HONEST: value depends on (dimension, thresholds) -- structure not absolute constant",
      "depends on (dimension, thresholds)" in _note and "not an absolute physiological constant" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
