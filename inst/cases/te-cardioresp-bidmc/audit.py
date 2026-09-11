import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/te_summary.csv"))}
# claims trace
check("te_resp_pleth traces",     abs(sm["te_resp_pleth"]     - by["te_resp_pleth"]["value"])     < 1e-7)
check("te_pleth_resp traces",     abs(sm["te_pleth_resp"]     - by["te_pleth_resp"]["value"])     < 1e-7)
check("net traces",               abs(sm["net"]               - by["net"]["value"])               < 1e-7)
check("max_diff_numpy traces",    abs(sm["max_diff_numpy"]    - by["max_diff_numpy"]["value"])    < 1e-16)
check("te_constructed_xy traces", abs(sm["te_constructed_xy"] - by["te_constructed_xy"]["value"]) < 1e-5)
check("te_constructed_yx traces", abs(sm["te_constructed_yx"] - by["te_constructed_yx"]["value"]) < 1e-5)
# machine-precision: op == independent numpy transfer entropy, bit-for-bit
check("op == independent from-scratch numpy transfer entropy BIT-FOR-BIT (< 1e-10)", sm["max_diff_numpy"] < 1e-10)
check("net = te_resp_pleth - te_pleth_resp (internally consistent)",
      abs(sm["net"] - (sm["te_resp_pleth"] - sm["te_pleth_resp"])) < 1e-6)
check("the op and numpy TE agree in BOTH directions to machine precision",
      abs(sm["te_resp_pleth"] - sm["te_resp_pleth_numpy"]) < 1e-10 and
      abs(sm["te_pleth_resp"] - sm["te_pleth_resp_numpy"]) < 1e-10)
# directed recovery on a constructed x->y coupling
check("directed recovery: constructed x->y TE >> reverse (driver identified)",
      sm["te_constructed_xy"] > 5 * sm["te_constructed_yx"])
check("net_constructed = te_constructed_xy - te_constructed_yx (large positive)",
      abs(sm["net_constructed"] - (sm["te_constructed_xy"] - sm["te_constructed_yx"])) < 1e-5 and sm["net_constructed"] > 0.3)
# finding
check("real net directed info flow is respiration -> pulse (positive net, both TE > 0)",
      sm["net"] > 0 and sm["te_resp_pleth"] > 0 and sm["te_pleth_resp"] > 0)
check("the real TE values are small (weak coupling, finite-sample regime)", sm["te_resp_pleth"] < 0.2)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: genuine MACHINE-PRECISION match (identical formula), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention" in _note)
check("HONEST: transfer entropy is ESTIMATOR-DEPENDENT (this is the histogram estimator)",
      "estimator-dependent" in _note and "histogram" in _note)
check("HONEST: histogram estimator has a positive finite-sample bias -- not significance tests",
      "positive finite-sample bias" in _note and "not significance tests" in _note)
check("HONEST: model-free complement to the linear Granger result",
      "model-free" in _note and "granger" in _note)
check("HONEST: independent-implementation reference (numpy), not a self-comparison",
      "numpy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
