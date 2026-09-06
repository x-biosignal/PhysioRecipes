import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/tep_summary.csv"))}
cs   = list(csv.DictReader(open("artifacts/tep_component_summary.csv")))
comp = list(csv.DictReader(open("artifacts/tep_components.csv")))

CANON = ["N15", "P30", "N45", "P60", "N100", "P180"]

# --- claims trace to artifacts ----------------------------------------------
check("n_components traces",    int(sm["n_components"]) == by["n_components"]["value"])
check("n100_latency traces",    abs(sm["n100_median_latency_ms"] - by["n100_latency"]["value"]) < 1)
check("p180_latency traces",    abs(sm["p180_median_latency_ms"] - by["p180_latency"]["value"]) < 1)
check("canonical_order traces", int(sm["latency_order_canonical"]) == by["canonical_order"]["value"])
check("polarity_match traces",  abs(sm["mean_polarity_match_pct"] - by["polarity_match"]["value"]) < 0.1)

# --- the summary re-derives from the component-summary artifact --------------
rows = {r["component"]: r for r in cs}
check("all six canonical components present", set(rows) == set(CANON))
lat = [float(rows[c]["median_latency_ms"]) for c in CANON]
check("component latencies are monotonically increasing (canonical order)", all(b > a for a, b in zip(lat, lat[1:])))
check("latency_order_canonical == 1 iff monotonic", int(sm["latency_order_canonical"]) == int(all(b > a for a, b in zip(lat, lat[1:]))))
mean_match = sum(float(rows[c]["polarity_match_pct"]) for c in CANON) / 6
check("mean polarity-match re-derives from the component summary", abs(mean_match - sm["mean_polarity_match_pct"]) < 0.5)

# --- reference recovery: the canonical TEP structure ------------------------
check("N100 is negative-polarity in the summary", rows["N100"]["polarity"] == "negative")
check("P180 is positive-polarity in the summary", rows["P180"]["polarity"] == "positive")
check("N100 median latency is in the canonical 85-140 ms range", 85 <= float(rows["N100"]["median_latency_ms"]) <= 140)
check("P180 median latency is in the canonical 150-220 ms range", 150 <= float(rows["P180"]["median_latency_ms"]) <= 220)
check("every component matches its expected polarity in a MAJORITY of channels (>80%)",
      all(float(rows[c]["polarity_match_pct"]) > 80 for c in CANON))
check("component table has 6 components x 59 channels = 354 rows", len(comp) == 6 * 59)
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
