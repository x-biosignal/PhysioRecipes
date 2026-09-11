import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_cognition_partial_summary.csv"))}
# claims trace to the artifact
check("partial_spearman_r traces", abs(sm["partial_spearman_r"] - by["partial_spearman_r"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df traces", int(sm["df"]) == by["df"]["value"])
check("max_diff_ppcor traces (machine precision, < 1e-9)", abs(sm["max_diff_ppcor"] - by["max_diff_ppcor"]["value"]) < 1e-9)
check("max_diff_formula traces (machine precision, < 1e-9)", abs(sm["max_diff_formula"] - by["max_diff_formula"]["value"]) < 1e-9)
check("partial_pearson_r traces", abs(sm["partial_pearson_r"] - by["partial_pearson_r"]["value"]) < 1e-6)
check("partial_pearson_p traces", abs(sm["partial_pearson_p"] - by["partial_pearson_p"]["value"]) < 1e-3)
check("marginal_spearman traces", abs(sm["marginal_spearman"] - by["marginal_spearman"]["value"]) < 1e-6)
check("attenuated traces", int(sm["attenuated"]) == by["attenuated"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
# double reference: ppcor + closed-form, machine precision
check("partialCorrelation == ppcor::pcor.test to machine precision (< 1e-9)", sm["max_diff_ppcor"] < 1e-9)
check("partialCorrelation == closed-form recompute to machine precision (< 1e-9)", sm["max_diff_formula"] < 1e-9)
# the finding: attenuation with age; rank survives, linear vanishes
check("partial Spearman is attenuated relative to marginal (partial < marginal)", sm["partial_spearman_r"] < sm["marginal_spearman"] and int(sm["attenuated"]) == 1)
check("rank partial correlation still significant (p < 0.05)", 10 ** (-sm["neg_log10_p"]) < 0.05)
check("linear (Pearson) partial correlation vanishes (p > 0.05, non-significant)", sm["partial_pearson_p"] > 0.05)
check("age explains most of the link (partial < half the marginal)", sm["partial_spearman_r"] < 0.5 * sm["marginal_spearman"])
check("pearson partial is near zero (|r| < 0.1)", abs(sm["partial_pearson_r"]) < 0.1)
check("df = n - 2 - 1 (one covariate)", int(sm["df"]) == int(sm["n"]) - 3)
check("cohort n=158", int(sm["n"]) == 158)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new partialCorrelation op",
      "new op" in _note and "partialcorrelation" in _note)
check("HONEST: sway from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: ppcor::pcor.test to machine precision",
      "ppcor::pcor.test" in _note and "machine precision" in _note)
check("HONEST: Pearson partial bit-for-bit vs the closed-form",
      "closed-form" in _note and "bit-for-bit" in _note)
check("HONEST: largely age-confounded finding",
      "age-confounded" in _note or "largely age" in _note)
check("HONEST: resolves the sibling case's open question",
      "resolves" in _note and "open question" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-reference cross check (ppcor + closed-form)",
      "ppcor::pcor.test" in case["validation"]["reference"].lower() and "closed-form" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
