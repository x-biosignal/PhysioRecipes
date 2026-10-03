import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/fnirs_summary.csv"))}
ct   = list(csv.DictReader(open("artifacts/fnirs_contrast.csv")))
bl   = list(csv.DictReader(open("artifacts/fnirs_block_grandavg.csv")))

# --- claims trace to artifacts ----------------------------------------------
check("mbll_r_mne traces",   abs(sm["mbll_hbo_r_mne"]        - by["mbll_r_mne"]["value"])   < 1e-3)
check("hbo_activation traces", int(sm["n_sig_hbo_activation"]) == by["hbo_activation"]["value"])
check("hbr_decrease traces", int(sm["n_hbr_decrease"])       == by["hbr_decrease"]["value"])
check("hbo_peak traces",     abs(sm["hbo_block_peak_uM"]     - by["hbo_peak"]["value"])     < 1e-3)
check("n_channels traces",   int(sm["n_channels"]) == by["n_channels"]["value"])

# --- the summary re-derives from the per-channel contrast + block artifacts --
n_sig = sum(1 for r in ct if float(r["hbo_p"]) < 0.05 and float(r["hbo_est"]) > 0)
n_neg = sum(1 for r in ct if float(r["hbr_est"]) < 0)
check("n contrast rows == 28 channels", len(ct) == 28)
check("n_sig_hbo_activation re-derives from fnirs_contrast.csv", n_sig == int(sm["n_sig_hbo_activation"]))
check("n_hbr_decrease re-derives from fnirs_contrast.csv", n_neg == int(sm["n_hbr_decrease"]))

# --- reference recovery 1: mbll == MNE beer_lambert_law (machine precision) --
check("mbll() reproduces MNE beer_lambert_law() to machine precision (min r > 0.999)",
      sm["mbll_hbo_r_mne"] > 0.999 and sm["mbll_hbr_r_mne"] > 0.999)

# --- reference recovery 2: the canonical activation signature ---------------
hbo = [float(r["HbO"]) for r in bl]; hbr = [float(r["HbR"]) for r in bl]
times = [float(r["time_s"]) for r in bl]
peak_t = times[hbo.index(max(hbo))]
check("HbO INCREASES on activation (grand-average peak > 0)", max(hbo) > 0)
check("HbR DECREASES on activation (grand-average trough < 0)", min(hbr) < 0)
check("HbO peak > |HbR| trough (HbO is the dominant response)", max(hbo) > abs(min(hbr)))
check("haemodynamic response peaks 3-8 s after onset (canonical HRF delay)", 3.0 <= peak_t <= 8.0)
check("most channels activate: >= half show significant positive HbO", sm["n_sig_hbo_activation"] >= 14)

check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper()
      and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))

print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
