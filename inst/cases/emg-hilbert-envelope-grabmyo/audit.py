import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/emg_envelope_summary.csv"))}
bc   = list(csv.DictReader(open("artifacts/emg_envelope_by_channel.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("max_abs_diff traces",        abs(sm["max_abs_diff_vs_scipy"] - by["max_abs_diff"]["value"])        < 1e-18)
check("n_channels traces",          int(sm["n_channels"])           == by["n_channels"]["value"])
check("mean_envelope traces",       abs(sm["mean_envelope"]         - by["mean_envelope"]["value"])       < 1e-6)
check("mean_modulation traces",     abs(sm["mean_modulation"]       - by["mean_modulation"]["value"])     < 1e-4)
check("most_active_channel traces", int(sm["most_active_channel"])  == by["most_active_channel"]["value"])

# --- external cross-tool validation: emgEnvelope(hilbert) == scipy (machine precision)
check("op == scipy.signal.hilbert to machine precision (< 1e-9)", sm["max_abs_diff_vs_scipy"] < 1e-9)
check("the agreement is at machine precision (< 1e-12)", sm["max_abs_diff_vs_scipy"] < 1e-12)
check("all 32 channels have a Hilbert envelope", int(sm["n_channels"]) == 32 and len(bc) == 32)
check("every channel matches scipy to machine precision",
      all(float(r["max_diff_vs_scipy"]) < 1e-9 for r in bc))

# --- reference recovery: a real activation envelope -------------------------
check("the envelope shows burst activity (mean peak/mean modulation > 1)", sm["mean_modulation"] > 1)
check("the modulation is substantial (> 3 = clear bursts, not flat)", sm["mean_modulation"] > 3)
check("the mean envelope amplitude is positive", sm["mean_envelope"] > 0)
check("the most-active channel is a valid channel index (1-32)", 1 <= int(sm["most_active_channel"]) <= 32)
check("the most-active channel has an above-average envelope",
      float([r for r in bc if int(r["channel"]) == int(sm["most_active_channel"])][0]["mean_envelope"])
      > sm["mean_envelope"])

# --- honest scope -----------------------------------------------------------
check("HONEST: Hilbert is exactly-defined (matches to machine precision)",
      "exactly-defined" in case["validation"]["note"].lower() or "exactly defined" in case["validation"]["note"].lower())
check("HONEST: upgrades emgEnvelope validation from RMS (grade D) to Hilbert (grade A)",
      "grade d" in case["validation"]["note"].lower() and "grade a" in case["validation"]["note"].lower())
check("HONEST: cross-tool (scipy), not a self-comparison", "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
