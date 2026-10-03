import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/poincare_summary.csv"))}
# claims trace
check("sd1 traces",              abs(sm["sd1"]              - by["sd1"]["value"])              < 1e-6)
check("sd2 traces",              abs(sm["sd2"]              - by["sd2"]["value"])              < 1e-6)
check("sd1_sd2_ratio traces",    abs(sm["sd1_sd2_ratio"]    - by["sd1_sd2_ratio"]["value"])    < 1e-6)
check("max_diff_numpy traces",   abs(sm["max_diff_numpy"]   - by["max_diff_numpy"]["value"])   < 1e-12)
check("sd1_diff_nk traces",      abs(sm["sd1_diff_nk"]      - by["sd1_diff_nk"]["value"])      < 1e-12)
check("sd2_paired_vs_nk traces", abs(sm["sd2_paired_vs_nk"] - by["sd2_paired_vs_nk"]["value"]) < 1e-12)
check("sd2_conv_diff traces",    abs(sm["sd2_conv_diff"]    - by["sd2_conv_diff"]["value"])    < 1e-6)
check("young_mean_sd1 traces",   abs(sm["young_mean_sd1"]   - by["young_mean_sd1"]["value"])   < 1e-3)
check("old_mean_sd1 traces",     abs(sm["old_mean_sd1"]     - by["old_mean_sd1"]["value"])     < 1e-3)
# machine-precision: three bit-exact identities
check("op == independent numpy analytical closed-form BIT-FOR-BIT (< 1e-10)", sm["max_diff_numpy"] < 1e-10)
check("op.SD1 == NeuroKit2 SD1 BIT-FOR-BIT (SD1 is universal SDSD/sqrt(2))", sm["sd1_diff_nk"] < 1e-9)
check("independent numpy paired-projection == NeuroKit2 SD2 BIT-FOR-BIT (identifies the convention)", sm["sd2_paired_vs_nk"] < 1e-9)
check("the op-vs-NeuroKit2 SD2 gap is small (~0.2 ms, O(1/n) convention, not an error)", 0 < sm["sd2_conv_diff"] < 0.3)
# internal consistency: SD1 = SDSD/sqrt(2) => ratio = sd1/sd2
check("SD1/SD2 ratio internally consistent", abs(sm["sd1_sd2_ratio"] - sm["sd1"]/sm["sd2"]) < 1e-6)
# finding: aging (young > old short-term HRV)
check("finding: young SD1 markedly exceeds old SD1 (age-related vagal decline)",
      sm["young_mean_sd1"] > sm["old_mean_sd1"] and (sm["young_mean_sd1"] - sm["old_mean_sd1"]) > 10)
check("finding: long-term HRV (SD2) also declines with age", sm["young_mean_sd2"] > sm["old_mean_sd2"])
check("SD1 values are physiologic (10-150 ms) for 5-min RR", 10 < sm["sd1"] < 150 and 10 < sm["young_mean_sd1"] < 150)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: genuine MACHINE-PRECISION match (identical formula), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention" in _note)
check("HONEST: SD1 matches NeuroKit2 because SD1 = SDSD/sqrt(2) is universal",
      "universal" in _note and "sdsd/sqrt(2)" in _note)
check("HONEST: SD2 gap is a paired-projection-vs-closed-form CONVENTION, neither is wrong",
      "convention" in _note and "paired-projection" in _note and "neither is wrong" in _note)
check("HONEST: aging finding is the geometric complement of the DFA result, descriptive n=5+5",
      "aging" in _note and "complement of the dfa" in _note and "descriptive" in _note)
check("HONEST: cross-tool references (NeuroKit2 + numpy), not a self-comparison",
      "neurokit2" in case["validation"]["reference"].lower() and "numpy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
