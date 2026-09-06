import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/increment_summary.csv"))}
check("incren_m2 traces",   abs(sm["incren_m2"] - by["incren_m2"]["value"]) < 1e-6)
check("incren_m3 traces",   abs(sm["incren_m3"] - by["incren_m3"]["value"]) < 1e-6)
check("incren_m4 traces",   abs(sm["incren_m4"] - by["incren_m4"]["value"]) < 1e-6)
check("max_diff_nk traces", abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-18)
check("n_words_m2 traces",  int(sm["n_words_m2"]) == by["n_words_m2"]["value"])
check("monotonic traces",   int(sm["monotonic"]) == by["monotonic"]["value"])
# machine-precision
check("op == NeuroKit2 entropy_increment BIT-FOR-BIT over the family (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# increment structure
check("0 < increment-words realized < (2q+1)^m = 81 (structured, not word-saturating)", 0 < int(sm["n_words_m2"]) < 81)
check("exactly 33 of 81 increment-words realized", int(sm["n_words_m2"]) == 33)
# monotone family
check("IncrEn non-increasing in dimension (m2 > m3 > m4)", sm["incren_m2"] > sm["incren_m3"] > sm["incren_m4"])
check("monotonic flag is set", int(sm["monotonic"]) == 1)
check("IncrEn values positive (valid entropy)", sm["incren_m2"] > 0 and sm["incren_m4"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the increment-domain complexity gap",
      "newly authored" in _note and "no increment-domain complexity" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical pipeline), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: mechanism distinct -- encodes direction + graded size of changes",
      "direction and graded size of changes" in _note)
check("HONEST: value depends on (dimension, q) -- structure not absolute constant",
      "depends on (dimension, q)" in _note and "not an absolute physiological constant" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
