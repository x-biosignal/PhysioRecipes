import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/arspec_summary.csv"))}
check("ar_peak_hz traces",                abs(sm["ar_peak_hz"] - by["ar_peak_hz"]["value"]) < 1e-2)
check("max_rel_diff_specar traces",       abs(sm["max_rel_diff_specar"] - by["max_rel_diff_specar"]["value"]) < 1e-16)
check("n_freq traces",                    int(sm["n_freq"]) == by["n_freq"]["value"])
check("peak_in_alpha traces",             int(sm["peak_in_alpha"]) == by["peak_in_alpha"]["value"])
check("periodogram_peak_hz traces",       abs(sm["periodogram_peak_hz"] - by["periodogram_peak_hz"]["value"]) < 1e-2)
check("cross_method_peak_diff_hz traces", abs(sm["cross_method_peak_diff_hz"] - by["cross_method_peak_diff_hz"]["value"]) < 1e-2)
# machine-precision vs spec.ar
check("arSpectrum == stats::spec.ar BIT-FOR-BIT (max |rel diff| < 1e-9)", sm["max_rel_diff_specar"] < 1e-9)
# spectral structure + cross-method agreement
check("AR peak in the alpha band (8-13 Hz)", 8 <= sm["ar_peak_hz"] <= 13 and int(sm["peak_in_alpha"]) == 1)
check("periodogram peak also in alpha band", 8 <= sm["periodogram_peak_hz"] <= 13)
check("parametric and nonparametric peaks agree within 1 Hz", sm["cross_method_peak_diff_hz"] < 1.0)
check("cross-method diff equals |AR peak - periodogram peak|", abs(sm["cross_method_peak_diff_hz"] - abs(sm["ar_peak_hz"] - sm["periodogram_peak_hz"])) < 1e-3)
check("n_freq = 500", int(sm["n_freq"]) == 500)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op building on arYuleWalker (spectral payoff of the AR lane)",
      "newly authored" in _note and "spectral payoff of the ar lane" in _note)
check("HONEST: genuine MACHINE-PRECISION match incl. the spec.ar N/(N-p-1) variance convention",
      "machine-precision" in _note and "n/(n-p-1)" in _note and "not a convention agreement" in _note)
check("HONEST: cross-method agreement (parametric AR vs nonparametric periodogram) is the finding",
      "cross-method agreement" in _note and "nonparametric" in _note)
check("HONEST: a spectral density up to estimator scaling; signal property",
      "spectral density" in _note and "signal property" in _note)
check("HONEST: spec.ar cross-tool reference", "spec.ar" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
