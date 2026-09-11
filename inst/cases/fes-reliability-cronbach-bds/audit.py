import os as _os; _os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, csv, sys
ok = True
def check(l, c):
    global ok; print(f"  [{'PASS' if c else 'FAIL'}] {l}"); ok = ok and bool(c)
case = json.load(open("case.json"))
by   = {cl["id"]: cl for cl in case["claims"]}
sm   = {r["metric"]: float(r["value"]) for r in csv.DictReader(open("artifacts/cronbach_summary.csv"))}
# claims trace to the artifact
check("alpha traces", abs(sm["alpha"] - by["alpha"]["value"]) < 1e-6)
check("average_r traces", abs(sm["average_r"] - by["average_r"]["value"]) < 1e-6)
check("max_diff_psych traces (bit-for-bit, == 0)", sm["max_diff_psych"] == by["max_diff_psych"]["value"] == 0)
check("max_diff_pingouin traces (machine precision, < 1e-9)", abs(sm["max_diff_pingouin"] - by["max_diff_pingouin"]["value"]) < 1e-9)
check("good_reliability traces", int(sm["good_reliability"]) == by["good_reliability"]["value"])
check("k traces", int(sm["k"]) == by["k"]["value"])
check("n traces", int(sm["n"]) == by["n"]["value"])
# triple reference: psych bit-for-bit, pingouin machine precision
check("cronbachAlpha == psych::alpha raw_alpha BIT-FOR-BIT (|diff| == 0)", sm["max_diff_psych"] == 0)
check("cronbachAlpha == pingouin.cronbach_alpha to machine precision (< 1e-9)", sm["max_diff_pingouin"] < 1e-9)
# the finding: good internal consistency
check("alpha exceeds 0.8 (good internal consistency)", sm["alpha"] > 0.8 and int(sm["good_reliability"]) == 1)
check("alpha below 1 (sane reliability value)", sm["alpha"] < 1.0)
check("mean inter-item correlation is positive and moderate (0.15-0.6)", 0.15 < sm["average_r"] < 0.6)
check("7-item scale, 163 respondents", int(sm["k"]) == 7 and int(sm["n"]) == 163)
# honest scope
_note = case["validation"]["note"].lower()
check("HONEST: AUTHORS the new cronbachAlpha op (psychometrics)",
      "new op" in _note and "cronbachalpha" in _note and "psychometrics" in _note)
check("HONEST: psych::alpha raw_alpha bit-for-bit",
      "psych::alpha raw_alpha" in _note and "bit-for-bit" in _note)
check("HONEST: pingouin.cronbach_alpha to machine precision",
      "pingouin.cronbach_alpha" in _note and "machine precision" in _note)
check("HONEST: a self-report scale, not a physiological signal",
      "self-report scale, not a physiological signal" in _note)
check("HONEST: reliability (consistency) is NOT a validity claim",
      "not a validity claim" in _note)
check("HONEST: good internal consistency finding, justifies the summed FES score",
      "good internal consistency" in _note and "summed fes total" in _note)
check("HONEST: two-tool cross reference (psych + pingouin)",
      "psych::alpha" in case["validation"]["reference"].lower() and "pingouin.cronbach_alpha" in case["validation"]["reference"].lower())
check("validation REAL + all_pass", "REAL" in case["validation"]["data"].upper() and case["validation"]["all_pass"] is True)
check("not escalated", all(q.get("escalate") is None for q in case["open_questions"]))
print("\nRESULT:", "ALL TRACE" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
