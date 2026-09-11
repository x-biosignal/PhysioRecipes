import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok=True
def check(l,c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
case=json.load(open("case.json"))
rows={r["method"]:r for r in csv.DictReader(open("artifacts/eda_realdata_methodmatched.csv"))}
hp=rows["highpass"]; by={cl["id"]:cl for cl in case["claims"]}
check("phasic_r traces (highpass)", abs(float(hp["phasic_r"])-by["phasic_r"]["value"])<1e-3)
check("tonic_r traces (highpass)",  abs(float(hp["tonic_r"])-by["tonic_r"]["value"])<1e-3)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated (embargo)", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
