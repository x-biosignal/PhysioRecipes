import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/granger_summary.csv"))}
ms   = list(csv.DictReader(open("artifacts/granger_multisubject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("gc_resp_to_pleth traces",  abs(sm["gc_resp_to_pleth"] - by["gc_resp_to_pleth"]["value"]) < 1e-9)
check("gc_pleth_to_resp traces",  abs(sm["gc_pleth_to_resp"] - by["gc_pleth_to_resp"]["value"]) < 1e-9)
check("net_gc traces",            abs(sm["net_gc"]           - by["net_gc"]["value"])           < 1e-9)
check("max_diff_statsmodels traces", abs(sm["max_diff_statsmodels"] - by["max_diff_statsmodels"]["value"]) < 1e-9)
check("max_diff_numpy traces",       abs(sm["max_diff_numpy"]       - by["max_diff_numpy"]["value"])       < 1e-12)
check("n_subjects_resp_dominant traces",
      int(sm["n_subjects_resp_dominant"]) == by["n_subjects_resp_dominant"]["value"])

# --- external cross-tool validation: op == statsmodels + independent OLS ------
check("op == statsmodels grangercausalitytests (agreement < 1e-5, both directions)",
      sm["max_diff_statsmodels"] < 1e-5)
check("op == independent numpy OLS (op arithmetic, < 1e-7)", sm["max_diff_numpy"] < 1e-7)
check("statsmodels reproduces the op's GC per direction (resp->pulse)",
      abs(sm["gc_resp_to_pleth"] - sm["gc_resp_to_pleth_statsmodels"]) < 1e-5)
check("independent OLS reproduces the op's GC per direction (pulse->resp)",
      abs(sm["gc_pleth_to_resp"] - sm["gc_pleth_to_resp_numpy"]) < 1e-7)

# --- both directions significant (bidirectional coupling) --------------------
check("respiration -> pulse is strongly significant (F > 20, p < 1e-10)",
      sm["F_resp_to_pleth"] > 20 and sm["p_resp_to_pleth"] < 1e-10)
check("pulse -> respiration is strongly significant (F > 20, p < 1e-10)",
      sm["F_pleth_to_resp"] > 20 and sm["p_pleth_to_resp"] < 1e-10)

# --- reference recovery: the directed finding --------------------------------
check("BIDMC-01 net direction is respiration -> pulse (net_gc > 0)", sm["net_gc"] > 0)
check("respiration -> pulse is the net-dominant direction in the majority (>= 12/20)",
      int(sm["n_subjects_resp_dominant"]) >= 12 and int(sm["n_subjects_total"]) == 20)
# the multi-subject table itself carries n_subjects_resp_dominant positives
_pos = sum(1 for r in ms if float(r["net_gc"]) > 0)
check("the per-subject table has the claimed number of respiration->pulse-dominant subjects",
      _pos == int(sm["n_subjects_resp_dominant"]))
check("coupling is genuinely BIDIRECTIONAL (some subjects run the other way, 0 < pos < 20)",
      0 < _pos < int(sm["n_subjects_total"]))

# --- honest scope -----------------------------------------------------------
_note = case["validation"]["note"].lower()
check("HONEST: statsmodels agreement is NOT a machine-precision match (intercept convention)",
      "agreement" in _note and "not a machine-precision" in _note and "intercept" in _note)
check("HONEST: op arithmetic machine-precise vs an INDEPENDENT numpy OLS (ridge floor)",
      "independent" in _note and "ridge" in _note)
check("HONEST: coupling is bidirectional, not unidirectional causation",
      "bidirectional" in _note and "not a claim of unidirectional" in _note)
check("HONEST: Granger causality is predictive precedence, not physical cause",
      "predictive" in _note and "not proof of a physical causal" in _note)
check("HONEST: cross-tool reference (statsmodels), not a self-comparison",
      "statsmodels" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
