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

check("overall_accuracy traces", abs(sm["overall_accuracy"] - by["overall_accuracy"]["value"]) < 5e-3)
check("walking_recall traces",   abs(float(pcr["walking"]["recall"])          - by["walking_recall"]["value"])  < 5e-3)
check("laying_recall traces",    abs(float(pcr["laying"]["recall"])           - by["laying_recall"]["value"])   < 5e-3)
check("upstairs_recall traces",  abs(float(pcr["walking_upstairs"]["recall"]) - by["upstairs_recall"]["value"]) < 5e-3)
check("n_test_windows traces",   int(sm["n_test_windows"]) == by["n_test_windows"]["value"])

# --- re-derive overall accuracy is consistent with per-class recalls (weighted) ---
tot = sum(int(r["n_test_windows"]) for r in pcr.values())
wacc = sum(float(r["recall"]) * int(r["n_test_windows"]) for r in pcr.values()) / tot
check("weighted per-class recall ~ overall accuracy", abs(wacc - sm["overall_accuracy"]) < 0.02)
check("test window total matches summary", tot == int(sm["n_test_windows"]))
check("six activities scored", len(pcr) == 6 == int(sm["n_activities"]))

# --- findings ---------------------------------------------------------------
check("accuracy well above chance", sm["overall_accuracy"] > 4 * sm["chance_level"])
check("laying is the most separable (recall 1.0)",
      float(pcr["laying"]["recall"]) == max(float(r["recall"]) for r in pcr.values()))
check("upstairs is the weakest class",
      float(pcr["walking_upstairs"]["recall"]) == min(float(r["recall"]) for r in pcr.values()))
check("d450/d455/d415 in the ICF profile", all(c in icf for c in ("d450","d455","d415")))

print("\nRESULT:", "PASS — every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
