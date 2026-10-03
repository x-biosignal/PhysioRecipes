import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c

def row(path):
    r = list(csv.DictReader(open(path)))[0]
    return {k: (float(v) if k != "channel" else v) for k, v in r.items()}

OTHERS = ("delta", "theta", "beta", "gamma")
case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])

# --- primary bundle: eyes-closed O1 -----------------------------------------
h = hashlib.sha256(open("bundle/prereg.json", "rb").read()).hexdigest()
check("prereg_hash traces", h == case["verification"]["prereg_hash"])
vr = {c["id"]: c for c in json.load(open("bundle/verification_report.json"))["claims"]}
for cl in case["claims"]:
    v = vr.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED + value traces",
          v.get("status") == "GROUNDED" and abs(float(v.get("artifact", -9)) - cl["value"]) < 0.001)
check("n_grounded == n_claims == 5",
      len(case["claims"]) == 5 == case["verification"]["n_grounded"])

closed_O1 = row("bundle/terminal_table.csv")
check("eyes-closed O1 alpha dominant (bundle)",
      all(closed_O1["alpha"] > closed_O1[b] for b in OTHERS))

# --- the three contrast runs (artifacts) ------------------------------------
closed_Oz = row("artifacts/eyesclosed_Oz_terminal.csv")
open_O1   = row("artifacts/eyesopen_O1_terminal.csv")
open_Oz   = row("artifacts/eyesopen_Oz_terminal.csv")
arms = {
    "O1": {"closed": closed_O1, "open": open_O1,
           "case": case["contrast"]["electrodes"]["O1"]},
    "Oz": {"closed": closed_Oz, "open": open_Oz,
           "case": case["contrast"]["electrodes"]["Oz"]},
}
for e, a in arms.items():
    cclosed, copen, cj = a["closed"], a["open"], a["case"]
    check(f"{e}: eyes-closed alpha traces to terminal",
          abs(cclosed["alpha"] - cj["eyes_closed"]) < 5e-4)
    check(f"{e}: eyes-open alpha traces to terminal",
          abs(copen["alpha"] - cj["eyes_open"]) < 5e-4)
    check(f"{e}: BERGER blocking (eyes-closed alpha > eyes-open alpha)",
          cclosed["alpha"] > copen["alpha"])
    check(f"{e}: alpha dominant eyes-closed",
          all(cclosed["alpha"] > cclosed[b] for b in OTHERS))
    check(f"{e}: alpha NOT dominant eyes-open (alpha blocked)",
          any(copen[b] >= copen["alpha"] for b in OTHERS))
    check(f"{e}: alpha_drop traces",
          abs((cclosed["alpha"] - copen["alpha"]) - cj["alpha_drop"]) < 5e-4)

# --- contrast summary table + case-level decision ---------------------------
ct = {r["electrode"]: r for r in csv.DictReader(open("artifacts/berger_contrast.csv"))}
for e_key, arm in (("O1..", "O1"), ("Oz..", "Oz")):
    r = ct[e_key]
    check(f"contrast table {e_key}: blocking flag true and matches terminals",
          r["blocking_at_this_e"].upper() == "TRUE" and
          float(r["alpha_eyes_closed"]) > float(r["alpha_eyes_open"]))
check("case-level berger_met == blocking at BOTH electrodes",
      case["contrast"]["berger_met"] is True and
      all(ct[k]["blocking_at_this_e"].upper() == "TRUE" for k in ("O1..", "Oz..")))

# --- every eyes-open run is a GROUNDED + replayable frozen run ---------------
sec = json.load(open("artifacts/secondary_runs.json"))
for name, s in sec.items():
    check(f"secondary run {name}: replay byte-identical + 5/5 grounded + adheres",
          s["replay_byte_identical"] is True and s["prereg_adheres"] is True and
          s["n_grounded"] == s["n_claims"] == 5)

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
