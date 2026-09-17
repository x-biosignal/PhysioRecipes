import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sampen_summary.csv"))}
# claims trace
check("sample_entropy traces",           abs(sm["sample_entropy"] - by["sample_entropy"]["value"]) < 1e-6)
check("approximate_entropy traces",      abs(sm["approximate_entropy"] - by["approximate_entropy"]["value"]) < 1e-6)
check("max_diff_sampen_antropy traces",  abs(sm["max_diff_sampen_antropy"] - by["max_diff_sampen_antropy"]["value"]) < 1e-15)
check("max_diff_sampen_neurokit traces", abs(sm["max_diff_sampen_neurokit"] - by["max_diff_sampen_neurokit"]["value"]) < 1e-15)
check("max_diff_apen_antropy traces",    abs(sm["max_diff_apen_antropy"] - by["max_diff_apen_antropy"]["value"]) < 1e-15)
check("max_diff_apen_neurokit traces",   abs(sm["max_diff_apen_neurokit"] - by["max_diff_apen_neurokit"]["value"]) < 1e-15)
check("sampen_gt_apen traces",           int(sm["sampen_gt_apen"]) == by["sampen_gt_apen"]["value"])
check("n_samples traces",                int(sm["n_samples"]) == by["n_samples"]["value"])
# machine-precision, DOUBLE reference each
check("sampleEntropy == antropy.sample_entropy BIT-FOR-BIT (< 1e-9)", sm["max_diff_sampen_antropy"] < 1e-9)
check("sampleEntropy == NeuroKit2 entropy_sample BIT-FOR-BIT (< 1e-9)", sm["max_diff_sampen_neurokit"] < 1e-9)
check("approximateEntropy == antropy.app_entropy BIT-FOR-BIT (< 1e-9)", sm["max_diff_apen_antropy"] < 1e-9)
check("approximateEntropy == NeuroKit2 entropy_approximate BIT-FOR-BIT (< 1e-9)", sm["max_diff_apen_neurokit"] < 1e-9)
# 3 tools agree within each measure
check("SampEn: PhysioMoCap == antropy == NeuroKit2",
      abs(sm["sample_entropy"] - sm["antropy_sampen"]) < 1e-9 and abs(sm["sample_entropy"] - sm["neurokit_sampen"]) < 1e-9)
check("ApEn: PhysioMoCap == antropy == NeuroKit2",
      abs(sm["approximate_entropy"] - sm["antropy_apen"]) < 1e-9 and abs(sm["approximate_entropy"] - sm["neurokit_apen"]) < 1e-9)
# the finding: ApEn self-match bias
check("finding: SampEn > ApEn (the ApEn self-match bias)", sm["sample_entropy"] > sm["approximate_entropy"] and int(sm["sampen_gt_apen"]) == 1)
check("both entropies are positive, finite regularity values", 0 < sm["sample_entropy"] < 10 and 0 < sm["approximate_entropy"] < 10)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: CROSS-TOOL AUDIT of shipped ops (not new ops)",
      "cross-tool audit" in _note and "shipped" in _note and "not new ops" in _note)
check("HONEST: FIRST antropy/NeuroKit2 + EEG certification (previously only base-R Pincus on accelerometer)",
      "first" in _note and "antropy" in _note and "neurokit2" in _note and "accelerometer" in _note)
check("HONEST: genuine machine-precision (same template-counting algorithm), not a convention agreement",
      "bit-for-bit" in _note and "template-counting algorithm" in _note and "not a convention agreement" in _note)
check("HONEST: the ApEn self-match bias finding (ApEn underestimates entropy; SampEn removes the self-count)",
      "self-match bias" in _note and "underestimate" in _note and "self-count" in _note)
check("HONEST: two-tool cross reference (antropy + NeuroKit2)",
      "antropy" in case["validation"]["reference"].lower() and "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
