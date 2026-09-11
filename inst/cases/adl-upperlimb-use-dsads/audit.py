import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
ov   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/overall_use.csv"))}
pa   = list(csv.DictReader(open("artifacts/per_activity_use.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("use_ratio traces",       abs(ov["use_ratio"]                  - by["use_ratio"]["value"])       < 5e-3)
check("magnitude_ratio traces", abs(ov["magnitude_ratio"]            - by["magnitude_ratio"]["value"]) < 5e-3)
check("n_dynamic traces",       int(ov["n_dynamic_activities"])      == by["n_dynamic"]["value"])
check("max_abs_mag traces",     abs(ov["max_abs_mag_ratio_dynamic"]  - by["max_abs_mag"]["value"])     < 5e-3)
check("mean_abs_mag traces",    abs(ov["mean_abs_mag_ratio_dynamic"] - by["mean_abs_mag"]["value"])    < 5e-3)

# --- reference recovery: healthy bilateral SYMMETRY -------------------------
check("overall arm use is symmetric (|magnitude ratio| < 0.2)", abs(ov["magnitude_ratio"]) < 0.2)
check("every dynamic activity is symmetric (max |mag ratio| < 0.5)", ov["max_abs_mag_ratio_dynamic"] < 0.5)
check("mean dynamic asymmetry is small (< 0.2)", ov["mean_abs_mag_ratio_dynamic"] < 0.2)
# per-activity table: dynamic activities have use ratio 1 and are symmetric
dyn = [r for r in pa if abs(float(r["use_ratio"]) - 1.0) < 1e-6]
check("14 activities have both arms in use (use ratio == 1)", len(dyn) == 14)
check("all dynamic activities are symmetric in the table",
      all(abs(float(r["magnitude_ratio"])) < 0.5 for r in dyn))

# --- honest scope: clinical asymmetry needs DUA-gated bilateral-wrist data ---
check("open question flags the clinical bilateral-wrist gap",
      any("wrist" in q["q"].lower() for q in case["open_questions"]))

print("\nRESULT:", "PASS — symmetric reference recovered; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
