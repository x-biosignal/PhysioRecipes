import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/crossmodal_dcor_summary.csv"))}
bs   = list(csv.DictReader(open("artifacts/crossmodal_dcor_by_subject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("dcor traces",        abs(sm["dcor"]        - by["dcor"]["value"])        < 1e-9)
check("p_value traces",     abs(sm["p_value"]     - by["p_value"]["value"])     < 1e-9)
check("dcor_energy traces", abs(sm["dcor_energy"] - by["dcor_energy"]["value"]) < 1e-9)
check("dcor_mean5 traces",  abs(sm["dcor_mean5"]  - by["dcor_mean5"]["value"])  < 1e-6)
check("dcor_min5 traces",   abs(sm["dcor_min5"]   - by["dcor_min5"]["value"])   < 1e-6)

# --- external cross-tool validation: distanceCorrelation == energy::dcor -----
check("op == energy::dcor to machine precision (|diff| < 1e-9)", abs(sm["dcor"] - sm["dcor_energy"]) < 1e-9)
check("the recorded abs_diff is at machine precision (< 1e-12)", sm["abs_diff"] < 1e-12)

# --- reference recovery: the true dependence structure ----------------------
check("kinematics-kinetics coupling is strong (dCor > 0.7)", sm["dcor"] > 0.7)
check("the coupling is significant (permutation p <= 0.01)", sm["p_value"] <= 0.01)
check("coupling holds across ALL five subjects (min dCor > 0.5)", sm["dcor_min5"] > 0.5)
check("the five subjects are consistent (max - min < 0.1)", (sm["dcor_max5"] - sm["dcor_min5"]) < 0.1)
check("the per-subject artifact lists all five subjects", len(bs) == int(sm["n_subjects"]) == 5)
check("every subject's dCor traces to [min5, max5]",
      all(sm["dcor_min5"] - 1e-6 <= float(r["dcor"]) <= sm["dcor_max5"] + 1e-6 for r in bs))

# --- honest scope -----------------------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("HONEST: treadmill (no forward drift) noted in the scope", "treadmill" in case["validation"]["note"].lower())
check("HONEST: cross-tool (energy::dcor), not a self-comparison", "energy::dcor" in case["validation"]["reference"])
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
