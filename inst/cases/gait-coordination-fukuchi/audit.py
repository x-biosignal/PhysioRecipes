import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
cs   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/coordination_summary.csv"))}
cv   = {r["condition"]: r for r in csv.DictReader(open("artifacts/coordination_variability.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("marp traces",       abs(cs["marp_deg"]   - by["marp"]["value"])       < 0.1)
check("distal traces",     abs(cs["distal"]     - by["distal"]["value"])     < 5e-3)
check("in_phase traces",   abs(cs["in_phase"]   - by["in_phase"]["value"])   < 5e-3)
check("proximal traces",   abs(cs["proximal"]   - by["proximal"]["value"])   < 5e-3)
check("n_cycles traces",   int(cs["n_treadmill_cycles"]) == by["n_cycles"]["value"])

# --- reference recovery: the sagittal hip-knee coordination is knee-led -----
props = {k: cs[k] for k in ("in_phase", "anti_phase", "proximal", "distal")}
check("distal (knee-led) is the modal coordination pattern", cs["distal"] == max(props.values()))
check("the joints are substantially out of phase (MARP 60-100 deg)", 60 <= cs["marp_deg"] <= 100)
check("not simple in-phase lockstep (in-phase < 0.5)", cs["in_phase"] < 0.5)
check("CRP and vector coding agree: high MARP goes with low in-phase",
      (cs["marp_deg"] > 60) and (cs["in_phase"] < 0.4))
check("vector-coding proportions sum to 1", abs(sum(props.values()) - 1) < 1e-2)

# --- honest scope: variability is between-cohort, T ~ O (no difference claimed) ---
dpT = float(cv["treadmill"]["deviation_phase_deg"]); dpO = float(cv["overground"]["deviation_phase_deg"])
check("treadmill and overground deviation phase are similar (no condition claim)",
      abs(dpT - dpO) < 10)
check("open question flags the need for continuous multi-stride data",
      any("stride" in q["q"] for q in case["open_questions"]))
# integrity: the case documents the sagittal-axis correction
check("validation note records the sagittal (Z) axis / correction",
      "sagittal" in case["validation"]["note"].lower())

print("\nRESULT:", "PASS -- every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
