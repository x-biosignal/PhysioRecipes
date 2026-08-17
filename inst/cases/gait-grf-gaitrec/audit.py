import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok=True
def check(l,c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
case=json.load(open("case.json"))
kv={r["item"]:r["value"] for r in csv.DictReader(open("artifacts/gaitrec_grf_realdata_validation.csv"))}
for cl in case["claims"]:
    check(f"{cl['id']} traces", abs(float(kv[cl['id']])-cl["value"])<1e-3)
# directional clinical pattern holds (patient loading peak < control; trough > control)
by={cl["id"]:cl["value"] for cl in case["claims"]}
check("patient loading peak < control", by["patient_peak1_bw"]<by["control_peak1_bw"])
check("patient mid-stance trough > control", by["patient_trough_bw"]>by["control_trough_bw"])
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
