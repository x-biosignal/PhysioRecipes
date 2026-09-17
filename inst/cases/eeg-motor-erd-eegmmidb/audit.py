import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, hashlib, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c

def chan(path):
    """{channel_label: {band: value}} from a terminal_table.csv."""
    out = {}
    for r in csv.DictReader(open(path)):
        out[r["channel"]] = {k: float(v) for k, v in r.items() if k != "channel"}
    return out

case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])

# --- primary bundle: S001 rest ----------------------------------------------
h = hashlib.sha256(open("bundle/prereg.json", "rb").read()).hexdigest()
check("prereg_hash traces", h == case["verification"]["prereg_hash"])
vr = {c["id"]: c for c in json.load(open("bundle/verification_report.json"))["claims"]}
for cl in case["claims"]:
    v = vr.get(cl["id"], {})
    check(f"claim {cl['id']} GROUNDED + value traces",
          v.get("status") == "GROUNDED" and abs(float(v.get("artifact", -9)) - cl["value"]) < 0.05)
check("n_grounded == n_claims == 5", len(case["claims"]) == 5 == case["verification"]["n_grounded"])

# --- per-subject ERD re-derived from terminals (mu = alpha band) ------------
erd = case["erd"]
n_mu = 0; n_beta = 0; mu_means = []
def erd_pct(move, rest):
    return (move - rest) / rest * 100.0
for s in erd["subjects"]:
    subj = s["subject"]
    rest = chan("bundle/terminal_table.csv" if subj == "S001" else f"artifacts/rest_{subj}_terminal.csv")
    move = chan(f"artifacts/move_{subj}_terminal.csv")
    mu_c3 = erd_pct(move["C3.."]["alpha"], rest["C3.."]["alpha"])
    mu_c4 = erd_pct(move["C4.."]["alpha"], rest["C4.."]["alpha"])
    be_c3 = erd_pct(move["C3.."]["beta"], rest["C3.."]["beta"])
    be_c4 = erd_pct(move["C4.."]["beta"], rest["C4.."]["beta"])
    mu_mean = (mu_c3 + mu_c4) / 2.0; be_mean = (be_c3 + be_c4) / 2.0
    check(f"{subj}: mu ERD (mean C3/C4) traces to terminals",
          abs(mu_mean - s["mu_ERD_pct"]) < 0.1)
    check(f"{subj}: beta ERD traces to terminals",
          abs(be_mean - s["beta_ERD_pct"]) < 0.1)
    check(f"{subj}: mu DESYNC during movement (ERD < 0)", (mu_mean < 0) == bool(s["mu_desync"]) and mu_mean < 0)
    check(f"{subj}: beta desync flag matches", (be_mean < 0) == bool(s["beta_desync"]))
    n_mu += int(mu_mean < 0); n_beta += int(be_mean < 0); mu_means.append(mu_mean)

check("n_mu_desync re-derived == case.json", n_mu == erd["n_mu_desync"])
check("n_beta_desync re-derived == case.json", n_beta == erd["n_beta_desync"])
check("all_mu_desync flag consistent (5/5 here)",
      (n_mu == erd["n_subjects"]) == bool(erd["all_mu_desync"]))
check("mean mu ERD traces (<0.2)", abs(sum(mu_means) / len(mu_means) - erd["mean_mu_ERD_pct"]) < 0.2)

# --- panel table + every run is a GROUNDED + replayable frozen run ----------
panel = {r["subject"]: r for r in csv.DictReader(open("artifacts/erd_panel.csv"))}
check("panel has all 5 subjects", len(panel) == erd["n_subjects"] == 5)
check("every panel row: mu_desync true", all(r["mu_desync"].upper() == "TRUE" for r in panel.values()))
sec = json.load(open("artifacts/secondary_runs.json"))
check("secondary_runs has all 10 runs", len(sec) == 10)
for name, r in sec.items():
    check(f"run {name}: replay byte-identical + 5/5 grounded + adheres",
          r["replay_byte_identical"] is True and r["prereg_adheres"] is True and
          r["n_grounded"] == r["n_claims"] == 5)

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
