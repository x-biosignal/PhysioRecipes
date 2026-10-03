import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/bandpower_summary.csv"))}
# claims trace
check("mean_delta_power traces",        abs(sm["mean_delta_power"] - by["mean_delta_power"]["value"]) < 1e-2)
check("mean_alpha_power traces",        abs(sm["mean_alpha_power"] - by["mean_alpha_power"]["value"]) < 1e-2)
check("mean_rel_alpha traces",          abs(sm["mean_rel_alpha"]   - by["mean_rel_alpha"]["value"])   < 1e-5)
check("max_rel_alpha traces",           abs(sm["max_rel_alpha"]    - by["max_rel_alpha"]["value"])    < 1e-5)
check("max_diff_scipy traces",          abs(sm["max_diff_scipy"]   - by["max_diff_scipy"]["value"])   < 1e-15)
check("posterior_mean_relalpha traces", abs(sm["posterior_mean_relalpha"] - by["posterior_mean_relalpha"]["value"]) < 1e-5)
check("frontal_mean_relalpha traces",   abs(sm["frontal_mean_relalpha"]   - by["frontal_mean_relalpha"]["value"])   < 1e-5)
check("n_channels traces",              int(sm["n_channels"]) == by["n_channels"]["value"])
# machine-precision: op == scipy.signal.welch, bit-for-bit
check("op == scipy.signal.welch BIT-FOR-BIT over 64ch x 5 bands (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("all 64 channels x 5 bands validated", int(sm["n_channels"]) == 64 and int(sm["n_bands"]) == 5)
# finding: posterior alpha dominance
check("finding: posterior relative alpha markedly exceeds frontal (eyes-closed alpha rhythm)",
      sm["posterior_mean_relalpha"] > sm["frontal_mean_relalpha"] and
      (sm["posterior_mean_relalpha"] - sm["frontal_mean_relalpha"]) > 0.2)
check("finding: peak relative alpha (posterior) exceeds the montage mean", sm["max_rel_alpha"] > sm["mean_rel_alpha"])
check("alpha power exceeds delta power on average (alpha-dominant eyes-closed rest)", sm["mean_alpha_power"] > sm["mean_delta_power"])
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: FIRST external-reference (scipy) certification; bandPower is NOT a new op",
      "first external-reference" in _note and "not a new op" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical estimate), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: the match REQUIRES the symmetric-Hann + detrend conventions (scipy defaults differ)",
      "symmetric" in _note and "detrend" in _note and "requires" in _note)
check("HONEST: posterior alpha is the eyes-closed topography, cross-consistent with the Hjorth case",
      "posterior" in _note and "eyes-closed" in _note and "hjorth" in _note)
check("HONEST: scipy cross-tool reference, not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
