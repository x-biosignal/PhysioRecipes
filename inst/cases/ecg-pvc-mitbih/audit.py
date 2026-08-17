import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
per  = list(csv.DictReader(open("artifacts/pvc_per_record.csv")))
pool = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/pvc_pooled.csv"))}
ref  = json.load(open("artifacts/ref_pvc.json"))

def f1(se, ppv): return 2*se*ppv/(se+ppv) if (se+ppv) > 0 else 0.0

# --- per-record metric identities: Se=TP/(TP+FN), PPV=TP/(TP+FP), F1 ---------
for r in per:
    TP, FP, FN = int(r["TP"]), int(r["FP"]), int(r["FN"])
    se  = TP/(TP+FN) if TP+FN else 0.0
    ppv = TP/(TP+FP) if TP+FP else 0.0
    ok_row = (abs(se - float(r["sensitivity"])) < 1e-3 and
              abs(ppv - float(r["ppv"])) < 1e-3 and
              abs(f1(se, ppv) - float(r["f1"])) < 1e-3)
    check(f"record {r['record']}: Se/PPV/F1 identities hold", ok_row)

# --- n_pvc per record matches the ground-truth ref_pvc.json ------------------
for r in per:
    check(f"record {r['record']}: n_pvc matches .atr ground truth",
          int(r["n_pvc"]) == ref[r["record"]]["n_pvc"] == sum(ref[r["record"]]["is_pvc"]))

# --- pooled = micro-average over all beats -----------------------------------
TP = sum(int(r["TP"]) for r in per); FP = sum(int(r["FP"]) for r in per); FN = sum(int(r["FN"]) for r in per)
se, ppv = TP/(TP+FN), TP/(TP+FP)
check("pooled TP/FP/FN sum from per-record", TP == pool["TP"] and FP == pool["FP"] and FN == pool["FN"])
check("pooled sensitivity is the micro-average", abs(se  - pool["pooled_sensitivity"]) < 1e-3)
check("pooled ppv is the micro-average",         abs(ppv - pool["pooled_ppv"]) < 1e-3)
check("pooled f1 is the micro-average",          abs(f1(se, ppv) - pool["pooled_f1"]) < 1e-3)

# --- claims trace ------------------------------------------------------------
check("pooled_ppv claim traces",         abs(pool["pooled_ppv"]         - by["pooled_ppv"]["value"])         < 1e-3)
check("pooled_sensitivity claim traces", abs(pool["pooled_sensitivity"] - by["pooled_sensitivity"]["value"]) < 1e-3)
check("pooled_f1 claim traces",          abs(pool["pooled_f1"]          - by["pooled_f1"]["value"])          < 1e-3)
best  = max(per, key=lambda r: float(r["f1"]))
worst = min(per, key=lambda r: float(r["sensitivity"]))
check("isolated_f1 claim = best-record F1",       abs(float(best["f1"])          - by["isolated_f1"]["value"])      < 1e-3)
check("runs_sensitivity claim = worst-record Se", abs(float(worst["sensitivity"]) - by["runs_sensitivity"]["value"]) < 1e-3)

# --- the honest headline: precise (high PPV) but recall pattern-dependent -----
check("precision high: pooled PPV >= 0.90 (acceptance criterion)", pool["pooled_ppv"] >= 0.90)
check("per-record PPV >= 0.99 on all but the noisiest record 203",
      all(float(r["ppv"]) >= 0.99 for r in per if r["record"] != "203"))
ses = [float(r["sensitivity"]) for r in per]
check("recall is pattern-dependent (spans a perfect 1.0 down to < 0.30)",
      max(ses) >= 0.999 and min(ses) < 0.30)
check("open question names the run-type blind spot",
      "run" in case["open_questions"][0]["q"].lower())

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
