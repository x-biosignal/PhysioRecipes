import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/lz_summary.csv"))}
bs   = {r["stage"]: r for r in csv.DictReader(open("artifacts/lz_by_stage.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("lz_n3_op traces",      abs(sm["lz_n3"]         - by["lz_n3_op"]["value"])      < 1e-6)
check("lz_wake traces",       abs(sm["lz_wake"]       - by["lz_wake"]["value"])       < 1e-6)
check("lz_rem traces",        abs(sm["lz_rem"]        - by["lz_rem"]["value"])        < 1e-6)
check("wake_minus_n3 traces", abs(sm["wake_minus_n3"] - by["wake_minus_n3"]["value"]) < 1e-6)
check("abs_diff claim is ~0 (machine precision)", by["abs_diff"]["value"] < 1e-9)

# --- external cross-tool validation: eegComplexity LZ == antropy -------------
check("op == antropy per stage to machine precision (< 1e-9)",
      all(abs(float(r["lz_eegComplexity"]) - float(r["lz_antropy"])) < 1e-9 for r in bs.values()))
check("recorded max |diff| vs antropy is at machine precision (< 1e-12)", sm["max_abs_diff_vs_antropy"] < 1e-12)

# --- reference recovery: the consciousness gradient -------------------------
check("deep sleep N3 is the complexity MINIMUM", sm["lz_n3"] == min(sm["lz_n3"], sm["lz_wake"], sm["lz_n2"], sm["lz_rem"]))
check("wake complexity exceeds deep sleep (gradient > 0)", sm["wake_minus_n3"] > 0)
check("REM (dreaming) recovers toward wake (REM >= N2)", sm["lz_rem"] >= sm["lz_n2"])
check("N2 is intermediate (N3 < N2 < wake)", sm["lz_n3"] < sm["lz_n2"] < sm["lz_wake"] + 1e-9)
check("all four stages present", len(bs) == int(sm["n_stages"]) == 4)
check("all LZ values are valid (0 < LZ < 1)", all(0 < float(r["lz_eegComplexity"]) < 1 for r in bs.values()))

# --- honest scope -----------------------------------------------------------
check("HONEST: LZ is exactly-defined -> machine precision, extends the perm-entropy validation",
      "exactly" in case["validation"]["note"].lower() and "permutation-entropy" in case["validation"]["note"].lower())
check("HONEST: single subject, fixed-length per stage (demonstration not norm)",
      "single subject" in case["validation"]["note"].lower() and "fixed-length" in case["validation"]["note"].lower())
check("HONEST: cross-tool (antropy), not a self-comparison", "antropy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
