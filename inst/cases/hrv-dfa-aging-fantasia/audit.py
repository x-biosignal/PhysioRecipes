import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/dfa_summary.csv"))}
bs   = list(csv.DictReader(open("artifacts/dfa_by_subject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("alpha1 traces",        abs(sm["alpha1_f1y01"]      - by["alpha1"]["value"])        < 1e-6)
check("young_mean_a1 traces", abs(sm["young_mean_alpha1"] - by["young_mean_a1"]["value"]) < 1e-6)
check("old_mean_a1 traces",   abs(sm["old_mean_alpha1"]   - by["old_mean_a1"]["value"])   < 1e-6)
check("aging_effect traces",  abs(sm["aging_effect"]      - by["aging_effect"]["value"])  < 1e-6)
check("abs_diff claim is ~0 (machine precision)", by["abs_diff"]["value"] < 1e-9)

# --- external cross-tool validation: ecgDFA == independent standard DFA ------
check("ecgDFA == independent standard-DFA to machine precision (< 1e-9)", sm["max_diff_vs_independent_dfa"] < 1e-9)
check("the agreement is at machine precision (< 1e-12)", sm["max_diff_vs_independent_dfa"] < 1e-12)
check("every subject matches the independent DFA to machine precision",
      all(float(r["diff_vs_ref"]) < 1e-9 for r in bs))

# --- reference recovery: the aging effect -----------------------------------
check("aging effect is positive (elderly alpha1 > young)", sm["aging_effect"] > 0)
check("elderly mean alpha1 exceeds young mean", sm["old_mean_alpha1"] > sm["young_mean_alpha1"])
check("young alpha1 is near healthy fractal scaling (0.8-1.3)", 0.8 < sm["young_mean_alpha1"] < 1.3)
check("elderly alpha1 is elevated toward Brownian (> 1.2)", sm["old_mean_alpha1"] > 1.2)
check("EVERY elderly subject is above the young mean (consistent effect)",
      all(float(r["alpha1"]) > sm["young_mean_alpha1"] for r in bs if r["group"] == "old"))
check("5 young + 5 elderly subjects", int(sm["n_young"]) == 5 and int(sm["n_old"]) == 5 and len(bs) == 10)

# --- honest scope -----------------------------------------------------------
check("HONEST: machine precision vs an INDEPENDENT reimplementation (different fitter)",
      "independent" in case["validation"]["note"].lower() and ".fast_lm" in case["validation"]["note"])
check("HONEST: nolds agreement looser (~0.03-0.1), DFA is implementation-sensitive",
      "nolds" in case["validation"]["note"].lower() and "implementation-sensitive" in case["validation"]["note"].lower())
check("HONEST: this fold exercises the ecgDFA bug fix (0.3.2, was NA on long RR)",
      "bug fix" in case["validation"]["note"].lower() and "na" in case["validation"]["note"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
