import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/mad_summary.csv"))}
check("mad_max_abs_diff_g traces", abs(sm["mad_max_abs_diff_g"] - by["mad_max_abs_diff_g"]["value"]) < 1e-16)
check("mad_correlation traces",    abs(sm["mad_correlation"] - by["mad_correlation"]["value"]) < 1e-9)
check("n_epochs traces",           int(sm["n_epochs"]) == by["n_epochs"]["value"])
check("mean_mad_mg traces",        abs(sm["mean_mad_mg"] - by["mean_mad_mg"]["value"]) < 1e-2)
check("max_mad_mg traces",         abs(sm["max_mad_mg"] - by["max_mad_mg"]["value"]) < 1e-1)
check("min_mad_mg traces",         abs(sm["min_mad_mg"] - by["min_mad_mg"]["value"]) < 1e-2)
# machine-precision vs GGIR
check("computeMAD == GGIR g.applymetrics MAD to machine precision (< 1e-9 g)", sm["mad_max_abs_diff_g"] < 1e-9)
check("correlation with GGIR is 1.0", abs(sm["mad_correlation"] - 1.0) < 1e-9)
# physical movement profile
check("749 epochs certified", int(sm["n_epochs"]) == 749)
check("MAD range is physical and ordered (min < mean < max)", sm["min_mad_mg"] < sm["mean_mad_mg"] < sm["max_mad_mg"])
check("mean MAD in a plausible free-living range (50-500 mg)", 50 < sm["mean_mad_mg"] < 500)
check("all MAD values positive (valid deviation)", sm["min_mad_mg"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the MAD gap (ENMO existed, MAD did not)",
      "newly authored" in _note and "but not mad" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical computation), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: MAD and ENMO genuinely complementary (variation vs elevation)",
      "genuinely complementary" in _note and "variation of the magnitude" in _note)
check("HONEST: MAD is a physical quantity, mean/max/min meaningful not placeholders",
      "physical quantity" in _note and "not reproducibility placeholders" in _note)
check("HONEST: GGIR cross-tool reference", "ggir" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
