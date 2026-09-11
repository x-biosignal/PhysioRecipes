import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(label, cond):
    global ok; print(f"  [{'PASS' if cond else 'FAIL'}] {label}"); ok = ok and cond

case = json.load(open("case.json"))
print("case.json valid; id =", case["id"], "| status =", case["status"])

h = hashlib.sha256(open("bundle/prereg.json","rb").read()).hexdigest()
check("prereg_hash == sha256(bundle/prereg.json)", h == case["verification"]["prereg_hash"])

vr = json.load(open("bundle/verification_report.json")); vrb = {c["id"]:c for c in vr["claims"]}
for cl in case["claims"]:
    v = vrb.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED + value traces",
          v.get("status")=="GROUNDED" and abs(float(v.get("artifact",0))-cl["value"])<0.02)
check("n_grounded == n_claims", vr["n_grounded"]==vr["n_claims"]==case["verification"]["n_grounded"])

# cross_tool -> real mitbih_hrv.csv (metric,value,standard_def,rhrv)
hrv = {r["metric"]: r for r in csv.DictReader(open("artifacts/mitbih_hrv.csv"))}
for c in case["cross_tool"]["summary"]:
    r = hrv.get(c["metric"], {})
    phys_ok = abs(float(r.get("value",-9)) - c["physioecg"]) < 1e-3
    ref_ok  = abs(float(r.get("rhrv",-9))  - c["reference"]) < 1e-3
    std_ok  = abs(float(r.get("value",-9)) - float(r.get("standard_def",-99))) < 1e-6  # exact std-def repro
    check(f"cross-tool {c['metric']}: PhysioECG & RHRV & exact-std-def all trace", phys_ok and ref_ok and std_ok)

det = {r["record"]: r for r in csv.DictReader(open("artifacts/mitbih_realdata_validation.csv"))}
for d in case["detection"]["records"]:
    r = det.get(d["record"], {})
    check(f"detection {d['record']} f1 traces", abs(float(r.get("f1",-9))-d["f1"])<1e-3)

# open-question pNN50 synthetic-series values present (labelled synthetic)
pnn = [float(r["pnn50_pct"]) for r in csv.DictReader(open("artifacts/pnn50_diagnosis.csv"))]
for val in (0.0, 22.22, 50.51):
    check(f"pNN50 {val}% present (synthetic diagnosis)", any(abs(p-val)<0.05 for p in pnn))
check("open question not escalated (resolved)", case["open_questions"][0]["escalate"] is None)

print("\nRESULT:", "ALL TRACE — case self-audits clean" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
