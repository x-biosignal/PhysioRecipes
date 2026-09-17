import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/dunn_summary.csv"))}
# claims trace to the artifact
check("max_abs_z traces", abs(sm["max_abs_z"] - by["max_abs_z"]["value"]) < 1e-6)
check("p_adj_C_A traces", abs(sm["p_adj_C_A"] - by["p_adj_C_A"]["value"]) < 1e-8)
check("p_adj_K_A traces", abs(sm["p_adj_K_A"] - by["p_adj_K_A"]["value"]) < 1e-4)
check("p_adj_H_K traces", abs(sm["p_adj_H_K"] - by["p_adj_H_K"]["value"]) < 1e-4)
check("max_diff_z_pmcmr traces (machine precision, < 1e-9)", abs(sm["max_diff_z_pmcmr"] - by["max_diff_z_pmcmr"]["value"]) < 1e-9)
check("max_diff_padj_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_padj_scipy"] - by["max_diff_padj_scipy"]["value"]) < 1e-9)
check("n_sig_hc_vs_pathology traces", int(sm["n_sig_hc_vs_pathology"]) == by["n_sig_hc_vs_pathology"]["value"])
check("n_sig_pathology_pathology traces", int(sm["n_sig_pathology_pathology"]) == by["n_sig_pathology_pathology"]["value"])
check("n_pairs traces", int(sm["n_pairs"]) == by["n_pairs"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
# triple reference: PMCMRplus + scikit_posthocs, machine precision
check("dunnTest z == PMCMRplus to machine precision (< 1e-9)", sm["max_diff_z_pmcmr"] < 1e-9)
check("dunnTest p_adj == scikit_posthocs.posthoc_dunn to machine precision (< 1e-9)", sm["max_diff_padj_scipy"] < 1e-9)
# the pattern, from the per-pair padj rows
hc_pairs   = ["padj_A-HC", "padj_K-HC", "padj_H-HC", "padj_C-HC"]
path_pairs = ["padj_K-A", "padj_H-A", "padj_H-K", "padj_C-A", "padj_C-K", "padj_C-H"]
check("all four healthy-vs-pathology pairs significant (p < 0.05)", all(sm[k] < 0.05 for k in hc_pairs))
check("exactly 4 of 6 pathology-pathology pairs significant", sum(sm[k] < 0.05 for k in path_pairs) == 4)
check("calcaneus differs from ankle, knee and hip (C-A, C-K, C-H all significant)", all(sm[k] < 0.05 for k in ["padj_C-A", "padj_C-K", "padj_C-H"]))
check("hip differs from ankle (H-A significant)", sm["padj_H-A"] < 0.05)
check("knee-vs-ankle and hip-vs-knee are NOT significant", sm["padj_K-A"] > 0.05 and sm["padj_H-K"] > 0.05)
check("n_sig counts match the per-pair rows", int(sm["n_sig_hc_vs_pathology"]) == sum(sm[k] < 0.05 for k in hc_pairs) == 4 and int(sm["n_sig_pathology_pathology"]) == sum(sm[k] < 0.05 for k in path_pairs) == 4)
check("largest |z| is the healthy-vs-calcaneus separation (z ~ 16)", 15 < sm["max_abs_z"] < 17)
check("10 pairwise comparisons for 5 groups", int(sm["n_pairs"]) == 10)
check("large cohort (n_total = 1844)", int(sm["n_total"]) == 1844)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new dunnTest op",
      "new op" in _note and "dunntest" in _note)
check("HONEST: push-off from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: PMCMRplus to machine precision",
      "pmcmrplus" in _note and "machine precision" in _note)
check("HONEST: scikit_posthocs.posthoc_dunn to machine precision",
      "scikit_posthocs.posthoc_dunn" in _note and "machine precision" in _note)
check("HONEST: push-off grades the pathologies (contrast with dynamic range 0/6)",
      "grades the pathologies" in _note and "0/6" in _note)
check("HONEST: dynamic range flags, push-off grades",
      "flags impairment" in _note and "grades it" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (PMCMRplus + scikit_posthocs)",
      "pmcmrplus" in case["validation"]["reference"].lower() and "scikit_posthocs" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
