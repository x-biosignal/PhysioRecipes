import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/cohort_summary.csv"))}

# --- claims trace to the artifact -------------------------------------------
check("n_subjects traces",      int(s["n_subjects"])          == by["n_subjects"]["value"])
check("n_recordings traces",    int(s["n_obs"])               == by["n_recordings"]["value"])
check("fixef_agreement traces", abs(s["max_abs_fixef_diff"]   - by["fixef_agreement"]["value"]) < 1e-6)
check("ranef_sd traces",        abs(s["ranef_sd_lme4"]        - by["ranef_sd"]["value"])        < 0.01)
check("beta_testtime traces",   abs(s["beta_testtime"]        - by["beta_testtime"]["value"])   < 5e-4)
check("cohort_n traces",        int(s["cohort_n_subjects"])   == by["cohort_n"]["value"])

# --- reference recovery: exact reference-engine (lme4) reproduction ----------
check("fitMixedModel reproduces lme4 fixed effects (max abs diff < 1e-6)", s["max_abs_fixef_diff"] < 1e-6)
check("random-intercept SD identical to lme4 (physio == lme4)", abs(s["ranef_sd_lme4"] - s["ranef_sd_physio"]) < 1e-6)
check("random-intercept SD is a sensible UPDRS spread (5-20 points)", 5 < s["ranef_sd_lme4"] < 20)
check("total UPDRS progresses over time (test_time slope > 0)", s["beta_testtime"] > 0)
check("PhysioCohort built the full 42-subject container", int(s["cohort_n_subjects"]) == 42)
check("cohort size matches the recording table (both 42 subjects)", int(s["cohort_n_subjects"]) == int(s["n_subjects"]))

# --- honest scope: public longitudinal-patient-cohort ceiling ---------------
check("open question flags the DUA-gated / public-ceiling limitation",
      any(("DUA" in q["q"]) or ("public" in q["q"]) for q in case["open_questions"]))

print("\nRESULT:", "PASS -- reference-engine reproduction on a real longitudinal patient cohort; every number traces"
      if ok else "FAIL")
raise SystemExit(0 if ok else 1)
