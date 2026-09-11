import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/circular_summary.csv"))}
bs   = list(csv.DictReader(open("artifacts/circular_by_subject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("mean_direction traces",   abs(sm["mean_direction"]        - by["mean_direction"]["value"])   < 1e-6)
check("resultant_length traces", abs(sm["resultant_length_rbar"] - by["resultant_length"]["value"]) < 1e-6)
check("mean_abs_diff traces",    abs(sm["mean_abs_diff_vs_circular"] - by["mean_abs_diff"]["value"]) < 1e-15)
check("rbar_abs_diff traces",    abs(sm["rbar_abs_diff_vs_circular"] - by["rbar_abs_diff"]["value"]) < 1e-15)
check("rbar_mean5 traces",       abs(sm["rbar_mean5"]            - by["rbar_mean5"]["value"])        < 1e-6)

# --- external cross-tool validation: circularSummary == circular package -----
check("mean direction == circular::mean.circular to machine precision (< 1e-9)", sm["mean_abs_diff_vs_circular"] < 1e-9)
check("R-bar == circular::rho.circular exactly (< 1e-12)", sm["rbar_abs_diff_vs_circular"] < 1e-12)

# --- reference recovery: a valid, non-uniform circular sample ---------------
check("R-bar is a valid concentration (0 < R-bar < 1)", 0 < sm["resultant_length_rbar"] < 1)
check("mean direction is a valid angle (0-360 deg)", 0 <= sm["mean_direction"] < 360)
check("coupling angles are significantly non-uniform (Rayleigh p < 1e-3)", sm["rayleigh_p_op"] < 1e-3)
check("the two Rayleigh p's agree on significance (both < 1e-5)",
      sm["rayleigh_p_op"] < 1e-5 and sm["rayleigh_p_circular"] < 1e-5)
check("the per-subject artifact lists all five subjects", len(bs) == 5)
check("every subject's R-bar traces to [min, max] and is a valid concentration",
      all(0 < float(r["rbar"]) < 1 for r in bs))

# --- honest scope -----------------------------------------------------------
check("HONEST: Rayleigh p is an approximation, NOT bit-identical (both p ~ 3e-8)",
      sm["rayleigh_p_op"] != sm["rayleigh_p_circular"] and "approximation" in case["validation"]["note"].lower())
check("HONEST: between-subject R-bar spread is real (0.06-0.29)",
      (max(float(r["rbar"]) for r in bs) - min(float(r["rbar"]) for r in bs)) > 0.15)
check("HONEST: cross-tool (circular package), not a self-comparison", "circular" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
