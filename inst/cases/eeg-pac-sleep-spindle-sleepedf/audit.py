import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pac_summary.csv"))}
pd   = list(csv.DictReader(open("artifacts/pac_phase_distribution.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("pac_mi traces",       abs(sm["pac_mi"]       - by["pac_mi"]["value"])       < 1e-9)
check("tensorpac_mi traces", abs(sm["tensorpac_mi"] - by["tensorpac_mi"]["value"]) < 1e-9)
check("surrogate_z traces",  abs(sm["surrogate_z"]  - by["surrogate_z"]["value"])  < 1e-4)
check("n_exceed traces",     int(sm["n_exceed"])    == by["n_exceed"]["value"])

# --- external cross-tool validation: phaseAmplitudeCoupling == tensorpac -----
check("op == tensorpac to machine precision (|diff| < 1e-9)", abs(sm["pac_mi"] - sm["tensorpac_mi"]) < 1e-9)
check("the recorded abs_diff is at machine precision (< 1e-12)", sm["abs_diff"] < 1e-12)

# --- reference recovery: the coupling is real -------------------------------
check("SO-spindle coupling is present (MI > 0)", sm["pac_mi"] > 0)
check("coupling is significant vs a circular-shift null (z >= 3)", sm["surrogate_z"] >= 3)
check("observed MI exceeds every surrogate (200/200)", int(sm["n_exceed"]) == int(sm["n_surrogates"]) == 200)
check("observed MI is far above the surrogate mean (>= 5x)", sm["pac_mi"] >= 5 * sm["surrogate_mean"])
check("the bands are SO phase (0.5-1.25) and spindle amp (12-15)",
      sm["phase_lo"] == 0.5 and sm["phase_hi"] == 1.25 and sm["amp_lo"] == 12 and sm["amp_hi"] == 15)

# --- the phase-amplitude distribution artifact is a proper 18-bin distribution
check("phase distribution has 18 bins", len(pd) == 18)
check("phase distribution is normalized (sums ~ 1)",
      abs(sum(float(r["norm_mean_amp"]) for r in pd) - 1.0) < 1e-4)
check("the distribution is modulated (peak bin > uniform 1/18)",
      max(float(r["norm_mean_amp"]) for r in pd) > 1.0 / 18)

# --- honest scope -----------------------------------------------------------
check("HONEST: identical phase+amp fed to both engines (validates the MI computation)",
      "identical phase" in case["validation"]["note"].lower())
check("HONEST: cross-tool (tensorpac), not a self-comparison", "tensorpac" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
