import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/eeg_aperiodic_summary.csv"))}
bc   = list(csv.DictReader(open("artifacts/eeg_aperiodic_by_channel.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("exp_corr traces",           abs(sm["exp_corr"]           - by["exp_corr"]["value"])           < 1e-6)
check("mean_abs_exp_diff traces",  abs(sm["mean_abs_exp_diff"]  - by["mean_abs_exp_diff"]["value"])  < 1e-6)
check("mean_exp_specparam traces", abs(sm["mean_exp_specparam"] - by["mean_exp_specparam"]["value"]) < 1e-6)
check("mean_exp_fooof traces",     abs(sm["mean_exp_fooof"]     - by["mean_exp_fooof"]["value"])     < 1e-6)
check("n_channels traces",         int(sm["n_channels"])        == by["n_channels"]["value"])

# --- reference recovery: eegAperiodic reproduces the canonical fooof ---------
check("strong cross-tool agreement (exp corr >= 0.95)", sm["exp_corr"] >= 0.95)
check("small mean |exponent diff| (<= 0.1)", sm["mean_abs_exp_diff"] <= 0.1)
check("specparam mean exponent physiologically plausible (0.8-2.0)", 0.8 < sm["mean_exp_specparam"] < 2.0)
check("fooof mean exponent physiologically plausible (0.8-2.0)", 0.8 < sm["mean_exp_fooof"] < 2.0)
check("good aperiodic fits (mean R^2 >= 0.9)", sm["mean_r2"] >= 0.9)
check("all 64 channels parameterized", int(sm["n_channels"]) == 64 and len(bc) == 64)

# --- per-channel artifact is consistent with the summary --------------------
diffs = [abs(float(r["exp_specparam"]) - float(r["exp_fooof"])) for r in bc]
check("per-channel |diff| max traces to the summary", abs(max(diffs) - sm["max_abs_exp_diff"]) < 1e-4)
check("clean central channels agree tightly (C3, Cz < 0.05)",
      all(abs(float(r["exp_specparam"]) - float(r["exp_fooof"])) < 0.05
          for r in bc if r["channel"] in ("C3", "Cz")))

# --- honest scope -----------------------------------------------------------
check("HONEST: agreement benchmark, not byte identity (systematic offset noted)",
      sm["mean_exp_specparam"] != sm["mean_exp_fooof"] and "offset" in case["validation"]["note"].lower())
check("HONEST: only a few channels diverge (<= 6 with |diff| > 0.15)", sm["n_ch_diff_gt_0.15"] <= 6)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("validation names fooof as the reference", "fooof" in case["validation"]["reference"].lower())
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
