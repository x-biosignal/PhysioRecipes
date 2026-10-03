import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/id_summary.csv"))}
agr  = list(csv.DictReader(open("artifacts/id_agreement.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("ankle_r traces",       abs(sm["ankle_r_mean"]     - by["ankle_r"]["value"])       < 5e-3)
check("knee_r traces",        abs(sm["knee_r_mean"]      - by["knee_r"]["value"])        < 5e-3)
check("hip_r traces",         abs(sm["hip_r_mean"]       - by["hip_r"]["value"])         < 5e-3)
check("ankle_ref_peak traces",abs(sm["ankle_ref_peak_mean"] - by["ankle_ref_peak"]["value"]) < 5e-3)
check("n_subjects traces",    int(sm["n_subjects"]) == by["n_subjects"]["value"])

# --- the summary means re-derive from the per-subject agreement table --------
def mean_of(joint, col):
    v = [float(r[col]) for r in agr if r["joint"] == joint]
    return sum(v) / len(v)
check("id_agreement has 15 rows (5 subjects x 3 joints)", len(agr) == 15)
check("ankle_r_mean == mean of per-subject ankle r", abs(mean_of("ankle","r") - sm["ankle_r_mean"]) < 1e-3)
check("hip_r_mean == mean of per-subject hip r",     abs(mean_of("hip","r")   - sm["hip_r_mean"])   < 1e-3)

# --- reference recovery: the physics + the known accuracy structure ----------
check("ankle sagittal moment is recovered excellently (r > 0.95)", sm["ankle_r_mean"] > 0.95)
check("DISTAL-TO-PROXIMAL accuracy gradient: ankle > knee > hip",
      sm["ankle_r_mean"] > sm["knee_r_mean"] > sm["hip_r_mean"])
check("recovered ankle push-off peak is physiological (1.4-1.9 N*m/kg)",
      1.4 <= sm["ankle_ref_peak_mean"] <= 1.9)
check("every subject's ankle moment agrees strongly (all r > 0.90)",
      all(float(r["r"]) > 0.90 for r in agr if r["joint"] == "ankle"))

# --- honest scope: the hip degrades + its peak inflates (reported, not hidden) ---
check("HONEST: hip is the least-accurate joint (lowest r)",
      sm["hip_r_mean"] == min(sm["ankle_r_mean"], sm["knee_r_mean"], sm["hip_r_mean"]))
check("HONEST: the hip moment peak INFLATES vs the reference (GTR proxy)",
      sm["hip_id_peak_mean"] > sm["hip_ref_peak_mean"])
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
