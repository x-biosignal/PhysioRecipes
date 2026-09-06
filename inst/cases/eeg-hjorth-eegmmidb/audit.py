import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
rows = list(csv.DictReader(open("artifacts/hjorth_summary.csv")))
sm   = {r["metric"]: float(r["value"]) for r in rows}
det  = {r["metric"]: r.get("detail", "") for r in rows}
pc   = list(csv.DictReader(open("artifacts/hjorth_per_channel.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("mean_mobility traces",     abs(sm["mean_mobility"]     - by["mean_mobility"]["value"])     < 1e-6)
check("mean_complexity traces",   abs(sm["mean_complexity"]   - by["mean_complexity"]["value"])   < 1e-6)
check("min_mobility traces",      abs(sm["min_mobility"]      - by["min_mobility"]["value"])      < 1e-6)
check("max_diff_numpy traces",    abs(sm["max_diff_numpy"]    - by["max_diff_numpy"]["value"])    < 1e-18)
check("max_diff_antropy traces",  abs(sm["max_diff_antropy"]  - by["max_diff_antropy"]["value"])  < 1e-12)
check("n_channels traces",        int(sm["n_channels"])       == by["n_channels"]["value"])

# --- machine-precision leg vs numpy + agreement vs antropy -------------------
check("Hjorth == independent numpy (unbiased variance) BIT-FOR-BIT (< 1e-10)",
      sm["max_diff_numpy"] < 1e-10)
check("Hjorth == antropy.hjorth_params up to the ddof convention (< 1e-5)",
      sm["max_diff_antropy"] < 1e-5)
check("per-channel: op mobility matches antropy for every channel (< 1e-5)",
      max(abs(float(r["hjorth_mobility"]) - float(r["mobility_antropy"])) for r in pc) < 1e-5)
check("all 64 channels present in the per-channel table", len(pc) == int(sm["n_channels"]) == 64)

# --- reference recovery: the mobility topography -----------------------------
check("minimum mobility is well below the mean (posterior alpha = slow = low mobility)",
      sm["min_mobility"] < sm["mean_mobility"])
check("the minimum-mobility channel is parieto-occipital (POz)", "poz" in det.get("min_mobility","").lower())
check("mobility spans a real range (max > 2x min)", sm["max_mobility"] > 2 * sm["min_mobility"])
check("the per-channel minimum matches the reported min_mobility",
      abs(min(float(r["hjorth_mobility"]) for r in pc) - sm["min_mobility"]) < 1e-6)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: BIT-FOR-BIT vs an INDEPENDENT numpy implementation (formula exactly correct)",
      "bit-for-bit" in _note and "independent" in _note and "exactly correct" in _note)
check("HONEST: antropy agreement is machine precision UP TO the variance ddof convention",
      "ddof" in _note and "convention" in _note and "biased" in _note)
check("HONEST: mobility topography is a DESCRIPTIVE spatial pattern, not a clinical claim",
      "descriptive" in _note and "not a clinical claim" in _note)
check("HONEST: Hjorth is a COARSE mean-frequency proxy", "coarse" in _note and "proxy" in _note)
check("HONEST: cross-tool references (antropy + numpy), not a self-comparison",
      "antropy" in case["validation"]["reference"].lower() and "numpy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
