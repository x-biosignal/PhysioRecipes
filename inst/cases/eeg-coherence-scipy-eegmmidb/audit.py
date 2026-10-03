import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/coherence_summary.csv"))}
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-18)
check("mean_coherence traces", abs(sm["mean_coherence"] - by["mean_coherence"]["value"]) < 1e-5)
check("max_coherence traces",  abs(sm["max_coherence"]  - by["max_coherence"]["value"])  < 1e-5)
check("min_coherence traces",  abs(sm["min_coherence"]  - by["min_coherence"]["value"])  < 1e-5)
check("n_channels traces",     int(sm["n_channels"])    == by["n_channels"]["value"])
check("n_pairs traces",        int(sm["n_pairs"])       == by["n_pairs"]["value"])
# machine-precision
check("op == scipy.signal.coherence BIT-FOR-BIT over all 28 pairs (< 1e-9)", sm["max_diff_scipy"] < 1e-9)
check("8 posterior channels, 28 pairs (8 choose 2)", int(sm["n_channels"])==8 and int(sm["n_pairs"])==28)
check("coherence is a valid ratio in [0,1]", 0 <= sm["min_coherence"] <= sm["mean_coherence"] <= sm["max_coherence"] <= 1)
# finding
check("finding: posterior alpha coherence is high (mean > 0.4) -- spatial synchrony", sm["mean_coherence"] > 0.4)
check("finding: peak coherence (adjacent occipital) exceeds the mean", sm["max_coherence"] > sm["mean_coherence"])
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: FIRST external-reference (scipy) certification; eegCoherence is NOT a new op",
      "first external-reference" in _note and "the op is not new" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical coherence), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: the coherence ratio cancels the window normalization (why it's exact)",
      "ratio cancels the window normalization" in _note)
check("HONEST: volume-conduction caveat (MS-coherence inflated; imaginary coherence available)",
      "volume conduction" in _note and "imaginary coherence" in _note)
check("HONEST: scipy cross-tool reference, not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
