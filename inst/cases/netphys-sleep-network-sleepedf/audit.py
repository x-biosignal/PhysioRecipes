import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/netphys_summary.csv"))}
bs   = {r["stage"]: r for r in csv.DictReader(open("artifacts/netphys_network_by_stage.csv"))}
deg  = list(csv.DictReader(open("artifacts/netphys_node_degree.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("n_states traces",       int(sm["n_states"]) == by["n_states"]["value"])
check("rem_n_links traces",    int(sm["rem_n_links"]) == by["rem_n_links"]["value"])
check("rem_density traces",    abs(sm["rem_density"] - by["rem_density"]["value"]) < 1e-3)
check("wake_rem_reconfig traces", int(sm["wake_rem_links_changed"]) == by["wake_rem_reconfig"]["value"])
check("hub_is_delta traces",   int(sm["hub_node_is_delta"]) == by["hub_is_delta"]["value"])

# --- the summary re-derives from the per-stage + degree artifacts ------------
check("4 stages in the by-stage network table", len(bs) == 4 and set(bs) == {"Wake","Light","Deep","REM"})
check("rem_n_links matches the by-stage table", int(bs["REM"]["n_links"]) == int(sm["rem_n_links"]))
check("rem_density matches the by-stage table", abs(float(bs["REM"]["density"]) - sm["rem_density"]) < 1e-3)
# hub = node with the highest total degree across stages
node_cols = [c for c in deg[0].keys() if c != "stage"]
totals = {c: sum(float(r[c]) for r in deg) for c in node_cols}
hub = max(totals, key=totals.get)
check("hub (max total degree) is EEG_delta", hub == "EEG_delta")
check("hub total degree == artifact value", abs(totals["EEG_delta"] - sm["hub_total_degree"]) < 1e-6)

# --- reference recovery: the sleep-stage network RECONFIGURATION -------------
dens = {s: float(bs[s]["density"]) for s in bs}
check("REM is the MOST-integrated state (highest density)", dens["REM"] == max(dens.values()))
check("the network RECONFIGURES: density is not constant across stages",
      len(set(round(v, 3) for v in dens.values())) >= 2)
check("wake and REM link sets DIFFER (reconfiguration > 0)", int(sm["wake_rem_links_changed"]) > 0)
check("REM density > Wake density (state-dependent integration)", dens["REM"] > dens["Wake"])
check("the slow-wave delta rhythm is the hub (highest degree)", int(sm["hub_node_is_delta"]) == 1)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
