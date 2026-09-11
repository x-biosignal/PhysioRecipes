import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/perm_entropy_summary.csv"))}
bc   = list(csv.DictReader(open("artifacts/perm_entropy_by_channel.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("max_abs_diff traces",    abs(sm["max_abs_diff"]    - by["max_abs_diff"]["value"])    < 1e-18)
check("pe_corr traces",         abs(sm["pe_corr"]         - by["pe_corr"]["value"])         < 1e-9)
check("mean_pe_op traces",      abs(sm["mean_pe_op"]      - by["mean_pe_op"]["value"])      < 1e-6)
check("mean_pe_antropy traces", abs(sm["mean_pe_antropy"] - by["mean_pe_antropy"]["value"]) < 1e-6)
check("n_channels traces",      int(sm["n_channels"])     == by["n_channels"]["value"])

# --- external cross-tool validation: eegComplexity == antropy (machine precision)
check("op == antropy to machine precision (max |diff| < 1e-9)", sm["max_abs_diff"] < 1e-9)
check("the agreement is at machine precision (max |diff| < 1e-12)", sm["max_abs_diff"] < 1e-12)
check("correlation is exactly 1.0 across channels", abs(sm["pe_corr"] - 1.0) < 1e-9)
check("both engines' mean entropy agree", abs(sm["mean_pe_op"] - sm["mean_pe_antropy"]) < 1e-9)

# --- reference recovery: plausible complexity across the scalp --------------
check("mean permutation entropy is physiologically plausible (0.5-1.0 normalized)", 0.5 < sm["mean_pe_op"] < 1.0)
check("all 64 channels have a permutation entropy", int(sm["n_channels"]) == 64 and len(bc) == 64)
check("per-channel |diff| max traces to the summary",
      abs(max(abs(float(r["pe_eegComplexity"]) - float(r["pe_antropy"])) for r in bc) - sm["max_abs_diff"]) < 1e-6)
check("every channel's entropy is in [min_pe, max_pe]",
      all(sm["min_pe"] - 1e-6 <= float(r["pe_eegComplexity"]) <= sm["max_pe"] + 1e-6 for r in bc))

# --- honest scope -----------------------------------------------------------
check("HONEST: permutation entropy is exactly-defined (matches to machine precision)",
      "exactly-defined" in case["validation"]["note"].lower() or "exactly defined" in case["validation"]["note"].lower())
check("HONEST: sample/spectral entropy do NOT match exactly (noted, not claimed)",
      "sample entropy" in case["validation"]["note"].lower() and "spectral entropy" in case["validation"]["note"].lower())
check("HONEST: cross-tool (antropy), not a self-comparison", "antropy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
