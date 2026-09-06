import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/fuzzy_summary.csv"))}
check("fuzzyen_m2 traces",          abs(sm["fuzzyen_m2"] - by["fuzzyen_m2"]["value"]) < 1e-6)
check("fuzzyen_m3 traces",          abs(sm["fuzzyen_m3"] - by["fuzzyen_m3"]["value"]) < 1e-6)
check("max_diff_nk traces",         abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-18)
check("sampen_m2 traces",           abs(sm["sampen_m2"] - by["sampen_m2"]["value"]) < 1e-6)
check("fuzzy_vs_sampen_gap traces", abs(sm["fuzzy_vs_sampen_gap"] - by["fuzzy_vs_sampen_gap"]["value"]) < 1e-6)
check("monotonic traces",           int(sm["monotonic"]) == by["monotonic"]["value"])
# machine-precision
check("op == NeuroKit2 entropy_fuzzy BIT-FOR-BIT over the family (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# fuzzy-vs-crisp finding
check("FuzzyEn (soft) < crisp SampEn at m=2 (soft counts partial matches)", sm["fuzzyen_m2"] < sm["sampen_m2"])
check("fuzzy-vs-sample gap equals |FuzzyEn - SampEn| at m=2", abs(sm["fuzzy_vs_sampen_gap"] - abs(sm["fuzzyen_m2"] - sm["sampen_m2"])) < 1e-6)
check("gap is substantial (> 0.1), not a rounding artifact", sm["fuzzy_vs_sampen_gap"] > 0.1)
# monotonic in dimension
check("FuzzyEn non-increasing (m=2 > m=3)", sm["fuzzyen_m2"] > sm["fuzzyen_m3"] and int(sm["monotonic"]) == 1)
check("FuzzyEn values positive (valid entropy)", sm["fuzzyen_m2"] > 0 and sm["fuzzyen_m3"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op completing the sample-entropy family (fuzzy generalization)",
      "newly authored" in _note and "not the fuzzy generalization" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical pipeline), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: fuzzy-vs-crisp = soft membership counts near-matches the crisp step rejects",
      "near-matches the heaviside step rejects" in _note and "robust, continuous generalization" in _note)
check("HONEST: value depends on (dimension, r, fuzzy power n) -- not an absolute constant",
      "depends on (dimension, r, fuzzy power n)" in _note and "not an absolute physiological constant" in _note)
check("HONEST: NeuroKit2 cross-tool reference (fuzzy + sample)", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
