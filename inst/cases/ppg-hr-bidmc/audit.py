import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, statistics
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
per  = list(csv.DictReader(open("artifacts/ppg_ecg_per_record.csv")))
agr  = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/ppg_ecg_agreement.csv"))}

# --- per-record diff identity: diff == ppg_pr - ecg_hr (each rounded to 2 dp) -
check("per-record diff == ppg_pr - ecg_hr (within double-rounding)",
      all(abs(float(r["diff"]) - (float(r["ppg_pr"]) - float(r["ecg_hr"]))) < 3e-2 for r in per))

# --- objective ECG-reference validity flag (ecg_hr in [40,180]) --------------
valid = [r for r in per if 40 <= float(r["ecg_hr"]) <= 180]
failed = [r for r in per if not (40 <= float(r["ecg_hr"]) <= 180)]
check("n_records_total matches file", len(per) == int(agr["n_records_total"]))
check("exactly the ecg_valid flag partitions the records",
      all((r["ecg_valid"].upper() == "TRUE") == (40 <= float(r["ecg_hr"]) <= 180) for r in per))
check("n_ecg_detection_failures matches", len(failed) == int(agr["n_ecg_detection_failures"]))
check("n_records_valid matches", len(valid) == int(agr["n_records_valid"]))
check("the one excluded record has an implausibly low ECG rate (< 40 bpm)",
      len(failed) == 1 and float(failed[0]["ecg_hr"]) < 40)

# --- re-derive Bland-Altman stats on the VALID records -----------------------
d = [float(r["diff"]) for r in valid]
bias = statistics.mean(d); sdd = statistics.stdev(d)
mae  = statistics.mean(abs(x) for x in d)
w5   = 100 * sum(1 for x in d if abs(x) <= 5) / len(d)
check("mean bias re-derives",  abs(bias - agr["mean_bias_bpm"]) < 1e-2)
check("sd of diff re-derives", abs(sdd - agr["sd_diff_bpm"]) < 1e-2)
check("lower LoA = bias - 1.96*sd", abs((bias - 1.96*sdd) - agr["loa_lower_bpm"]) < 5e-2)
check("upper LoA = bias + 1.96*sd", abs((bias + 1.96*sdd) - agr["loa_upper_bpm"]) < 5e-2)
check("MAE re-derives",        abs(mae - agr["mae_bpm"]) < 1e-2)
check("pct within 5 bpm re-derives", abs(w5 - agr["pct_within_5bpm"]) < 1e-1)

# --- claims trace ------------------------------------------------------------
check("pearson_r claim traces", abs(agr["pearson_r"]     - by["pearson_r"]["value"]) < 1e-3)
check("mean_bias claim traces", abs(agr["mean_bias_bpm"] - by["mean_bias"]["value"]) < 1e-2)
check("loa_lower claim traces", abs(agr["loa_lower_bpm"] - by["loa_lower"]["value"]) < 1e-2)
check("loa_upper claim traces", abs(agr["loa_upper_bpm"] - by["loa_upper"]["value"]) < 1e-2)
check("within5 claim traces",   abs(agr["pct_within_5bpm"] - by["within5"]["value"]) < 1e-1)

# --- acceptance: MAE <= 5 and >= 85% within 5 bpm ----------------------------
check("acceptance: MAE <= 5 bpm", agr["mae_bpm"] <= 5.0)
check("acceptance: >= 85% within 5 bpm", agr["pct_within_5bpm"] >= 85.0)
check("open question / note flags the excluded ECG-failure record",
      "bidmc03" in case["validation"]["note"])

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
