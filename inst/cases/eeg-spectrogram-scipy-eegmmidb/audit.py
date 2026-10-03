import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/spectrogram_summary.csv"))}
check("max_diff_scipy traces",       abs(sm["max_diff_scipy"]       - by["max_diff_scipy"]["value"])       < 1e-15)
check("n_freqs traces",              int(sm["n_freqs"])             == by["n_freqs"]["value"])
check("n_windows traces",            int(sm["n_windows"])           == by["n_windows"]["value"])
check("median_peak_freq_hz traces",  abs(sm["median_peak_freq_hz"]  - by["median_peak_freq_hz"]["value"])  < 1e-4)
check("n_windows_alpha_peak traces", int(sm["n_windows_alpha_peak"])== by["n_windows_alpha_peak"]["value"])
check("alpha_power_cv_pct traces",   abs(sm["alpha_power_cv_pct"]   - by["alpha_power_cv_pct"]["value"])   < 1e-3)
check("mean_alpha_power traces",     abs(sm["mean_alpha_power"]     - by["mean_alpha_power"]["value"])     < 1e-2)
# machine-precision
check("op == scipy.signal.spectrogram BIT-FOR-BIT over 129x11 cells (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("full freq x time matrix (129 x 11)", int(sm["n_freqs"])==129 and int(sm["n_windows"])==11)
# finding
check("finding: alpha dominates EVERY window (sustained rhythm)", int(sm["n_windows_alpha_peak"])==int(sm["n_windows"]))
check("finding: median peak frequency is in the alpha band (8-13 Hz)", 8 <= sm["median_peak_freq_hz"] <= 13)
check("finding: alpha power waxes/wanes across time (CV > 20%, hidden by averaged PSD)", sm["alpha_power_cv_pct"] > 20)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: FIRST external-reference (scipy) certification; spectrogram is NOT a new op",
      "first external-reference" in _note and "not new" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical STFT), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: the match REQUIRES the matched conventions (scipy defaults differ)",
      "requires" in _note and "scipy's defaults" in _note)
check("HONEST: time-frequency reveals what the averaged Welch PSD hides",
      "waxing" in _note and "averaged" in _note)
check("HONEST: scipy cross-tool reference, not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
