import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/rsa_mantel_summary.csv"))}
bs   = list(csv.DictReader(open("artifacts/rsa_mantel_by_subject.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("rsa_similarity traces", abs(sm["rsa_similarity"] - by["rsa_similarity"]["value"]) < 1e-9)
check("p_value traces",        abs(sm["p_value"]        - by["p_value"]["value"])        < 1e-9)
check("mantel_vegan traces",   abs(sm["mantel_vegan"]   - by["mantel_vegan"]["value"])   < 1e-9)
check("rsa_mean5 traces",      abs(sm["rsa_mean5"]      - by["rsa_mean5"]["value"])      < 1e-6)
check("rsa_min5 traces",       abs(sm["rsa_min5"]       - by["rsa_min5"]["value"])       < 1e-6)

# --- external cross-tool validation: representationalSimilarity == vegan::mantel
check("op == vegan::mantel to machine precision (|diff| < 1e-9)", abs(sm["rsa_similarity"] - sm["mantel_vegan"]) < 1e-9)
check("the recorded abs_diff is exactly 0 (machine precision)", sm["abs_diff"] < 1e-12)

# --- reference recovery: the true representational correspondence ------------
check("kinematics-kinetics representational correspondence is moderate (Mantel r > 0.3)", sm["rsa_similarity"] > 0.3)
check("the correspondence is significant (permutation p <= 0.05)", sm["p_value"] <= 0.05)
check("correspondence holds across ALL five subjects (min Mantel r > 0.3)", sm["rsa_min5"] > 0.3)
check("the per-subject artifact lists all five subjects", len(bs) == int(sm["n_subjects"]) == 5)
check("every subject's Mantel r traces to [min5, max5]",
      all(sm["rsa_min5"] - 1e-6 <= float(r["mantel_r"]) <= sm["rsa_max5"] + 1e-6 for r in bs))

# --- honest scope: RSA is more conservative than distance correlation -------
check("HONEST: RSA/Mantel (0.38) < distance correlation (0.72) noted (distinct measures)",
      "0.72" in case["proposition"] and "distance correlation" in case["validation"]["note"].lower())
check("HONEST: cross-tool (vegan::mantel), not a self-comparison", "vegan::mantel" in case["validation"]["reference"])
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
