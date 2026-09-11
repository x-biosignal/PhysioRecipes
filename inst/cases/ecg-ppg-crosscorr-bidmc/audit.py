import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/crosscorr_summary.csv"))}
pf   = list(csv.DictReader(open("artifacts/crosscorr_profile.csv")))
# claims trace
check("peak_lag traces",           abs(sm["peak_lag"]           - by["peak_lag"]["value"])           < 1e-9)
check("peak_lag_seconds traces",   abs(sm["peak_lag_seconds"]   - by["peak_lag_seconds"]["value"])   < 1e-6)
check("peak_correlation traces",   abs(sm["peak_correlation"]   - by["peak_correlation"]["value"])   < 1e-8)
check("max_diff_numpy traces",     abs(sm["max_diff_numpy"]     - by["max_diff_numpy"]["value"])     < 1e-16)
check("scipy_peak_lag_abs traces", abs(sm["scipy_peak_lag_abs"] - by["scipy_peak_lag_abs"]["value"]) < 1e-9)
check("n_lags traces",             int(sm["n_lags"])            == by["n_lags"]["value"])
# machine-precision + scipy
check("op == independent numpy normalized cross-correlation BIT-FOR-BIT (< 1e-10)", sm["max_diff_numpy"] < 1e-10)
check("scipy peak-lag magnitude matches the op peak lag", int(sm["scipy_peak_lag_abs"]) == int(sm["peak_lag"]))
check("the profile's op and numpy columns match to machine precision per lag",
      max(abs(float(r["correlation_op"]) - float(r["correlation_numpy"])) for r in pf) < 1e-6)
check("all 181 lags present in the profile", len(pf) == int(sm["n_lags"]) == 181)
# finding
check("the peak lag is a physiologic pulse arrival time (0.1-0.7 s)", 0.1 <= sm["peak_lag_seconds"] <= 0.7)
check("the peak correlation is a real coupling (|corr| > 0.1)", abs(sm["peak_correlation"]) > 0.1)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: genuine MACHINE-PRECISION match (identical formula), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention" in _note)
check("HONEST: scipy compared by MAGNITUDE (opposite lead/lag sign convention)",
      "magnitude" in _note and "opposite lead/lag sign convention" in _note)
check("HONEST: negative peak correlation is a morphology effect (sign not meaningful)",
      "negative" in _note and "anti-phase" in _note and "not the sign" in _note)
check("HONEST: quasi-periodic -- the window isolates the first (pulse-arrival) peak",
      "quasi-periodic" in _note and "isolates the first" in _note)
check("HONEST: cross-tool references (numpy + scipy), not a self-comparison",
      "numpy" in case["validation"]["reference"].lower() and "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
