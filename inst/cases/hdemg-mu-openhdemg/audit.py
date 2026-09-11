import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok=True
def check(l,c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
case=json.load(open("case.json"))
roa={int(r["ref_mu"]):float(r["roa_lag_aware"]) for r in csv.DictReader(open("artifacts/hdemg_roa.csv"))}
m={"mu1_roa":1,"mu2_roa":2,"mu4_roa":4,"mu5_roa":5}
for cl in case["claims"]:
    check(f"{cl['id']} traces", abs(roa[m[cl['id']]]-cl["value"])<1e-3)
    check(f"{cl['id']} recovered (RoA>=0.75)", cl["value"]>=0.75)
check("MU3 genuinely not recovered in source (RoA<0.1)", roa[3]<0.1)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
