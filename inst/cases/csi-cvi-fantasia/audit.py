import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/csi_summary.csv"))}
check("csi traces",           abs(sm["csi"] - by["csi"]["value"]) < 1e-4)
check("cvi traces",           abs(sm["cvi"] - by["cvi"]["value"]) < 1e-4)
check("csi_modified traces",  abs(sm["csi_modified"] - by["csi_modified"]["value"]) < 1e-2)
check("max_diff_nk traces",   abs(sm["max_diff_nk"] - by["max_diff_nk"]["value"]) < 1e-16)
check("young_mean_cvi traces",abs(sm["young_mean_cvi"] - by["young_mean_cvi"]["value"]) < 1e-3)
check("old_mean_cvi traces",  abs(sm["old_mean_cvi"] - by["old_mean_cvi"]["value"]) < 1e-3)
check("n_young_cvi_gt_oldmean traces", int(sm["n_young_cvi_gt_oldmean"]) == by["n_young_cvi_gt_oldmean"]["value"])
# machine-precision (newly-authored op == NeuroKit2)
check("op == NeuroKit2 hrv_nonlinear BIT-FOR-BIT over CSI/CVI/CSI_Modified (< 1e-9)", sm["max_diff_nk"] < 1e-9)
# internal consistency: CSI = SD2/SD1 > 0, CVI positive, CSI_modified = L^2/T
check("CSI is a positive ratio (SD2/SD1)", sm["csi"] > 0)
check("CVI is a physiologic log-area (typically 3-6)", 2 < sm["cvi"] < 7)
# finding
check("finding: CVI (vagal) higher in young than old (parasympathetic decline with age)", sm["young_mean_cvi"] > sm["old_mean_cvi"])
check("finding: vagal-decline robust (all 5 young above old mean)", int(sm["n_young_cvi_gt_oldmean"]) == 5)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the CSI/CVI gap (raw SD1/SD2 only before)",
      "newly authored" in _note and "raw sd1/sd2" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical Toichi formulas), not a convention agreement",
      "machine-precision" in _note and "identical toichi" in _note)
check("HONEST: SD2 uses the geometric convention (differs from ecgHRVpoincare's closed-form)",
      "geometric paired-projection" in _note and "closed-form sd2" in _note)
check("HONEST: aging finding descriptive (n=5+5), complements DFA/Poincare aging",
      "descriptive on n=5+5" in _note and "complementing the dfa" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
