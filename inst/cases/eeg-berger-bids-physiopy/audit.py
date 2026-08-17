import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import csv
import json

ok = True


def check(label, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    ok = ok and bool(cond)


case = json.load(open("case.json"))
by = {cl["id"]: cl for cl in case["claims"]}
rows = {r["condition"]: float(r["occipital_alpha"])
        for r in csv.DictReader(open("artifacts/berger_summary.csv"))}
ec, eo = rows["eyes_closed"], rows["eyes_open"]


def close(a, b):
    return abs(a - b) <= abs(b) * 1e-9 + 1e-18


# claims trace to the artifact
check("alpha_ec traces to artifact", close(ec, by["alpha_ec"]["value"]))
check("alpha_eo traces to artifact", close(eo, by["alpha_eo"]["value"]))
# derived ratio matches the claim
check("berger_ratio == EC/EO", abs(ec / eo - by["berger_ratio"]["value"]) < 1e-3)
# the effect itself
check("Berger effect: eyes-closed alpha > eyes-open", ec > eo)

print("\n" + ("ALL TRACE" if ok else "AUDIT FAIL"))
raise SystemExit(0 if ok else 1)
