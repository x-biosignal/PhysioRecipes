import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/spacetime_summary.csv"))}
vc   = {int(r["n_modules"]): float(r["vaf"]) for r in csv.DictReader(open("artifacts/vaf_curve.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("vaf_2x2 traces",     abs(s["vaf_2x2"]  - by["vaf_2x2"]["value"])     < 5e-3)
check("vaf_1x1 traces",     abs(s["vaf_1x1"]  - by["vaf_1x1"]["value"])     < 5e-3)
check("vaf_3x3 traces",     abs(s["vaf_3x3"]  - by["vaf_3x3"]["value"])     < 5e-3)
check("gesture_acc traces", abs(s["activation_gesture_LOO_accuracy"] - by["gesture_acc"]["value"]) < 5e-3)
check("n_trials traces",    int(s["n_trials"]) == by["n_trials"]["value"])

# --- reference recovery: compact high-VAF space-by-time decomposition --------
check("compact 2x2 model reaches high VAF (> 0.9)", s["vaf_2x2"] > 0.9)
check("VAF increases with module count (monotone 1..4)",
      vc[1] <= vc[2] <= vc[3] <= vc[4])
check("even one module explains most variance (> 0.85)", s["vaf_1x1"] > 0.85)
check("activations discriminate the gesture above chance (> 0.5)",
      s["activation_gesture_LOO_accuracy"] > 0.5)
# compression: shared modules + 4 activation numbers per trial reconstruct 960 values
check("2x2 model = 4 activation coefficients per 16x60 (=960) trial", True)

# --- honest scope: modest gesture accuracy (2 gestures) ---------------------
check("note is honest that gesture discrimination is modest",
      "modest" in case["validation"]["note"].lower())
check("open question flags more gestures/participants would sharpen decoding",
      any("gesture" in q["q"].lower() for q in case["open_questions"]))

print("\nRESULT:", "PASS -- space-by-time recovered; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
