import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
ag   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/agreement.csv"))}
ih   = list(csv.DictReader(open("artifacts/item_hierarchy.csv")))

# --- claims trace to the agreement / hierarchy artifacts ---------------------
check("item_spearman traces",      abs(ag["item_location_spearman_vs_erm"] - by["item_spearman"]["value"]) < 1e-3)
check("item_pearson traces",       abs(ag["item_location_pearson_vs_erm"]  - by["item_pearson"]["value"])  < 1e-3)
check("person_pearson traces",     abs(ag["person_measure_pearson_vs_erm"] - by["person_pearson"]["value"]) < 1e-3)
check("person_reliability traces", abs(ag["person_reliability"]            - by["person_reliability"]["value"]) < 1e-3)
check("n_items traces",            int(ag["n_items"])   == by["n_items"]["value"])
check("n_persons traces",          int(ag["n_persons"]) == by["n_persons"]["value"])

# --- hierarchy artifact is internally consistent ----------------------------
check("24 items in hierarchy",     len(ih) == 24 == int(ag["n_items"]))
locs = [float(r["location"]) for r in ih]
check("hierarchy sorted hardest-first", locs == sorted(locs, reverse=True))
check("locations centred (mean ~ 0)", abs(sum(locs) / len(locs)) < 1e-2)
# the substantive finding: a 'do-shout' item is hardest, a 'want-curse' easiest
check("hardest item is a 'DoShout'",  "DoShout" in ih[0]["item"])
check("easiest item is a 'WantCurse'", "WantCurse" in ih[-1]["item"])

# --- cross-tool agreement is genuinely high (real-data validation) ----------
check("item agreement >= 0.95",   ag["item_location_spearman_vs_erm"] >= 0.95 and ag["item_location_pearson_vs_erm"] >= 0.95)
check("person agreement >= 0.95", ag["person_measure_pearson_vs_erm"] >= 0.95)
check("reliability in (0, 1]",    0 < ag["person_reliability"] <= 1)

print("\nRESULT:", "PASS — every number traces and reproduces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
