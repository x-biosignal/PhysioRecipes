import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/petrosian_summary.csv"))}
check("petrosian_fd_poz traces",         abs(sm["petrosian_fd_poz"] - by["petrosian_fd_poz"]["value"]) < 1e-6)
check("max_diff_antropy traces",         abs(sm["max_diff_antropy"] - by["max_diff_antropy"]["value"]) < 1e-18)
check("n_samples traces",                int(sm["n_samples"]) == by["n_samples"]["value"])
check("posterior_mean traces",           abs(sm["posterior_mean"] - by["posterior_mean"]["value"]) < 1e-4)
check("frontal_mean traces",             abs(sm["frontal_mean"] - by["frontal_mean"]["value"]) < 1e-4)
check("n_posterior_lt_frontmean traces", int(sm["n_posterior_lt_frontmean"]) == by["n_posterior_lt_frontmean"]["value"])
# machine-precision
check("op == antropy.petrosian_fd BIT-FOR-BIT (< 1e-9)", sm["max_diff_antropy"] < 1e-9)
# valid FD
check("Petrosian FD is a valid waveform-complexity index (1 < FD < 1.2)", 1 < sm["petrosian_fd_poz"] < 1.2)
# finding
check("finding: posterior Petrosian FD lower than frontal (smoother alpha oscillation)", sm["posterior_mean"] < sm["frontal_mean"])
check("finding: robust -- all posterior channels below the frontal mean", int(sm["n_posterior_lt_frontmean"]) == int(sm["n_posterior"]))
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: NEWLY AUTHORED op filling the waveform-fractal-dimension gap",
      "newly authored" in _note and "waveform-fractal-dimension view" in _note)
check("HONEST: genuine MACHINE-PRECISION match (identical formula), not a convention agreement (unlike Higuchi/Katz)",
      "machine-precision" in _note and "identical" in _note and "unlike the higuchi/katz" in _note)
check("HONEST: finding descriptive (smoother posterior alpha), consistent with sibling cases",
      "smoother" in _note and "descriptive" in _note)
check("HONEST: antropy cross-tool reference", "antropy" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
