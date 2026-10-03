import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/mskn_summary.csv"))}
dd   = list(csv.DictReader(open("artifacts/mskn_degree_distribution.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("n_bones traces",   int(sm["n_bones"]) == by["n_bones"]["value"])
check("n_muscles traces", int(sm["n_muscles"]) == by["n_muscles"]["value"])
check("homunc_r2 traces", abs(sm["homunculus_r_squared"] - by["homunc_r2"]["value"]) < 1e-3)
check("homunc_f traces",  abs(sm["homunculus_f"] - by["homunc_f"]["value"]) < 1e-2)
check("homunc_n traces",  int(sm["homunculus_n"]) == by["homunc_n"]["value"])

# --- reference recovery: the paper's structure + finding --------------------
check("hypergraph is at the paper scale: 173 bones", int(sm["n_bones"]) == 173)
check("hypergraph is at the paper scale: 270 muscles", int(sm["n_muscles"]) == 270)
check("impact-homunculus R^2 matches the paper (0.52 +/- 0.05)", abs(sm["homunculus_r_squared"] - 0.52) < 0.05)
check("impact-homunculus F matches the paper (21.3 +/- 3)", abs(sm["homunculus_f"] - 21.3) < 3)
check("impact-homunculus correspondence is significant (p < 0.001)", sm["homunculus_p"] < 0.001)
check("homunculus correspondence over 21 body regions", int(sm["homunculus_n"]) == 21)

# --- honest scope: the recovery model direction holds but R^2 is lower ------
check("HONEST: recovery model reproduces a POSITIVE R^2 (direction holds)", sm["recovery_r_squared"] > 0)
check("HONEST: recovery R^2 is lower than the paper's 0.757 (documented boundary)", sm["recovery_r_squared"] < 0.757)

# --- the degree-distribution artifact is present + heavy-tailed --------------
kmax = len(dd) - 1
check("degree distribution spans a heavy tail (>= 15 degree bins)", kmax >= 15)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
