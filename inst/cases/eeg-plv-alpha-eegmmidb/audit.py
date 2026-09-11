import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/plv_summary.csv"))}
hist = list(csv.DictReader(open("artifacts/plv_phasediff_hist.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("plv traces",            abs(sm["plv"]            - by["plv"]["value"])            < 1e-9)
check("plv_scipy traces",      abs(sm["plv_scipy"]      - by["plv_scipy"]["value"])      < 1e-9)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-12)
check("formula_diff traces",   abs(sm["formula_diff"]   - by["formula_diff"]["value"])   < 1e-15)
check("plv_locked traces",     abs(sm["plv_locked"]     - by["plv_locked"]["value"])     < 1e-6)
check("plv_unlocked traces",   abs(sm["plv_unlocked"]   - by["plv_unlocked"]["value"])   < 1e-6)

# --- three-way validation ----------------------------------------------------
check("op == scipy Hilbert-band PLV (agreement < 1e-3, phase-robust)", sm["max_diff_scipy"] < 1e-3)
check("PLV summation formula is exact (< 1e-9)", sm["formula_diff"] < 1e-9)
check("ground truth: phase-locked PLV near 1 (> 0.9)", sm["plv_locked"] > 0.9)
check("ground truth: independent PLV near 0 (< 0.1)", sm["plv_unlocked"] < 0.1)
check("ground truth separates locked from independent (gap > 0.8)",
      sm["plv_locked"] - sm["plv_unlocked"] > 0.8)

# --- reference recovery: the finding ----------------------------------------
check("PLV is a valid value in [0, 1]", 0 <= sm["plv"] <= 1)
check("real O1-Oz alpha PLV is high (> 0.7) -- posterior alpha synchronization", sm["plv"] > 0.7)
check("the phase-difference distribution is concentrated (a clear modal bin)",
      max(int(r["count"]) for r in hist) > 3 * (sum(int(r["count"]) for r in hist) / len(hist)))
check("mean phase lag is small (nearly in phase, |lag| < 0.5 rad)", abs(sm["mean_phase_diff_rad"]) < 0.5)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: scipy agreement is an AGREEMENT, NOT machine precision (filtfilt padding)",
      "agreement, not machine precision" in _note and "filtfilt" in _note)
check("HONEST: anchored on exact formula + ground-truth recovery (phase-robust)",
      "exact formula" in _note and "ground-truth recovery" in _note and "phase" in _note)
check("HONEST: PLV NOT volume-conduction-robust -- PLI/wPLI caveat noted",
      "volume-conduction" in _note and ("pli" in _note or "wpli" in _note))
check("HONEST: descriptive connectivity value, not a clinical claim",
      "descriptive" in _note and "not a clinical claim" in _note)
check("HONEST: cross-tool reference (scipy), not a self-comparison",
      "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
