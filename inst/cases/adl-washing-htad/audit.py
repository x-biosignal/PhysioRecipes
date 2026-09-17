import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/summary.csv"))}
pcr  = {r["activity"]: r for r in csv.DictReader(open("artifacts/per_class_recall.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("washing_recall traces",   abs(sm["washing_recall"]   - by["washing_recall"]["value"])   < 5e-3)
check("overall_accuracy traces", abs(sm["overall_accuracy"] - by["overall_accuracy"]["value"]) < 5e-3)
check("chance_level traces",     abs(sm["chance_level"]     - by["chance_level"]["value"])     < 5e-3)
check("n_subjects traces",       int(sm["n_subjects"]) == by["n_subjects"]["value"])
check("washing_pcr cross-checks summary",
      abs(float(pcr["washing"]["recall"]) - sm["washing_recall"]) < 1e-3)

# --- the finding: washing recognised above chance ---------------------------
check("washing recall > 2x chance", sm["washing_recall"] > 2 * sm["chance_level"])
check("washing is in the task set", "washing" in pcr)
check("seven tasks scored", len(pcr) == 7 and int(sm["n_activities"]) == 7)

# --- honest scope is machine-visible: N = 3 --------------------------------
check("N = 3 subjects (small-N flagged)", int(sm["n_subjects"]) == 3)
check("note states N=3", "N = 3" in case["validation"]["note"] or "N=3" in case["validation"]["note"])
check("open question flags the small N", any("few" in q["q"] or "subjects" in q["q"] for q in case["open_questions"]))

print("\nRESULT:", "PASS — every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
