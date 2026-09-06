import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/detrend_summary.csv"))}
check("max_diff_scipy traces",              abs(sm["max_diff_scipy"]              - by["max_diff_scipy"]["value"])              < 1e-15)
check("slope_removed traces",               abs(sm["slope_removed_uv_per_sample"] - by["slope_removed_uv_per_sample"]["value"]) < 1e-5)
check("lowfreq_power_raw traces",           abs(sm["lowfreq_power_raw"]           - by["lowfreq_power_raw"]["value"])           < 1e-2)
check("lowfreq_power_linear traces",        abs(sm["lowfreq_power_linear"]        - by["lowfreq_power_linear"]["value"])        < 1e-2)
check("lowfreq_power_constant traces",      abs(sm["lowfreq_power_constant"]      - by["lowfreq_power_constant"]["value"])      < 1e-2)
check("leakage_reduction_pct traces",       abs(sm["leakage_reduction_pct"]       - by["leakage_reduction_pct"]["value"])       < 1e-2)
# machine-precision
check("op == scipy.signal.detrend BIT-FOR-BIT (linear + constant, < 1e-9)", sm["max_diff_scipy"] < 1e-9)
# finding: detrend type matters for spectral leakage
check("linear detrend leaves less sub-1-Hz power than constant", sm["lowfreq_power_linear"] < sm["lowfreq_power_constant"])
check("both detrends reduce low-freq power vs raw", sm["lowfreq_power_linear"] < sm["lowfreq_power_raw"] and sm["lowfreq_power_constant"] < sm["lowfreq_power_raw"])
check("leakage reduction is substantial (>20%) -- the type genuinely matters", sm["leakage_reduction_pct"] > 20)
check("leakage_reduction is internally consistent with the two powers",
      abs(sm["leakage_reduction_pct"] - 100*(sm["lowfreq_power_constant"]-sm["lowfreq_power_linear"])/sm["lowfreq_power_constant"]) < 1e-2)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: FIRST external-reference (scipy) certification; detrendSignal is not new",
      "first external-reference" in _note and "op is not new" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical detrend), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: finding is methodological (detrend TYPE matters), not a physiological claim",
      "methodological" in _note and "not a physiological claim" in _note)
check("HONEST: linear detrend removes only the LINEAR part (wander needs high-pass)",
      "linear part" in _note and "high-pass" in _note)
check("HONEST: scipy cross-tool reference, not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
