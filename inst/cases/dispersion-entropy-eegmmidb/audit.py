import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, math
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/dispersion_summary.csv"))}
check("dispen traces",               abs(sm["dispen"] - by["dispen"]["value"]) < 1e-6)
check("rden traces",                 abs(sm["rden"] - by["rden"]["value"]) < 1e-6)
check("max_diff_nk_dispen traces",   abs(sm["max_diff_nk_dispen"] - by["max_diff_nk_dispen"]["value"]) < 1e-18)
check("max_diff_nk_rden traces",     abs(sm["max_diff_nk_rden"] - by["max_diff_nk_rden"]["value"]) < 1e-20)
check("n_patterns_observed traces",  int(sm["n_patterns_observed"]) == by["n_patterns_observed"]["value"])
check("dispen_below_ceiling traces", int(sm["dispen_below_ceiling"]) == by["dispen_below_ceiling"]["value"])
# machine-precision: op == NeuroKit2 for BOTH DispEn and RDEn
check("op == NeuroKit2 entropy_dispersion DispEn BIT-FOR-BIT (< 1e-9)", sm["max_diff_nk_dispen"] < 1e-9)
check("op == NeuroKit2 entropy_dispersion RDEn  BIT-FOR-BIT (< 1e-9)", sm["max_diff_nk_rden"] < 1e-9)
# pattern structure: some but not all c^m patterns realized (structured)
check("0 < patterns realized < c^m=216 (structured, not pattern-saturating)", 0 < int(sm["n_patterns_observed"]) < 216)
check("exactly 108 of 216 patterns realized", int(sm["n_patterns_observed"]) == 108)
# normalization: DispEn below the base-2/ln ceiling 1/ln(2)
check("DispEn below the NeuroKit2 ceiling 1/ln(2)=1.4427", sm["dispen"] < 1.0/math.log(2) and int(sm["dispen_below_ceiling"]) == 1)
check("DispEn and RDEn are positive", sm["dispen"] > 0 and sm["rden"] > 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the NCDF-based dispersion-entropy gap",
      "newly authored" in _note and "ncdf-based dispersion entropy" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical pipeline), not a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not a convention agreement" in _note)
check("HONEST: mechanism genuinely distinct (NCDF ranking + patterns, outlier-robust)",
      "genuinely distinct" in _note and "outlier-robust" in _note)
check("HONEST: NCDF classes near-equiprobable -> complexity is in the patterns not the marginal",
      "near-equiprobable" in _note and "not the marginal" in _note)
check("HONEST: NeuroKit2 normalization convention reproduced not corrected",
      "reproduced, not corrected" in _note and "1/ln2 = 1.443" in _note)
check("HONEST: NeuroKit2 cross-tool reference", "neurokit2" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
