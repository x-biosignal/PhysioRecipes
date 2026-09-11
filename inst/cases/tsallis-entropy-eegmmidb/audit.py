import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/tsallis_summary.csv"))}
check("tsallis_collision traces",     abs(sm["tsallis_collision"] - by["tsallis_collision"]["value"]) < 1e-6)
check("tsallis_shannon traces",       abs(sm["tsallis_shannon"] - by["tsallis_shannon"]["value"]) < 1e-6)
check("max_diff_nk traces",           abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-18)
check("diverge_from_renyi_q2 traces", abs(sm["diverge_from_renyi_q2"] - by["diverge_from_renyi_q2"]["value"]) < 1e-6)
check("agree_at_1 traces",            abs(sm["agree_at_1"] - by["agree_at_1"]["value"]) < 1e-18)
check("monotonic traces",             int(sm["monotonic"]) == by["monotonic"]["value"])
# machine-precision
check("op == NeuroKit2 entropy_tsallis BIT-FOR-BIT over the family (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# family structure: coincide at q=1, diverge at q=2
check("Tsallis & Renyi COINCIDE at q=1 (both Shannon; |diff| ~0)", sm["agree_at_1"] < 1e-9)
check("Tsallis & Renyi DIVERGE at q=2 (|diff| > 1; non-additive vs additive)", sm["diverge_from_renyi_q2"] > 1.0)
check("q=1 Tsallis recovers Shannon (2.325), above Renyi collision-order (2.167)", abs(sm["tsallis_shannon"] - 2.3247657693) < 1e-6 and sm["tsallis_shannon"] > sm["renyi_q2"])
check("q=2 Tsallis (0.885) < q=2 Renyi (2.167) -- distinct generalizations", sm["tsallis_collision"] < sm["renyi_q2"])
# monotonic family
check("full Tsallis family monotonic decreasing (q0.5 > q1 > q2 > q3)",
      sm["tsallis_q05"] > sm["tsallis_shannon"] > sm["tsallis_collision"] > sm["tsallis_q3"])
check("monotonic flag is set (defining property)", int(sm["monotonic"]) == 1)
check("Tsallis entropies are positive (valid entropy)", sm["tsallis_collision"] > 0 and sm["tsallis_shannon"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op completing the generalized-entropy pair (non-additive Tsallis)",
      "newly authored" in _note and "non-additive tsallis family" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical formula), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: q=1 = Shannon + coincides with Renyi at 1 + diverges elsewhere = defining structure",
      "q=1 = shannon" in _note and "coincidence-with-renyi-at-1" in _note and "divergence-elsewhere" in _note)
check("HONEST: histogram/bin-count dependent -- structure not absolute value",
      "bin-count-dependent" in _note and "not an absolute physiological quantity" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
