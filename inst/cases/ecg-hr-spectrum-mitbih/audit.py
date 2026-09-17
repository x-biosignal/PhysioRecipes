import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c

def mlii(path):
    """MLII lead (channel 1) row of a terminal_table.csv."""
    for r in csv.DictReader(open(path)):
        if r["channel"] == "1":
            return {k: (float(v) if k != "channel" else v) for k, v in r.items()}
    raise AssertionError("no channel 1 in " + path)

case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])

# --- primary bundle: record 117 (bradycardia) -------------------------------
h = hashlib.sha256(open("bundle/prereg.json", "rb").read()).hexdigest()
check("prereg_hash traces", h == case["verification"]["prereg_hash"])
vr = {c["id"]: c for c in json.load(open("bundle/verification_report.json"))["claims"]}
for cl in case["claims"]:
    v = vr.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED + value traces",
          v.get("status") == "GROUNDED" and abs(float(v.get("artifact", -9)) - cl["value"]) < 0.02)
check("n_grounded == n_claims == 2",
      len(case["claims"]) == 2 == case["verification"]["n_grounded"])

prim = mlii("bundle/terminal_table.csv")
check("primary mean_hr traces to terminal",
      abs(prim["mean_hr"] - [c["value"] for c in case["claims"] if c["id"] == "mean_hr"][0]) < 0.02)
check("primary mean_rr traces to terminal",
      abs(prim["mean_rr"] - [c["value"] for c in case["claims"] if c["id"] == "mean_rr"][0]) < 0.02)

# --- each record in the spectrum: value traces + HR = 60000/RR ---------------
terminals = {"117": "bundle/terminal_table.csv"}
for rec in ("115", "103", "234"):
    terminals[rec] = f"artifacts/rec{rec}_terminal.csv"
rows = {r["record"]: r for r in case["contrast"]["records"]}
for rec, path in terminals.items():
    t = mlii(path)
    cj = rows[rec]
    check(f"rec {rec}: mean_hr in case.json traces to terminal",
          abs(t["mean_hr"] - cj["mean_hr"]) < 0.02)
    check(f"rec {rec}: mean_rr in case.json traces to terminal",
          abs(t["mean_rr"] - cj["mean_rr"]) < 0.05)
    check(f"rec {rec}: HR = 60000/RR holds (<0.05 bpm)",
          abs(t["mean_hr"] - 60000.0 / t["mean_rr"]) < 0.05)

# --- spectrum table + case-level contrast -----------------------------------
sp = list(csv.DictReader(open("artifacts/ecg_hr_spectrum.csv")))
hrs = [float(r["mean_hr"]) for r in sp]
check("spectrum has 4 records", len(sp) == 4)
check("HR monotonically increasing across the panel order",
      all(hrs[i] < hrs[i + 1] for i in range(len(hrs) - 1)))
check("HR span matches case.json (>= 30 bpm)",
      abs((max(hrs) - min(hrs)) - case["contrast"]["hr_span_bpm"]) < 0.05 and (max(hrs) - min(hrs)) >= 30)
check("every record: reciprocal_ok flag true in spectrum table",
      all(r["reciprocal_ok"].upper() == "TRUE" for r in sp))
check("case-level flags consistent (monotonic + reciprocal_all)",
      case["contrast"]["monotonic_over_panel_order"] is True and
      case["contrast"]["reciprocal_hr_rr_holds_all"] is True)
sdnns = [float(r["sdnn"]) for r in sp]
check("SDNN fold-spread matches case.json",
      abs((max(sdnns) / min(sdnns)) - case["contrast"]["sdnn_fold_spread"]) < 0.1)

# --- every record is a GROUNDED + replayable frozen run ---------------------
sec = json.load(open("artifacts/secondary_runs.json"))
for name, s in sec.items():
    check(f"run {name} (rec {s['record']}): replay byte-identical + 2/2 grounded + adheres",
          s["replay_byte_identical"] is True and s["prereg_adheres"] is True and
          s["n_grounded"] == s["n_claims"] == 2)

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
