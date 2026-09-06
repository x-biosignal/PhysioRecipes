import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/fda_summary.csv"))}
cc   = list(csv.DictReader(open("artifacts/coefficient_curve.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("beta_peak_pct traces",   int(s["beta_peak_pct_cycle"])     == by["beta_peak_pct"]["value"])
check("beta_peak_value traces", abs(s["beta_peak_value"]          - by["beta_peak_value"]["value"]) < 5e-3)
check("global_p traces",        abs(s["speed_global_p"]           - by["global_p"]["value"])        < 1e-4)
check("cor_speed_peak traces",  abs(s["cor_speed_peakflexion"]    - by["cor_speed_peak"]["value"])  < 5e-3)
check("n_curves traces",        int(s["n_curves"])                == by["n_curves"]["value"])

# --- reference recovery: the established speed-dependence of the knee waveform
check("speed effect is significant (global p < 0.05)", s["speed_global_p"] < 0.05)
check("peak speed coefficient is positive (faster -> more flexion)", s["beta_peak_value"] > 0)
check("coefficient peaks in swing phase (55-75% cycle)", 55 <= s["beta_peak_pct_cycle"] <= 75)
check("peak knee flexion rises with speed (r > 0.4)", s["cor_speed_peakflexion"] > 0.4)
# the coefficient curve is also positive at loading-response flexion (~10-20%)
lr = [float(r["beta_speed"]) for r in cc if 10 <= int(r["pct_cycle"]) <= 20]
check("loading-response segment (10-20%) is positive", sum(lr) / len(lr) > 0)
# curve is genuinely a curve (varies), not flat
betas = [float(r["beta_speed"]) for r in cc]
check("coefficient curve varies across the cycle", (max(betas) - min(betas)) > 1.0)

# --- honest scope: ordinal speed level, not m/s -----------------------------
check("open question flags the m/s vs ordinal-speed limitation",
      any("m/s" in q["q"] for q in case["open_questions"]))

print("\nRESULT:", "PASS -- speed-dependence recovered; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
