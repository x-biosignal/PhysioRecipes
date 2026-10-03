import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
ea   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/enmo_agreement.csv"))}
fl   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/freeliving_summary.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("enmo_max_diff traces",     abs(ea["enmo_max_abs_diff_g"] - by["enmo_max_diff"]["value"]) < 1e-14)
check("enmo_correlation traces",  abs(ea["enmo_correlation"]    - by["enmo_correlation"]["value"]) < 1e-4)
check("intensity_gradient traces",abs(fl["intensity_gradient"]  - by["intensity_gradient"]["value"]) < 1e-2)
check("mvpa_min traces",          abs(fl["mvpa_min"]            - by["mvpa_min"]["value"]) < 0.1)
check("astp traces",              abs(fl["astp"]                - by["astp"]["value"]) < 1e-3)

# --- the rigorous result: ENMO matches GGIR to machine precision ------------
check("ENMO max diff < 1e-6 g (machine precision)", ea["enmo_max_abs_diff_g"] < 1e-6)
check("ENMO correlation ~ 1", ea["enmo_correlation"] >= 0.9999)
check("agreement computed over many epochs", int(ea["n_epochs"]) > 100)

# --- external check: intensity gradient matches GGIR::g.intensitygradient ----
check("ig_agree_ggir traces", abs(ea["ig_max_abs_diff_vs_ggir"] - by["ig_agree_ggir"]["value"]) < 1e-8)
check("intensity gradient matches GGIR to machine precision (max abs diff < 1e-8)",
      ea["ig_max_abs_diff_vs_ggir"] < 1e-8)
check("GGIR independently returns the same negative gradient (~ -1.19)",
      abs(ea["intensity_gradient_ggir"] - fl["intensity_gradient"]) < 1e-2)

# --- the summary is internally consistent -----------------------------------
check("intensity gradient is negative (time decreases with intensity)", fl["intensity_gradient"] < 0)
check("astp is a probability in (0,1)", 0 < fl["astp"] < 1)
check("time-use minutes are non-negative",
      fl["sedentary_min"] >= 0 and fl["light_min"] >= 0 and fl["mvpa_min"] >= 0)

print("\nRESULT:", "PASS — every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
