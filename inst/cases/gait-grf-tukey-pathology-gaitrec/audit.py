import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/tukey_summary.csv"))}
# claims trace to the artifact
check("diff_A_HC traces", abs(sm["diff_A_HC"] - by["diff_A_HC"]["value"]) < 1e-6)
check("neg_log10_p_A_HC traces", abs(sm["neg_log10_p_A_HC"] - by["neg_log10_p_A_HC"]["value"]) < 1e-2)
check("p_K_A traces", abs(sm["p_K_A"] - by["p_K_A"]["value"]) < 1e-4)
check("p_min_pathology_pathology traces", abs(sm["p_min_pathology_pathology"] - by["p_min_pathology_pathology"]["value"]) < 1e-4)
check("max_diff_p_baser traces (machine precision, < 1e-9)", abs(sm["max_diff_p_baser"] - by["max_diff_p_baser"]["value"]) < 1e-9)
check("max_diff_p_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_p_scipy"] - by["max_diff_p_scipy"]["value"]) < 1e-9)
check("n_sig_hc_vs_pathology traces", int(sm["n_sig_hc_vs_pathology"]) == by["n_sig_hc_vs_pathology"]["value"])
check("n_sig_pathology_pathology traces", int(sm["n_sig_pathology_pathology"]) == by["n_sig_pathology_pathology"]["value"])
check("n_pairs traces", int(sm["n_pairs"]) == by["n_pairs"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
# double reference: base R + scipy, machine precision
check("tukeyHSD == base R TukeyHSD to machine precision (< 1e-9)", sm["max_diff_p_baser"] < 1e-9)
check("tukeyHSD == scipy.stats.tukey_hsd to machine precision (< 1e-9)", sm["max_diff_p_scipy"] < 1e-9)
# the pattern, from the per-pair rows
hc_pairs   = ["p_A-HC", "p_K-HC", "p_H-HC", "p_C-HC"]
path_pairs = ["p_K-A", "p_H-A", "p_H-K", "p_C-A", "p_C-K", "p_C-H"]
check("all four healthy-vs-pathology pairs are significant (p < 0.05)", all(sm[k] < 0.05 for k in hc_pairs))
check("none of the six pathology-pathology pairs are significant (p > 0.05)", all(sm[k] > 0.05 for k in path_pairs))
check("n_sig_hc_vs_pathology (4) matches the per-pair count", int(sm["n_sig_hc_vs_pathology"]) == sum(sm[k] < 0.05 for k in hc_pairs) == 4)
check("n_sig_pathology_pathology (0) matches the per-pair count", int(sm["n_sig_pathology_pathology"]) == sum(sm[k] < 0.05 for k in path_pairs) == 0)
check("p_min_pathology_pathology equals the smallest pathology-pathology p", abs(sm["p_min_pathology_pathology"] - min(sm[k] for k in path_pairs)) < 1e-4)
check("10 pairwise comparisons for 5 groups (5 choose 2)", int(sm["n_pairs"]) == 10)
check("large cohort (n_total = 1844)", int(sm["n_total"]) == 1844)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new tukeyHSD op",
      "new op" in _note and "tukeyhsd" in _note)
check("HONEST: dynamic range from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: base R TukeyHSD to machine precision",
      "stats::tukeyhsd" in _note and "machine precision" in _note)
check("HONEST: scipy.stats.tukey_hsd to machine precision",
      "scipy.stats.tukey_hsd" in _note and "machine precision" in _note)
check("HONEST: separates healthy from pathological, not the pathology classes",
      "separates healthy from pathological" in _note and "not the pathology classes" in _note)
check("HONEST: complements the push-off case (dynamic range flags, push-off grades)",
      "push-off" in _note and "grade" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (base R + scipy)",
      "stats::tukeyhsd" in case["validation"]["reference"].lower() and "scipy.stats.tukey_hsd" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
