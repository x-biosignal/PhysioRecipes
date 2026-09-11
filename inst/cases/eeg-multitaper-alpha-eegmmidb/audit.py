import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/multitaper_summary.csv"))}
ps   = list(csv.DictReader(open("artifacts/multitaper_psd.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("peak_freq_hz traces",           abs(sm["peak_freq_hz"]           - by["peak_freq_hz"]["value"])           < 1e-6)
check("alpha_power_fraction traces",   abs(sm["alpha_power_fraction"]   - by["alpha_power_fraction"]["value"])   < 1e-6)
check("dpss_max_diff_vs_scipy traces", abs(sm["dpss_max_diff_vs_scipy"] - by["dpss_max_diff_vs_scipy"]["value"]) < 1e-16)
check("psd_max_diff_vs_scipy traces",  abs(sm["psd_max_diff_vs_scipy"]  - by["psd_max_diff_vs_scipy"]["value"])  < 1e-13)
check("psd_corr_vs_mne traces",        abs(sm["psd_corr_vs_mne"]        - by["psd_corr_vs_mne"]["value"])        < 1e-6)
check("n_tapers traces",               int(sm["n_tapers"])              == by["n_tapers"]["value"])

# --- machine-precision legs: DPSS + full PSD vs scipy ------------------------
check("DPSS tapers == scipy.signal.windows.dpss to machine precision (< 1e-10)",
      sm["dpss_max_diff_vs_scipy"] < 1e-10)
check("full PSD == independent scipy+numpy multitaper reconstruction (< 1e-6)",
      sm["psd_max_diff_vs_scipy"] < 1e-6)
check("the PSD table's op and scipy-recon columns match to machine precision",
      max(abs(float(r["psd_op"]) - float(r["psd_scipy_recon"])) for r in ps) < 1e-6)

# --- structure agreement with MNE (external toolbox) ------------------------
check("PSD correlates with MNE psd_array_multitaper > 0.98 (structure)", sm["psd_corr_vs_mne"] > 0.98)
check("MNE / op scale is the one-sided factor-of-2 (1.9 < scale < 2.1)", 1.9 < sm["mne_scale"] < 2.1)

# --- reference recovery: the alpha finding -----------------------------------
check("the multitaper spectrum peaks in the alpha band (8-13 Hz)", 8 <= sm["peak_freq_hz"] <= 13)
check("alpha dominates (>= 30% of the 0-45 Hz power in the alpha band)", sm["alpha_power_fraction"] >= 0.3)
check("n_tapers = 2*NW - 1 for NW=4 (7 tapers)", int(sm["n_tapers"]) == 7 and int(sm["bandwidth_NW"]) == 4)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: TWO machine-precision legs (DPSS vs scipy + PSD vs independent reconstruction)",
      "two machine-precision" in _note and "independent" in _note and "reconstruction" in _note)
check("HONEST: MNE agreement is STRUCTURE (correlation), NOT machine precision",
      "structure" in _note and "not machine precision" in _note)
check("HONEST: MNE differs by a one-sided factor-of-2 normalization convention",
      "one-sided" in _note and "factor-of-2" in _note)
check("HONEST: non-adaptive multitaper (equal-weight taper average)", "non-adaptive" in _note)
check("HONEST: alpha-dominated spectrum is the established rhythm, not a discovery",
      "established" in _note and "not a discovery" in _note)
check("HONEST: cross-tool references (scipy + MNE), not a self-comparison",
      "scipy" in case["validation"]["reference"].lower() and "mne" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
