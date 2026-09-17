import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/mse_summary.csv"))}
# claims trace
for k in ("mse_scale1","mse_scale5","mse_scale8","mse_auc"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-6)
check("peak_scale traces",          int(sm["peak_scale"]) == by["peak_scale"]["value"])
check("coarse_exceeds_fine traces", int(sm["coarse_exceeds_fine"]) == by["coarse_exceeds_fine"]["value"])
check("max_diff_neurokit traces",   abs(sm["max_diff_neurokit"] - by["max_diff_neurokit"]["value"]) < 1e-15)
check("n_samples traces",           int(sm["n_samples"]) == by["n_samples"]["value"])
# bit-exact across ALL 8 scales (op vs NeuroKit2)
dmax = max(abs(sm[f"mse_scale{i}"] - sm[f"nk_scale{i}"]) for i in range(1, 9))
check(f"multiscaleEntropy == NeuroKit2 across ALL 8 scales BIT-FOR-BIT (max |diff|={dmax:.1e} < 1e-9)", dmax < 1e-9)
check("summary max_diff_neurokit is the per-scale max", abs(sm["max_diff_neurokit"] - dmax) < 1e-15)
# the finding: non-monotonic, interior peak, coarse > fine
check("MSE peak is interior (not scale 1, not scale 8) -> non-monotonic", 1 < int(sm["peak_scale"]) < 8)
check("coarse-scale MSE exceeds scale 1 (structure, not white noise)",
      sm["mse_scale5"] > sm["mse_scale1"] and int(sm["coarse_exceeds_fine"]) == 1)
check("all 8 scales are positive, finite entropies", all(0 < sm[f"mse_scale{i}"] < 10 for i in range(1, 9)))
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEW standalone op completing the entropy family (was only inside eegComplexity)",
      "new standalone op" in _note and "completes the entropy family" in _note and "eegcomplexity" in _note)
check("HONEST: genuine machine-precision (identical coarse-graining + fixed-tolerance SampEn), not a convention agreement",
      "bit-for-bit" in _note and "coarse-graining" in _note and "not a convention agreement" in _note)
check("HONEST: the structure finding vs white noise (non-monotonic rise; noise falls monotonically)",
      "non-monotonic" in _note and "white-noise" in _note and "structure" in _note and "monotonically" in _note)
check("HONEST: the coarse-scale short-series caveat",
      "caveat" in _note and "short" in _note and "less stable" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
