import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/summary.csv"))}
pcr  = {r["activity"]: r for r in csv.DictReader(open("artifacts/per_class_recall.csv"))}
icf  = {r["icf_code"]: r for r in csv.DictReader(open("artifacts/icf_profile.csv"))}
chance = sm["chance_level"]

# --- claims trace to artifacts ----------------------------------------------
check("selfcare_detection traces", abs(sm["selfcare_detection_rate"] - by["selfcare_detection"]["value"]) < 5e-3)
check("overall_accuracy traces",   abs(sm["overall_accuracy"]        - by["overall_accuracy"]["value"])   < 5e-3)
check("n_subjects traces",         int(sm["n_subjects"]) == by["n_subjects"]["value"])
check("grooming_recall traces",    abs(float(pcr["grooming"]["recall"]) - by["grooming_recall"]["value"]) < 5e-3)
check("drinking_recall traces",    abs(float(pcr["drinking"]["recall"]) - by["drinking_recall"]["value"]) < 5e-3)
check("eating_recall traces",      abs(float(pcr["eating"]["recall"])   - by["eating_recall"]["value"])   < 5e-3)

# --- headline: self-care separable from locomotion --------------------------
check("self-care detection >= 0.9", sm["selfcare_detection_rate"] >= 0.9)

# --- what reproduces: grooming and drinking well above chance ---------------
check("grooming recall > 2x chance", float(pcr["grooming"]["recall"]) > 2 * chance)
check("drinking recall > 2x chance", float(pcr["drinking"]["recall"]) > 2 * chance)

# --- honest scope: eating is NOT distinguished (claim states 0.00) -----------
check("eating recall is ~0 (not distinguished)", float(pcr["eating"]["recall"]) < 0.05)
check("all self-care tasks are present in the test set (LOSO)",
      all(a in pcr for a in ("grooming", "drinking", "eating")))

# --- the recognised self-care d-codes appear in the ICF profile -------------
check("d520 and d560 in the ICF profile", "d520" in icf and "d560" in icf)
check("d550 (eating) share is small, consistent with recall 0",
      "d550" not in icf or float(icf["d550"]["proportion"]) < 0.1)

print("\nRESULT:", "PASS — every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
