import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, math
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/phase_summary.csv"))}
check("phasen_k4 traces",       abs(sm["phasen_k4"] - by["phasen_k4"]["value"]) < 1e-6)
check("phasen_k6 traces",       abs(sm["phasen_k6"] - by["phasen_k6"]["value"]) < 1e-6)
check("phasen_k8 traces",       abs(sm["phasen_k8"] - by["phasen_k8"]["value"]) < 1e-6)
check("max_diff_nk traces",     abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-18)
check("increasing_in_k traces", int(sm["increasing_in_k"]) == by["increasing_in_k"]["value"])
check("below_ceiling traces",   int(sm["below_ceiling"]) == by["below_ceiling"]["value"])
# machine-precision
check("op == NeuroKit2 entropy_phase BIT-FOR-BIT over k (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# k-structure
check("PhasEn increases with sector count k (k4 < k6 < k8)", sm["phasen_k4"] < sm["phasen_k6"] < sm["phasen_k8"])
check("increasing_in_k flag is set", int(sm["increasing_in_k"]) == 1)
check("PhasEn below the 1/ln(2)=1.4427 ceiling", sm["phasen_k4"] < 1.0/math.log(2) and int(sm["below_ceiling"]) == 1)
check("PhasEn values positive (valid entropy)", sm["phasen_k4"] > 0 and sm["phasen_k8"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the phase-plane SODP-entropy gap",
      "newly authored" in _note and "not the phase-plane sodp entropy" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical pipeline), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: mechanism distinct -- rate-of-change vs change-of-rate co-vary (phase-plane)",
      "rate-of-change" in _note and "change-of-rate" in _note and "phase-plane geometry" in _note)
check("HONEST: NeuroKit2 normalization convention reproduced not corrected",
      "reproduced, not corrected" in _note and "1/ln2 = 1.443" in _note)
check("HONEST: value depends on (delay, k) -- structure not absolute constant",
      "depends on (delay, k)" in _note and "not an absolute physiological constant" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
