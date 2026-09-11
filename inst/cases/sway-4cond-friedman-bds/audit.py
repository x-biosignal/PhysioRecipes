import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sway_friedman_summary.csv"))}
# claims trace to the artifact
check("Q_statistic traces", abs(sm["Q_statistic"] - by["Q_statistic"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df traces", int(sm["df"]) == by["df"]["value"])
check("rank_open_firm traces", abs(sm["rank_open_firm"] - by["rank_open_firm"]["value"]) < 1e-4)
check("rank_closed_foam traces", abs(sm["rank_closed_foam"] - by["rank_closed_foam"]["value"]) < 1e-4)
check("max_diff_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("max_diff_baser traces (bit-for-bit, == 0)", sm["max_diff_baser"] == by["max_diff_baser"]["value"] == 0)
check("monotone_order traces", int(sm["monotone_order"]) == by["monotone_order"]["value"])
check("n_subjects traces", int(sm["n_subjects"]) == by["n_subjects"]["value"])
check("k_conditions traces", int(sm["k_conditions"]) == by["k_conditions"]["value"])
# double reference: base R exact, scipy machine precision
check("friedmanTest == base R friedman.test BIT-FOR-BIT (|diff| == 0)", sm["max_diff_baser"] == 0)
check("friedmanTest == scipy.stats.friedmanchisquare to machine precision (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
# the finding: monotone sensory hierarchy on ranks AND on condition means
ranks = [sm["rank_open_firm"], sm["rank_closed_firm"], sm["rank_open_foam"], sm["rank_closed_foam"]]
means = [sm["mean_open_firm"], sm["mean_closed_firm"], sm["mean_open_foam"], sm["mean_closed_foam"]]
check("mean ranks monotone Open-Firm < Closed-Firm < Open-Foam < Closed-Foam", all(ranks[i] < ranks[i+1] for i in range(3)))
check("monotone_order flag agrees with the ranks", int(sm["monotone_order"]) == (1 if all(ranks[i] < ranks[i+1] for i in range(3)) else 0))
check("condition-mean path length also monotone (same ordering)", all(means[i] < means[i+1] for i in range(3)))
check("surface effect (firm->foam) dominates vision effect (open->closed): rank jumps", (ranks[2]-ranks[1]) > (ranks[1]-ranks[0]) and (ranks[2]-ranks[1]) > (ranks[3]-ranks[2]))
check("the omnibus difference is overwhelmingly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("df = k - 1", int(sm["df"]) == int(sm["k_conditions"]) - 1)
check("complete-block design (n=158, k=4)", int(sm["n_subjects"]) == 158 and int(sm["k_conditions"]) == 4)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new friedmanTest op (within-subject counterpart of oneWayAnova)",
      "new op" in _note and "friedmantest" in _note)
check("HONEST: path length from the certified swayMetrics",
      "swaymetrics" in _note and "certified" in _note)
check("HONEST: base R friedman.test bit-for-bit",
      "friedman.test" in _note and "bit-for-bit" in _note)
check("HONEST: scipy.stats.friedmanchisquare to machine precision",
      "friedmanchisquare" in _note and "machine precision" in _note)
check("HONEST: repeated-measures design (Friedman is the correct omnibus)",
      "repeated measures" in _note and "within-subject" in _note)
check("HONEST: monotone sensory ordering finding",
      "monotone" in _note and "open-firm" in _note and "closed-foam" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "friedmanchisquare" in case["validation"]["reference"].lower() and "friedman.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
