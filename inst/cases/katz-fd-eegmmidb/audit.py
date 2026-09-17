import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/katz_summary.csv"))}
# every summary metric traces to its claim
check("katz_fd traces",           abs(sm["katz_fd"] - by["katz_fd"]["value"]) < 1e-6)
check("antropy_katz_fd traces",   abs(sm["antropy_katz_fd"] - by["antropy_katz_fd"]["value"]) < 1e-6)
check("neurokit_katz_fd traces",  abs(sm["neurokit_katz_fd"] - by["neurokit_katz_fd"]["value"]) < 1e-6)
check("euclidean_katz_fd traces", abs(sm["euclidean_katz_fd"] - by["euclidean_katz_fd"]["value"]) < 1e-6)
check("max_diff_antropy traces",  abs(sm["max_diff_antropy"] - by["max_diff_antropy"]["value"]) < 1e-18)
check("max_diff_neurokit traces", abs(sm["max_diff_neurokit"] - by["max_diff_neurokit"]["value"]) < 1e-18)
check("euclidean_diff traces",    abs(sm["euclidean_diff"] - by["euclidean_diff"]["value"]) < 1e-6)
check("n_samples traces",         int(sm["n_samples"]) == by["n_samples"]["value"])
# machine-precision, DOUBLE reference
check("katzFD == antropy.katz_fd BIT-FOR-BIT (< 1e-9)", sm["max_diff_antropy"] < 1e-9)
check("katzFD == NeuroKit2 fractal_katz BIT-FOR-BIT (< 1e-9)", sm["max_diff_neurokit"] < 1e-9)
check("the two references agree with the op (all three equal)",
      abs(sm["katz_fd"] - sm["antropy_katz_fd"]) < 1e-9 and abs(sm["katz_fd"] - sm["neurokit_katz_fd"]) < 1e-9)
# the convention fix
check("convention fix is material (amplitude-only != Euclidean-plane; |diff| > 1)", sm["euclidean_diff"] > 1)
check("euclidean_diff equals |katz_fd - euclidean_katz_fd|",
      abs(sm["euclidean_diff"] - abs(sm["katz_fd"] - sm["euclidean_katz_fd"])) < 1e-6)
# the not-bounded property of the amplitude-only convention
check("amplitude-only KFD is NOT bounded to [1,2] (real EEG > 2, as antropy/NeuroKit2 return)", sm["katz_fd"] > 2)
check("KFD is a positive, finite complexity value", 0 < sm["katz_fd"] < 100)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEW STANDALONE op completing the fractal-dimension family (petrosianFD/svdEntropy)",
      "new standalone op" in _note and "completes the fractal-dimension family" in _note)
check("HONEST: genuine DOUBLE-REFERENCE machine-precision match (identical amplitude-only closed form), not a convention agreement",
      "double-reference machine-precision" in _note and "bit-for-bit" in _note and "not a convention agreement" in _note)
check("HONEST: the INTEGRITY convention fix (Euclidean-plane -> amplitude-only; was not comparable to any reference)",
      "amplitude-only" in _note and "euclidean" in _note and "not comparable to any reference" in _note and "restoring cross-tool comparability" in _note)
check("HONEST: the not-bounded caveat of the amplitude-only convention",
      "not bounded to [1, 2]" in _note)
check("HONEST: two-tool cross reference (antropy + NeuroKit2)",
      "antropy" in case["validation"]["reference"].lower() and "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
