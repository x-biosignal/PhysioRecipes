import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok=True
def check(l,c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
case=json.load(open("case.json"))
edge={r["method"]:float(r["split_half_edge_correlation"]) for r in csv.DictReader(open("artifacts/validation_split_half.csv"))}
node={r["method"]:float(r["split_half_node_strength_correlation"]) for r in csv.DictReader(open("artifacts/validation_topology_split_half.csv"))}
em={"coherence_edge_r":"coherence","partial_edge_r":"partial_coherence","wpli_edge_r":"wpli","gc_edge_r":"directed_gc"}
by={cl["id"]:cl for cl in case["claims"]}
for cid,meth in em.items():
    check(f"{cid} traces", abs(edge[meth]-by[cid]["value"])<1e-3)
check("coherence_node_r traces", abs(node["coherence"]-by["coherence_node_r"]["value"])<1e-3)
check("all claimed reproducibilities >= 0.83", all(cl["value"]>=0.83 for cl in case["claims"]))
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
