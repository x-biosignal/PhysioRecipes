import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pli_summary.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("pli traces",            abs(sm["pli"]            - by["pli"]["value"])            < 1e-9)
check("max_diff_scipy traces", abs(sm["max_diff_scipy"] - by["max_diff_scipy"]["value"]) < 1e-9)
check("formula_diff traces",   abs(sm["formula_diff"]   - by["formula_diff"]["value"])   < 1e-15)
check("plv_zerolag traces",    abs(sm["plv_zerolag"]    - by["plv_zerolag"]["value"])    < 1e-6)
check("pli_zerolag traces",    abs(sm["pli_zerolag"]    - by["pli_zerolag"]["value"])    < 1e-6)
check("pli_lagged traces",     abs(sm["pli_lagged"]     - by["pli_lagged"]["value"])     < 1e-6)

# --- three-way validation ----------------------------------------------------
check("op == scipy Hilbert-band PLI (agreement < 1e-2)", sm["max_diff_scipy"] < 1e-2)
check("PLI sign formula is exact (< 1e-9)", sm["formula_diff"] < 1e-9)

# --- the volume-conduction contrast (the key demonstration) ------------------
check("zero-lag: PLV counts it (PLV > 0.9)", sm["plv_zerolag"] > 0.9)
check("zero-lag: PLI DISCOUNTS it (PLI < 0.1)", sm["pli_zerolag"] < 0.1)
check("PLI separates zero-lag from lagged (lagged PLI > 0.9)", sm["pli_lagged"] > 0.9)
check("independent: both PLV and PLI ~0 (< 0.1)", sm["plv_independent"] < 0.1 and sm["pli_independent"] < 0.1)

# --- reference recovery: the real-data finding ------------------------------
check("real O1-Oz PLV is high (> 0.7)", sm["plv_real"] > 0.7)
check("real O1-Oz PLI is far below its PLV (< 0.1) -- mostly volume conduction", sm["pli"] < 0.1)
check("real coupling is dominated by the zero-lag component (PLV - PLI > 0.7)",
      sm["plv_real"] - sm["pli"] > 0.7)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: scipy agreement is an AGREEMENT, NOT machine precision (filtfilt + sign-sensitivity)",
      "agreement" in _note and "not machine precision" in _note and "sign() is more sensitive" in _note)
check("HONEST: anchored on the EXACT sign formula + ground-truth contrast",
      "exact sign formula" in _note and "ground-truth contrast" in _note)
check("HONEST: PLI is CONSERVATIVE -- a low PLI is a lower bound, not proof of no coupling",
      "conservative" in _note and "lower bound" in _note and "does not prove" in _note)
check("HONEST: descriptive, not a clinical claim -- wait, it's a methodological demonstration",
      "descriptive" in _note)
check("HONEST: cross-tool reference (scipy), not a self-comparison",
      "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
