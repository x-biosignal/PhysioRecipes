import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/wavelet_summary.csv"))}
sp   = list(csv.DictReader(open("artifacts/wavelet_marginal_spectrum.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("dominant_freq traces",        int(sm["dominant_freq_hz"])    == by["dominant_freq"]["value"])
check("alpha_power_fraction traces", abs(sm["alpha_power_fraction"] - by["alpha_power_fraction"]["value"]) < 1e-6)
check("tfr_corr traces",             abs(sm["tfr_corr_vs_mne"]      - by["tfr_corr_vs_mne"]["value"])      < 1e-6)
check("marginal_corr traces",        abs(sm["marginal_corr_vs_mne"] - by["marginal_corr_vs_mne"]["value"]) < 1e-6)
check("n_freqs traces",              int(sm["n_freqs"])             == by["n_freqs"]["value"])

# --- cross-tool validation: waveletTransform == MNE (structure) -------------
check("full-TFR correlation with MNE is very high (>= 0.99)", sm["tfr_corr_vs_mne"] >= 0.99)
check("marginal-spectrum correlation with MNE is very high (>= 0.99)", sm["marginal_corr_vs_mne"] >= 0.99)
check("a normalization scale factor is recorded (0 < scale < 1)", 0 < sm["norm_scale_op_over_mne"] < 1)

# --- reference recovery: the alpha rhythm -----------------------------------
check("the scalogram peaks in the alpha band (dominant 8-13 Hz)", 8 <= sm["dominant_freq_hz"] <= 13)
check("alpha dominates (>= 40% of power in the alpha band)", sm["alpha_power_fraction"] >= 0.4)
check("the marginal spectrum peaks at the dominant frequency",
      max(sp, key=lambda r: float(r["norm_power_op"]))["frequency_hz"] == str(int(sm["dominant_freq_hz"])))
check("the op and (scaled) MNE marginal spectra track each other per frequency",
      all(abs(float(r["mean_power_op"]) - float(r["mean_power_mne_scaled"])) <
          0.5 * max(float(r["mean_power_op"]), 1e-9) for r in sp if float(r["frequency_hz"]) >= 8))

# --- honest scope -----------------------------------------------------------
check("HONEST: independent Morlet impls, structure agreement NOT machine precision",
      "agreement" in case["validation"]["note"].lower() and "not a machine-precision" in case["validation"]["note"].lower())
check("HONEST: normalization convention (~0.49x) noted", "normalization" in case["validation"]["note"].lower())
check("HONEST: cross-tool (MNE), not a self-comparison", "mne" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
