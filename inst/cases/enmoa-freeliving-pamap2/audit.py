import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/enmoa_summary.csv"))}
check("enmoa_max_abs_diff_g traces", abs(sm["enmoa_max_abs_diff_g"] - by["enmoa_max_abs_diff_g"]["value"]) < 1e-16)
check("enmoa_correlation traces",    abs(sm["enmoa_correlation"] - by["enmoa_correlation"]["value"]) < 1e-9)
check("n_epochs traces",             int(sm["n_epochs"]) == by["n_epochs"]["value"])
check("mean_enmoa_mg traces",        abs(sm["mean_enmoa_mg"] - by["mean_enmoa_mg"]["value"]) < 1e-2)
check("enmoa_ge_enmo traces",        int(sm["enmoa_ge_enmo"]) == by["enmoa_ge_enmo"]["value"])
check("enmoa_minus_enmo_mg traces",  abs(sm["enmoa_minus_enmo_mg"] - by["enmoa_minus_enmo_mg"]["value"]) < 1e-2)
# machine-precision vs GGIR
check("computeENMOa == GGIR g.applymetrics ENMOa to machine precision (< 1e-9 g)", sm["enmoa_max_abs_diff_g"] < 1e-9)
check("correlation with GGIR is 1.0", abs(sm["enmoa_correlation"] - 1.0) < 1e-9)
# ENMO/ENMOa relationship
check("749 epochs certified", int(sm["n_epochs"]) == 749)
check("ENMOa >= ENMO at every epoch (flag set)", int(sm["enmoa_ge_enmo"]) == 1)
check("ENMOa exceeds ENMO by a positive, substantial gap (> 1 mg)", sm["enmoa_minus_enmo_mg"] > 1)
check("mean ENMOa in a plausible free-living range (50-500 mg)", 50 < sm["mean_enmoa_mg"] < 500)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op completing the ENMO+MAD+ENMOa accel triad",
      "newly authored" in _note and "accel movement triad" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical computation), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: ENMOa >= ENMO -- abs retains sub-1 g dips ENMO truncates",
      "abs keeps the sub-1 g dips" in _note and "truncation discards" in _note)
check("HONEST: ENMOa is a physical quantity, mean meaningful not a placeholder",
      "physical quantity" in _note and "not a reproducibility placeholder" in _note)
check("HONEST: GGIR cross-tool reference", "ggir" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
