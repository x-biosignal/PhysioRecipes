import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)

case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
s    = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/fusion_summary.csv"))}

# --- claims trace to artifacts ----------------------------------------------
check("cca1 traces",          abs(s["cca_canonical_cor_1"]         - by["cca1"]["value"])          < 5e-3)
check("joint_speed_r traces", abs(s["jive_joint_score_vs_speed_r"] - by["joint_speed_r"]["value"]) < 5e-3)
check("joint_kin traces",     abs(s["jive_joint_kinematics"]       - by["joint_kin"]["value"])     < 5e-3)
check("joint_kinet traces",   abs(s["jive_joint_kinetics"]         - by["joint_kinet"]["value"])   < 5e-3)
check("rv traces",            abs(s["rv_coefficient"]              - by["rv"]["value"])            < 5e-3)
check("n_obs traces",         int(s["n_obs"])                      == by["n_obs"]["value"])

# --- reference recovery: strong coupling + speed-driven shared component -----
check("CCA finds strong kinematics-kinetics coupling (top cor > 0.7)", s["cca_canonical_cor_1"] > 0.7)
check("JIVE joint component tracks speed (|r| > 0.5)", abs(s["jive_joint_score_vs_speed_r"]) > 0.5)
check("both modalities carry a shared (joint) component (> 0.1)",
      s["jive_joint_kinematics"] > 0.1 and s["jive_joint_kinetics"] > 0.1)
check("RV is significant even though modest (p < 0.05)", s["rv_p"] < 0.05)
# the teaching point: CCA reveals far stronger coupling than the whole-block RV
check("CCA coupling >> whole-block RV (need more than RV)", s["cca_canonical_cor_1"] > 5 * s["rv_coefficient"])

# --- honest scope -----------------------------------------------------------
check("note is honest about GRF units / one belt", "units" in case["validation"]["note"].lower())
check("open question flags a full EMG+IMU 4-modality extension",
      any("EMG" in q["q"] and "IMU" in q["q"] for q in case["open_questions"]))

print("\nRESULT:", "PASS -- shared cross-modal structure recovered; every number traces" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
