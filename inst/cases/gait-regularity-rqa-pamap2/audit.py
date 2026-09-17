import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/regularity_summary.csv"))}
tab  = {r["activity"]: r for r in csv.DictReader(open("artifacts/regularity_table.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("walk_det traces",  abs(s["walking_DET"]  - by["walk_det"]["value"])  < 5e-3)
check("walk_apen traces", abs(s["walking_ApEn"] - by["walk_apen"]["value"]) < 5e-3)
check("iron_det traces",  abs(s["ironing_DET"]  - by["iron_det"]["value"])  < 5e-3)
check("iron_apen traces", abs(s["ironing_ApEn"] - by["iron_apen"]["value"]) < 5e-3)
check("run_det traces",   abs(s["running_DET"]  - by["run_det"]["value"])   < 5e-3)

# --- reference recovery: locomotion is deterministic & regular; ironing is not
check("walking is highly deterministic (DET > 0.85)", s["walking_DET"] > 0.85)
check("running is highly deterministic (DET > 0.9)", s["running_DET"] > 0.9)
check("ironing is much less deterministic (DET < 0.6)", s["ironing_DET"] < 0.6)
check("walking is far more deterministic than ironing (gap > 0.3)",
      s["walking_DET"] - s["ironing_DET"] > 0.3)
check("walking is more regular than ironing (lower ApEn)", s["walking_ApEn"] < s["ironing_ApEn"])
check("the entropy gap iron-walk is substantial (> 0.5)",
      s["ironing_ApEn"] - s["walking_ApEn"] > 0.5)
# sample entropy agrees with approximate entropy (walking << ironing)
check("sample entropy separates walking from ironing",
      float(tab["walking"]["SampEn"]) < float(tab["ironing"]["SampEn"]))

# --- honest scope -----------------------------------------------------------
check("open question distinguishes Floquet/DFA (needs multi-stride data)",
      any("Floquet" in q["q"] or "DFA" in q["q"] for q in case["open_questions"]))

print("\nRESULT:", "PASS -- rhythm regularity separated; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
