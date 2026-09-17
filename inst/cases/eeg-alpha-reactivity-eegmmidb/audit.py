import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c

def o1(path):
    for r in csv.DictReader(open(path)):
        if r["channel"] == "O1..":
            return {k: (float(v) if k != "channel" else v) for k, v in r.items()}
    raise AssertionError("no O1.. row in " + path)

OTHERS = ("delta", "theta", "beta", "gamma")
case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])

# --- primary bundle: S001 eyes-closed O1 ------------------------------------
h = hashlib.sha256(open("bundle/prereg.json", "rb").read()).hexdigest()
check("prereg_hash traces", h == case["verification"]["prereg_hash"])
vr = {c["id"]: c for c in json.load(open("bundle/verification_report.json"))["claims"]}
for cl in case["claims"]:
    v = vr.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED + value traces",
          v.get("status") == "GROUNDED" and abs(float(v.get("artifact", -9)) - cl["value"]) < 0.001)
check("n_grounded == n_claims == 5", len(case["claims"]) == 5 == case["verification"]["n_grounded"])
prim = o1("bundle/terminal_table.csv")
check("primary (S001 closed) alpha dominant", all(prim["alpha"] > prim[b] for b in OTHERS))

# --- per-subject reactivity re-derived from terminals -----------------------
react = case["reactivity"]
n_react = 0; n_dom = 0; drops = []
for s in react["subjects"]:
    subj = s["subject"]
    tclosed = "bundle/terminal_table.csv" if subj == "S001" else f"artifacts/closed_{subj}_terminal.csv"
    topen = f"artifacts/open_{subj}_terminal.csv"
    c_closed, c_open = o1(tclosed), o1(topen)
    check(f"{subj}: eyes-closed alpha traces to terminal",
          abs(c_closed["alpha"] - s["alpha_eyes_closed"]) < 5e-4)
    check(f"{subj}: eyes-open alpha traces to terminal",
          abs(c_open["alpha"] - s["alpha_eyes_open"]) < 5e-4)
    reactive = c_closed["alpha"] > c_open["alpha"]
    check(f"{subj}: reactive flag matches terminals (closed > open = {reactive})",
          reactive == bool(s["reactive"]))
    dom = all(c_closed["alpha"] > c_closed[b] for b in OTHERS)
    check(f"{subj}: dominant_closed flag matches terminals",
          dom == bool(s["dominant_closed"]))
    check(f"{subj}: alpha_drop traces",
          abs((c_closed["alpha"] - c_open["alpha"]) - s["alpha_drop"]) < 5e-4)
    n_react += int(reactive); n_dom += int(dom); drops.append(c_closed["alpha"] - c_open["alpha"])

# --- case-level aggregates --------------------------------------------------
check("n_reactive re-derived == case.json", n_react == react["n_reactive"])
check("n_dominant_closed re-derived == case.json", n_dom == react["n_dominant_closed"])
check("all_reactive flag consistent (10/10 here)",
      (n_react == react["n_subjects"]) == bool(react["all_reactive"]))
check("mean_alpha_drop traces (<1e-3)", abs(sum(drops) / len(drops) - react["mean_alpha_drop"]) < 1e-3)

# --- reactivity panel table matches -----------------------------------------
panel = {r["subject"]: r for r in csv.DictReader(open("artifacts/reactivity_panel.csv"))}
check("panel has all 10 subjects", len(panel) == react["n_subjects"] == 10)
check("every panel row: reactive flag true (closed > open)",
      all(r["reactive"].upper() == "TRUE" for r in panel.values()))

# --- every run is a GROUNDED + replayable frozen run ------------------------
sec = json.load(open("artifacts/secondary_runs.json"))
check("secondary_runs has all 20 runs", len(sec) == 20)
for name, s in sec.items():
    check(f"run {name}: replay byte-identical + 5/5 grounded + adheres",
          s["replay_byte_identical"] is True and s["prereg_adheres"] is True and
          s["n_grounded"] == s["n_claims"] == 5)

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
