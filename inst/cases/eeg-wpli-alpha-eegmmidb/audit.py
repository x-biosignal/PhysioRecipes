import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/wpli_summary.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("wpli traces",                abs(sm["wpli"]                - by["wpli"]["value"])                < 1e-9)
check("wpli_debiased traces",       abs(sm["wpli_debiased"]       - by["wpli_debiased"]["value"])       < 1e-9)
check("max_diff_scipy traces",      abs(sm["max_diff_scipy"]      - by["max_diff_scipy"]["value"])      < 1e-9)
check("wpli_indep_biased traces",   abs(sm["wpli_indep_biased"]   - by["wpli_indep_biased"]["value"])   < 1e-6)
check("wpli_indep_debiased traces", abs(sm["wpli_indep_debiased"] - by["wpli_indep_debiased"]["value"]) < 1e-6)
check("wpli_lagged traces",         abs(sm["wpli_lagged"]         - by["wpli_lagged"]["value"])         < 1e-6)

# --- cross-tool validation ---------------------------------------------------
check("op == scipy imaginary-cross-spectrum wPLI (agreement < 1e-2)", sm["max_diff_scipy"] < 1e-2)
check("scipy reproduces the op's wPLI + debiased per direction",
      abs(sm["wpli"] - sm["wpli_scipy"]) < 1e-2 and abs(sm["wpli_debiased"] - sm["wpli_debiased_scipy"]) < 1e-2)

# --- the debiasing demonstration (the key property) --------------------------
check("independent: BIASED wPLI is spuriously positive (> 0.01)", sm["wpli_indep_biased"] > 0.01)
check("independent: DEBIASED wPLI is corrected to ~0 (< 0.01)", sm["wpli_indep_debiased"] < 0.01)
check("debiasing REDUCES the spurious value (biased > debiased on independent)",
      sm["wpli_indep_biased"] > sm["wpli_indep_debiased"])
check("genuine lagged coupling survives debiasing (debiased wPLI > 0.9)", sm["wpli_lagged"] > 0.9)
check("zero-lag (volume conduction) stays ~0 (|debiased| < 0.1)", abs(sm["wpli_zerolag"]) < 0.1)

# --- reference recovery: the finding + the family story ----------------------
check("real O1-Oz debiased wPLI is low (< 0.1)", sm["wpli_debiased"] < 0.1)
check("consistent with the PLI case (both VC-robust measures ~0 while PLV is high)",
      sm["pli_real"] < 0.1 and sm["wpli_debiased"] < 0.1 and sm["plv_real"] > 0.7)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: scipy agreement is an AGREEMENT, NOT machine precision (filtfilt convention)",
      "agreement" in _note and "not machine precision" in _note and "filtfilt" in _note)
check("HONEST: the debiasing is the key validated property (removes spurious connectivity)",
      "debiasing is the key validated property" in _note and "spurious" in _note)
check("HONEST: the debiased estimator can go NEGATIVE (unbiased), not an error",
      "negative" in _note and "unbiased estimator" in _note)
check("HONEST: wPLI is conservative -- a low value is a lower bound on lagged interaction",
      "conservative" in _note and "lower bound" in _note)
check("HONEST: cross-tool reference (scipy), not a self-comparison",
      "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
