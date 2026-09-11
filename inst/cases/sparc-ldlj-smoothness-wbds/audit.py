import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/sparc_summary.csv"))}
for k in ("sparc","ldlj","sparc_noisy"):
    check(f"{k} traces", abs(sm[k] - by[k]["value"]) < 1e-6)
check("max_diff_sparc traces", abs(sm["max_diff_sparc"] - by["max_diff_sparc"]["value"]) < 1e-15)
check("max_diff_ldlj traces",  abs(sm["max_diff_ldlj"] - by["max_diff_ldlj"]["value"]) < 1e-15)
check("noise_reduces_smoothness traces", int(sm["noise_reduces_smoothness"]) == by["noise_reduces_smoothness"]["value"])
check("n_samples traces", int(sm["n_samples"]) == by["n_samples"]["value"])
# bit-exact vs Balasubramanian
check("sparc == Balasubramanian reference BIT-FOR-BIT (< 1e-9)", sm["max_diff_sparc"] < 1e-9)
check("ldlj == Balasubramanian reference BIT-FOR-BIT (< 1e-9)", sm["max_diff_ldlj"] < 1e-9)
check("op equals reference (sparc == ref_sparc, ldlj == ref_ldlj)",
      abs(sm["sparc"] - sm["ref_sparc"]) < 1e-9 and abs(sm["ldlj"] - sm["ref_ldlj"]) < 1e-9)
# construct check: noise reduces smoothness (SPARC more negative)
check("adding noise makes SPARC more negative (detects reduced smoothness)", sm["sparc_noisy"] < sm["sparc"])
check("noise_reduces_smoothness flag set", int(sm["noise_reduces_smoothness"]) == 1)
check("SPARC and LDLJ are negative (as smoothness metrics are)", sm["sparc"] < 0 and sm["ldlj"] < 0)
check("walking-speed / smoothness correlation is negative (faster tends less smooth)", sm["speed_smoothness_corr"] < 0)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: CROSS-TOOL AUDIT of shipped ops (not new ops)",
      "cross-tool audit" in _note and "shipped" in _note and "not new ops" in _note)
check("HONEST: bit-for-bit vs the canonical Balasubramanian reference, not a convention agreement",
      "balasubramanian" in _note and "bit-for-bit" in _note and "identical deterministic closed forms" in _note)
check("HONEST: the construct check (noise makes SPARC more negative / detects reduced smoothness)",
      "construct check" in _note and "more negative" in _note and "reduced smoothness" in _note)
check("HONEST: the time-normalized / nominal-fs caveat",
      "time-normalized" in _note and "nominal" in _note)
check("HONEST: Balasubramanian reference tool cited", "balasubramanian" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
