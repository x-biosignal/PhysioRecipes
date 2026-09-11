import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/coherence_summary.csv"))}
sp   = list(csv.DictReader(open("artifacts/coherence_spectrum.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("max_abs_diff traces",        abs(sm["max_abs_diff_vs_scipy"] - by["max_abs_diff"]["value"])        < 1e-18)
check("peak_coherence traces",      abs(sm["peak_coherence"]        - by["peak_coherence"]["value"])      < 1e-6)
check("peak_freq_hz traces",        abs(sm["peak_freq_hz"]          - by["peak_freq_hz"]["value"])        < 1e-4)
check("band_mean_coherence traces", abs(sm["band_mean_coherence"]   - by["band_mean_coherence"]["value"]) < 1e-6)
check("n_freq traces",              int(sm["n_freq"])               == by["n_freq"]["value"])

# --- external cross-tool validation: coherence == scipy (machine precision) --
check("op == scipy.signal.coherence to machine precision (< 1e-9)", sm["max_abs_diff_vs_scipy"] < 1e-9)
check("the agreement is at machine precision (< 1e-12)", sm["max_abs_diff_vs_scipy"] < 1e-12)
check("the spectrum artifact confirms op == scipy per-frequency (< 1e-9)",
      all(abs(float(r["coherence"]) - float(r["scipy_coherence"])) < 1e-9 for r in sp))

# --- reference recovery: a real cardiac coherence peak ----------------------
check("PPG-ECG coherence peaks strongly in the cardiac band (peak > 0.8)", sm["peak_coherence"] > 0.8)
check("the peak frequency is a plausible heart rate (0.8-3 Hz = 48-180 bpm)", 0.8 < sm["peak_freq_hz"] < 3.0)
check("the peak is far above the 95% confidence limit", sm["peak_coherence"] > 10 * sm["confidence_limit"])
check("a valid coherence spectrum (values in [0,1])",
      all(0 <= float(r["coherence"]) <= 1 for r in sp))

# --- honest scope -----------------------------------------------------------
check("HONEST: no detrend -> DC component, finding read in the cardiac band",
      "detrend" in case["validation"]["note"].lower() and "cardiac band" in case["validation"]["note"].lower())
check("HONEST: machine-precision match REQUIRES matched Welch settings",
      "matched" in case["validation"]["note"].lower() or "matching the welch" in case["validation"]["note"].lower())
check("HONEST: cross-tool (scipy), not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
