import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/nemenyi_summary.csv"))}
# claims trace to the artifact
check("p_firm_vision traces", abs(sm["p_firm_vision"] - by["p_firm_vision"]["value"]) < 1e-6)
check("p_foam_vision traces", abs(sm["p_foam_vision"] - by["p_foam_vision"]["value"]) < 1e-9)
check("stat_extreme traces", abs(sm["stat_extreme"] - by["stat_extreme"]["value"]) < 1e-6)
check("max_diff_pmcmr traces (bit-for-bit, == 0)", sm["max_diff_pmcmr"] == by["max_diff_pmcmr"]["value"] == 0)
check("max_diff_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("foam_vision_stronger traces", int(sm["foam_vision_stronger"]) == by["foam_vision_stronger"]["value"])
check("n_sig traces", int(sm["n_sig"]) == by["n_sig"]["value"])
check("n_pairs traces", int(sm["n_pairs"]) == by["n_pairs"]["value"])
check("n_subjects traces", int(sm["n_subjects"]) == by["n_subjects"]["value"])
# triple reference: PMCMRplus bit-for-bit + scikit machine precision
check("nemenyiTest == PMCMRplus::frdAllPairsNemenyiTest BIT-FOR-BIT (|diff| == 0)", sm["max_diff_pmcmr"] == 0)
check("nemenyiTest == scikit_posthocs.posthoc_nemenyi_friedman to machine precision (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
# the finding: all pairs differ; vision effect surface-dependent
p_firm = sm["p_Closed-Firm~Open-Firm"]; p_foam = sm["p_Closed-Foam~Open-Foam"]
check("firm-vision matches the per-pair row", abs(p_firm - sm["p_firm_vision"]) < 1e-9)
check("foam-vision matches the per-pair row (8-dp-rounded detail)", abs(p_foam - sm["p_foam_vision"]) < 1e-8)
check("all six condition pairs are significant (p < 0.05)", int(sm["n_sig"]) == 6 == sum(1 for k in sm if k.startswith("p_") and "~" in k and sm[k] < 0.05))
check("vision effect BORDERLINE on firm (0.01 < p < 0.05)", 0.01 < p_firm < 0.05)
check("vision effect STRONG on foam (p < 1e-4)", p_foam < 1e-4)
check("vision effect is stronger on foam than firm (p_foam << p_firm)", p_foam < p_firm and int(sm["foam_vision_stronger"]) == 1)
check("the firm/foam vision-effect gap spans several orders of magnitude", (p_firm / p_foam) > 1e4)
check("6 pairwise comparisons for 4 conditions", int(sm["n_pairs"]) == 6)
check("complete-block cohort (n=158)", int(sm["n_subjects"]) == 158)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new nemenyiTest op",
      "new op" in _note and "nemenyitest" in _note)
check("HONEST: sway from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: PMCMRplus bit-for-bit",
      "pmcmrplus" in _note and "bit-for-bit" in _note)
check("HONEST: scikit_posthocs.posthoc_nemenyi_friedman to machine precision",
      "scikit_posthocs.posthoc_nemenyi_friedman" in _note and "machine precision" in _note)
check("HONEST: sensory reweighting, vision effect depends on the surface",
      "sensory reweighting" in _note and "depends on the surface" in _note)
check("HONEST: borderline on firm, strong on foam",
      "borderline on firm" in _note and "strong on foam" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (PMCMRplus + scikit_posthocs)",
      "frdallpairsnemenyitest" in case["validation"]["reference"].lower() and "posthoc_nemenyi_friedman" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
