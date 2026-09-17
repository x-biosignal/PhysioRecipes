import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c
case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])
h = hashlib.sha256(open("bundle/prereg.json","rb").read()).hexdigest()
check("prereg_hash traces", h == case["verification"]["prereg_hash"])
vr = {c["id"]: c for c in json.load(open("bundle/verification_report.json"))["claims"]}
for cl in case["claims"]:
    v = vr.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED+value traces",
          v.get("status")=="GROUNDED" and abs(float(v.get("artifact",-9))-cl["value"])<0.001)
check("n_grounded==n_claims==5", len(case["claims"])==5==case["verification"]["n_grounded"])
# alpha is dominant among the 5 claims
vals = {cl["id"]: cl["value"] for cl in case["claims"]}
check("alpha dominates all other bands (O1)", all(vals["alpha"]>vals[b] for b in ("delta","theta","beta","gamma")))
# Oz replication alpha traces + dominant
oz = {r["channel"]: r for r in csv.DictReader(open("artifacts/oz_replication_terminal.csv"))}
ozrow = list(oz.values())[0]
check("Oz alpha traces", abs(float(ozrow["alpha"]) - case["replication"]["alpha"]) < 0.001)
check("Oz alpha dominant", all(float(ozrow["alpha"])>float(ozrow[b]) for b in ("delta","theta","beta","gamma")))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
