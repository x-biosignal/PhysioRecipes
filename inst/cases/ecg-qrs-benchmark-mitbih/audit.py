import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and c

case = json.load(open("case.json"))
print("case", case["id"], "| status", case["status"])
rows = list(csv.DictReader(open("artifacts/qrs_benchmark.csv")))
per = [r for r in rows if r["record"] != "GROSS"]
gross = [r for r in rows if r["record"] == "GROSS"][0]

def f(r, k): return float(r[k])
def i(r, k): return int(r[k])

# --- per-record metric identities re-derived from TP/FP/FN -------------------
for r in per:
    tp, fp, fn = i(r, "TP"), i(r, "FP"), i(r, "FN")
    se = tp / (tp + fn); ppv = tp / (tp + fp); f1 = 2 * tp / (2 * tp + fp + fn)
    check(f"rec {r['record']}: Se/PPV/F1 re-derive from TP/FP/FN",
          abs(se - f(r, "Se")) < 5e-4 and abs(ppv - f(r, "PPV")) < 5e-4 and abs(f1 - f(r, "F1")) < 5e-4)
    check(f"rec {r['record']}: n_ref == TP + FN (every ref beat matched or missed)",
          i(r, "n_ref") == tp + fn)
check("8 records scored", len(per) == 8)

# --- GROSS row = pooled sums, metrics re-derived ----------------------------
gtp = sum(i(r, "TP") for r in per); gfp = sum(i(r, "FP") for r in per); gfn = sum(i(r, "FN") for r in per)
check("GROSS TP/FP/FN == sum over records", i(gross, "TP") == gtp and i(gross, "FP") == gfp and i(gross, "FN") == gfn)
gse = gtp / (gtp + gfn); gppv = gtp / (gtp + gfp); gf1 = 2 * gtp / (2 * gtp + gfp + gfn)
check("GROSS Se/PPV/F1 re-derive", abs(gse - f(gross, "Se")) < 5e-4 and abs(gppv - f(gross, "PPV")) < 5e-4 and abs(gf1 - f(gross, "F1")) < 5e-4)

# --- claims trace to the GROSS row ------------------------------------------
cl = {c["id"]: c["value"] for c in case["claims"]}
check("claim gross_se traces to GROSS row", abs(cl["gross_se"] - f(gross, "Se")) < 5e-4)
check("claim gross_ppv traces to GROSS row", abs(cl["gross_ppv"] - f(gross, "PPV")) < 5e-4)
check("claim gross_f1 traces to GROSS row", abs(cl["gross_f1"] - f(gross, "F1")) < 5e-4)

# --- acceptance + honesty ---------------------------------------------------
check("all_pass == (pooled Se,PPV,F1 all >= 0.95)",
      case["validation"]["all_pass"] == (gse >= 0.95 and gppv >= 0.95 and gf1 >= 0.95))
worst = min(per, key=lambda r: f(r, "F1"))
check("noisiest record reported (degradation not hidden; worst F1 < 0.95)", f(worst, "F1") < 0.95)
check("worst record in case.json matches the table",
      case["benchmark"]["worst_record"]["record"] == worst["record"] and
      abs(case["benchmark"]["worst_record"]["F1"] - f(worst, "F1")) < 5e-4)

# --- ground-truth beat counts match n_ref -----------------------------------
ref = json.load(open("artifacts/ref_beats.json"))
for r in per:
    check(f"rec {r['record']}: n_ref == len(ref_beats.json beats)",
          i(r, "n_ref") == len(ref[r["record"]]["beats"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
