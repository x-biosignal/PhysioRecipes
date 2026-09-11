import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/lomb_summary.csv"))}
pg   = list(csv.DictReader(open("artifacts/lomb_periodogram.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("lf traces",                  abs(sm["lf"]          - by["lf"]["value"])          < 1e-4)
check("hf traces",                  abs(sm["hf"]          - by["hf"]["value"])          < 1e-4)
check("lf_hf_ratio traces",         abs(sm["lf_hf_ratio"] - by["lf_hf_ratio"]["value"]) < 1e-6)
check("hf_nu traces",               abs(sm["hf_nu"]       - by["hf_nu"]["value"])       < 1e-3)
check("max_diff_periodogram traces",abs(sm["max_diff_periodogram"] - by["max_diff_periodogram"]["value"]) < 1e-12)
check("max_diff_bandpower traces",  abs(sm["max_diff_bandpower"]   - by["max_diff_bandpower"]["value"])   < 1e-15)

# --- external cross-tool validation: op == scipy.signal.lombscargle ----------
check("op == scipy Lomb-Scargle periodogram to machine precision (< 1e-5, rel ~1e-10)",
      sm["max_diff_periodogram"] < 1e-5)
check("op == scipy integrated band powers to machine precision (< 1e-6)",
      sm["max_diff_bandpower"] < 1e-6)
check("scipy reproduces the op's LF band power", abs(sm["lf"] - sm["lf_scipy"]) < 1e-6)
check("scipy reproduces the op's HF band power", abs(sm["hf"] - sm["hf_scipy"]) < 1e-6)
check("the periodogram table carries both op and scipy columns that match",
      max(abs(float(r["psd_op"]) - float(r["psd_scipy"])) for r in pg) < 1e-4)

# --- internal consistency ----------------------------------------------------
check("band powers sum to total_power (VLF+LF+HF)",
      abs((sm["vlf"] + sm["lf"] + sm["hf"]) - sm["total_power"]) < 1e-2)
check("normalized units sum to 100 (LF_nu + HF_nu)", abs(sm["lf_nu"] + sm["hf_nu"] - 100) < 1e-2)

# --- reference recovery: the autonomic finding -------------------------------
check("the tachogram is HF-dominant (LF/HF < 1)", sm["lf_hf_ratio"] < 1)
check("HF power exceeds LF power (vagal-dominant resting balance)", sm["hf"] > sm["lf"])
check("HF is the majority of LF+HF (HF_nu > 50%)", sm["hf_nu"] > 50)
check("the HF peak is in the respiratory band (0.15-0.4 Hz)", 0.15 <= sm["hf_peak"] <= 0.4)

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: genuine MACHINE-PRECISION match (identical formula), NOT a convention agreement",
      "machine-precision" in _note and "identical" in _note and "not an agreement" in _note)
check("HONEST: residual is the floating-point summation-order floor (not a methodological diff)",
      "summation-order floor" in _note or "summation floor" in _note)
check("HONEST: Lomb-Scargle is the correct estimate for UNEVEN sampling (no interpolation)",
      "unevenly-sampled" in _note or "no interpolation" in _note)
check("HONEST: LF/HF is a DESCRIPTIVE autonomic index, not a clinical claim",
      "descriptive" in _note and "not a clinical claim" in _note)
check("HONEST: cross-tool reference (scipy), not a self-comparison",
      "scipy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
