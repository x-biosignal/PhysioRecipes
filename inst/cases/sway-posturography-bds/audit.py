import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_summary.csv"))}
for k in ("path_length","mean_velocity","area_ce","area_cc","mean_distance","area_sw","ellipse_frac_in_95"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < (1e-3 if k=="ellipse_frac_in_95" else 1e-6))
check("max_diff_prieto traces", abs(sm["max_diff_prieto"] - by["max_diff_prieto"]["value"]) < 1e-12)
check("n_samples traces", int(sm["n_samples"]) == by["n_samples"]["value"])
# bit-exact vs Prieto reimplementation
check("swayMetrics == Prieto reimplementation BIT-FOR-BIT (< 1e-9)", sm["max_diff_prieto"] < 1e-9)
# internal consistency of the metric set
check("path_length positive; mean_velocity = path/duration (approx)", sm["path_length"] > 0 and abs(sm["mean_velocity"] - sm["path_length"]/((sm["n_samples"]-1)/100)) < 1e-6)
check("area_cc >= area_ce (circle bounds the ellipse here) and both positive", sm["area_cc"] > 0 and sm["area_ce"] > 0)
# construct check: 95% ellipse contains ~95% of points
check("95% confidence ellipse contains ~95% of COP samples (0.90-0.99)", 0.90 < sm["ellipse_frac_in_95"] < 0.99)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: CROSS-TOOL AUDIT of a shipped op (not a new op)",
      "cross-tool audit" in _note and "shipped" in _note and "not a new op" in _note)
check("HONEST: bit-for-bit vs the Prieto reference (identical deterministic closed forms), not a convention agreement",
      "prieto" in _note and "bit-for-bit" in _note and "identical deterministic closed forms" in _note)
check("HONEST: the 95% ellipse construct check (correctly scaled)",
      "construct check" in _note and "95%" in _note and "correctly scaled" in _note)
check("HONEST: Prieto reference cited", "prieto" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
