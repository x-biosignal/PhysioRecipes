import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
coh  = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/fatigue_cohort.csv"))}
ps   = list(csv.DictReader(open("artifacts/fatigue_per_subject.csv")))
rep  = {r["metric"]: r["value"] for r in csv.DictReader(open("artifacts/fatigue_representative.csv"))}

# --- claims trace to the cohort artifact -------------------------------------
check("n_fatigued traces",         int(coh["n_subjects_fatigued"]) == by["n_fatigued"]["value"])
check("mean_fatigue_index traces", abs(coh["mean_fatigue_index"] - by["mean_fatigue_index"]["value"]) < 1e-4)
check("mean_pct_change traces",    abs(coh["mean_pct_change"]     - by["mean_pct_change"]["value"])   < 1e-2)
check("mean_initial_mdf traces",   abs(coh["mean_initial_mdf_hz"] - by["mean_initial_mdf"]["value"])  < 1e-2)
check("mean_final_mdf traces",     abs(coh["mean_final_mdf_hz"]   - by["mean_final_mdf"]["value"])     < 1e-2)

# --- re-derive the cohort numbers from the per-subject rows ------------------
idx  = [float(r["fatigue_index"]) for r in ps]
ini  = [float(r["initial_mdf"])   for r in ps]
fin  = [float(r["final_mdf"])     for r in ps]
n_fat = sum(1 for v in idx if v < 1)
check("per-subject count reproduces n_fatigued", n_fat == int(coh["n_subjects_fatigued"]))
check("15 subjects present", len(ps) == 15 and int(coh["n_subjects"]) == 15)
check("mean fatigue index reproduces", abs(sum(idx)/len(idx) - coh["mean_fatigue_index"]) < 5e-4)
check("mean initial MDF reproduces",   abs(sum(ini)/len(ini) - coh["mean_initial_mdf_hz"]) < 5e-2)
check("mean final MDF reproduces",     abs(sum(fin)/len(fin) - coh["mean_final_mdf_hz"])   < 5e-2)

# --- internal consistency: pct_change is exactly 100*(fatigue_index - 1) -----
# (fatigue_index is the mean of per-channel final/initial ratios; the reported
#  percent change is defined from it, so this is a strict identity per subject)
consistent = all(abs(float(r["pct_change"]) - 100 * (float(r["fatigue_index"]) - 1)) < 1e-3 for r in ps)
check("pct_change == 100*(fatigue_index - 1) per subject", consistent)

# --- honest scoping: exactly one subject does NOT fatigue, and it is named ---
not_fat = [r["subject"] for r in ps if float(r["fatigue_index"]) >= 1]
check("exactly one non-fatiguing subject", len(not_fat) == 1)
check("open question names the non-fatiguing subject",
      len(not_fat) == 1 and not_fat[0] in case["open_questions"][0]["q"])

# --- representative subject is the one closest to the cohort mean % change ---
pooled = sum(float(r["pct_change"]) for r in ps) / len(ps)
closest = min(ps, key=lambda r: abs(float(r["pct_change"]) - pooled))["subject"]
check("representative subject is closest to cohort mean", closest == rep["representative_subject"])

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
