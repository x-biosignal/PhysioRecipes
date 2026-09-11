import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys, collections
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
BANDS = ["delta", "theta", "alpha", "sigma", "beta"]
STAGES = ["W", "N1", "N2", "N3", "REM"]

def sig(nm):
    return {r["stage"]: {b: float(r[f"rel_{b}"]) for b in BANDS} | {"n": int(r["n_epochs"])}
            for r in csv.DictReader(open(f"artifacts/stage_signature_{nm}.csv"))}
s1, s2 = sig("SC4001"), sig("SC4011")

# --- claims trace to the signature artifacts --------------------------------
check("n3_reldelta_s1 traces", abs(s1["N3"]["delta"] - by["n3_reldelta_s1"]["value"]) < 1e-3)
check("n3_reldelta_s2 traces", abs(s2["N3"]["delta"] - by["n3_reldelta_s2"]["value"]) < 1e-3)
check("deltarise_s1 traces",   abs((s1["N3"]["delta"] - s1["N1"]["delta"]) - by["deltarise_s1"]["value"]) < 2e-3)
check("n2_relsigma_s1 traces", abs(s1["N2"]["sigma"] - by["n2_relsigma_s1"]["value"]) < 1e-3)
check("n2_relsigma_s2 traces", abs(s2["N2"]["sigma"] - by["n2_relsigma_s2"]["value"]) < 1e-3)

# --- re-derive per-stage means from the aligned per-epoch table --------------
def rederive(nm):
    per = collections.defaultdict(list)
    for r in csv.DictReader(open(f"artifacts/epochs_{nm}.csv")):
        per[r["expert_stage"]].append([float(r[f"rel_{b}"]) for b in BANDS])
    out = {}
    for st, rows in per.items():
        out[st] = {b: sum(x[i] for x in rows) / len(rows) for i, b in enumerate(BANDS)}
        out[st]["n"] = len(rows)
    return out
for nm, tbl in (("SC4001", s1), ("SC4011", s2)):
    rd = rederive(nm)
    match = all(abs(rd[st][b] - tbl[st][b]) < 1e-3 for st in STAGES for b in BANDS)
    ncnt  = all(rd[st]["n"] == tbl[st]["n"] for st in STAGES)
    check(f"{nm}: per-stage means re-derive from aligned epochs", match and ncnt)

# --- the four canonical signatures hold in BOTH nights ----------------------
for nm, t in (("SC4001", s1), ("SC4011", s2)):
    check(f"{nm}: N3 has the highest relative delta of all stages",
          t["N3"]["delta"] == max(t[st]["delta"] for st in STAGES))
    check(f"{nm}: relative delta rises N1 < N2 < N3",
          t["N1"]["delta"] < t["N2"]["delta"] < t["N3"]["delta"])
    check(f"{nm}: relative beta falls N1 > N2 > N3",
          t["N1"]["beta"] > t["N2"]["beta"] > t["N3"]["beta"])
    check(f"{nm}: N2 has the highest relative sigma (spindle) of all stages",
          t["N2"]["sigma"] == max(t[st]["sigma"] for st in STAGES))

# --- honest scope: the classifier agreement is low and reported --------------
agr = {r["subject"]: float(r["classifier_agreement"]) for r in csv.DictReader(open("artifacts/staging_agreement.csv"))}
check("classifier agreement is honestly low (<0.20) in both nights",
      all(v < 0.20 for v in agr.values()))
check("open question flags the classifier limitation",
      "classifier" in case["open_questions"][0]["q"].lower())

# --- validated-tier invariants ----------------------------------------------
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
