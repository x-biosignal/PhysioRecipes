import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pushoff_kruskal_summary.csv"))}
# claims trace to the artifact
check("H_statistic traces", abs(sm["H_statistic"] - by["H_statistic"]["value"]) < 1e-6)
check("neg_log10_p traces", abs(sm["neg_log10_p"] - by["neg_log10_p"]["value"]) < 1e-2)
check("df traces", int(sm["df"]) == by["df"]["value"])
check("rank_hc traces", abs(sm["rank_hc"] - by["rank_hc"]["value"]) < 1e-3)
check("rank_calcaneus traces", abs(sm["rank_calcaneus"] - by["rank_calcaneus"]["value"]) < 1e-3)
check("max_diff_scipy traces (machine precision, < 1e-9)", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("max_diff_baser traces (bit-for-bit, == 0)", sm["max_diff_baser"] == by["max_diff_baser"]["value"] == 0)
check("hc_rank_highest traces", int(sm["hc_rank_highest"]) == by["hc_rank_highest"]["value"])
check("calcaneus_rank_lowest traces", int(sm["calcaneus_rank_lowest"]) == by["calcaneus_rank_lowest"]["value"])
check("n_total traces", int(sm["n_total"]) == by["n_total"]["value"])
# double reference: base R exact, scipy machine precision
check("kruskalTest == base R kruskal.test BIT-FOR-BIT (|diff| == 0)", sm["max_diff_baser"] == 0)
check("kruskalTest == scipy.stats.kruskal to machine precision (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
# the finding: healthy highest, calcaneus lowest; push-off discriminates the pathology classes
ranks = {"HC": sm["rank_hc"], "A": sm["rank_ankle"], "K": sm["rank_knee"], "H": sm["rank_hip"], "C": sm["rank_calcaneus"]}
means = {"HC": sm["mean_HC"], "A": sm["mean_A"], "K": sm["mean_K"], "H": sm["mean_H"], "C": sm["mean_C"]}
ns    = {k: int(sm[f"n_{k}"]) for k in ["HC","A","K","H","C"]}
check("healthy controls have the highest mean rank", max(ranks, key=ranks.get) == "HC" and int(sm["hc_rank_highest"]) == 1)
check("calcaneus pathology has the lowest mean rank", min(ranks, key=ranks.get) == "C" and int(sm["calcaneus_rank_lowest"]) == 1)
check("healthy push-off peak exceeds EVERY pathology class", all(means["HC"] > means[k] for k in ["A","K","H","C"]))
check("calcaneus push-off peak is the smallest of all five", min(means, key=means.get) == "C")
check("push-off DISCRIMINATES pathology (ranks not clustered: hip-ankle gap > 100)", (ranks["H"] - ranks["A"]) > 100)
check("mean-rank order matches push-off-mean order (C<A<K<H<HC)",
      [k for k in sorted(ranks, key=ranks.get)] == [k for k in sorted(means, key=means.get)])
check("the omnibus difference is overwhelmingly significant (-log10 p > 3)", sm["neg_log10_p"] > 3)
check("df = k - 1", int(sm["df"]) == int(sm["k_groups"]) - 1)
check("n_total = sum of per-class n", int(sm["n_total"]) == sum(ns.values()))
check("five classes (k=5), large cohort (n_total=1844)", int(sm["k_groups"]) == 5 and int(sm["n_total"]) == 1844)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new kruskalTest op (distribution-free counterpart of oneWayAnova)",
      "new op" in _note and "kruskaltest" in _note)
check("HONEST: push-off peak from the certified grfLandmarks",
      "grflandmarks" in _note and "certified" in _note)
check("HONEST: base R kruskal.test bit-for-bit",
      "kruskal.test" in _note and "bit-for-bit" in _note)
check("HONEST: scipy.stats.kruskal to machine precision",
      "scipy.stats.kruskal" in _note and "machine precision" in _note)
check("HONEST: Kruskal-Wallis chosen because the data is right-skewed (distribution-free)",
      "right-skewed" in _note and "distribution-free" in _note)
check("HONEST: push-off discriminates pathology; calcaneus worst propulsion",
      "discriminate" in _note and "calcaneus" in _note)
check("HONEST: cross-sectional association, not causation",
      "association, not causation" in _note)
check("HONEST: two-tool cross reference (scipy + base R)",
      "scipy.stats.kruskal" in case["validation"]["reference"].lower() and "kruskal.test" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
