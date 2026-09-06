#!/usr/bin/env python3
"""Validate a PhysioRecipes case against the SCHEMA.md invariants.

Generic, dataset-agnostic gate (run in CI on every case). Tier-aware:

  common:
    - case.json valid with the required fields
    - the dataset is public
    - status is one of draft / verified / validated
    - EMBARGO: a public case must NOT escalate an open question to a paper
      (unresolved -> paper cases stay private in recipes-embargo/)

  status == "verified":
    - a substrate bundle exists; prereg_hash == sha256(bundle/prereg.json)
    - every claim is GROUNDED in bundle/verification_report.json and its value
      matches the verified artifact value
    - n_grounded == n_claims == number of grounded claims
    - replay_byte_identical is true

  status == "validated":
    - a validation block cites REAL public data and a reference comparator
    - validation.all_pass is true; there are claims

Per-case number tracing (cross-tool tables, reference recovery) lives in each
case's own audit.py; this file enforces the shared invariants.

Usage: python3 tools/validate_case.py cases/<id>   (exit 0 = pass, 1 = fail)
"""
import json, hashlib, os, sys

def main(case_dir):
    ok = True
    def check(label, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        ok = ok and bool(cond)

    cj = os.path.join(case_dir, "case.json")
    if not os.path.exists(cj):
        print(f"  [FAIL] {cj} missing"); return 1
    case = json.load(open(cj))
    status = case.get("status")
    print(f"case {case.get('id')} | status = {status}")

    for f in ("id", "title", "dataset", "proposition", "opdag", "claims", "status"):
        check(f"required field: {f}", f in case)
    check("id matches directory", case.get("id") == os.path.basename(case_dir.rstrip("/")))
    check("dataset is public", case.get("dataset", {}).get("public") is True)
    check("status is valid", status in ("draft", "verified", "validated"))
    check("claims present", len(case.get("claims", [])) > 0)

    # EMBARGO: no public case may escalate an unresolved question to a paper.
    escalated = [q for q in case.get("open_questions", []) if q.get("escalate")]
    check("not escalated (embargo keeps unresolved->paper cases private)", len(escalated) == 0)

    if status == "validated":
        v = case.get("validation", {})
        check("validated case has a validation block", bool(v))
        check("validation cites REAL data", "REAL" in str(v.get("data", "")).upper())
        check("validation names a reference", bool(v.get("reference")))
        check("validation.all_pass is true", v.get("all_pass") is True)
        print("\nRESULT:", "PASS — invariants hold" if ok else "FAIL")
        return 0 if ok else 1

    # status == "verified" (default strict path): substrate bundle
    check("has a verification block", "verification" in case)
    bundle = os.path.join(case_dir, case.get("bundle", "bundle"))
    prereg = os.path.join(bundle, "prereg.json")
    vrp = os.path.join(bundle, "verification_report.json")
    check("bundle/prereg.json exists", os.path.exists(prereg))
    check("bundle/verification_report.json exists", os.path.exists(vrp))
    if not (os.path.exists(prereg) and os.path.exists(vrp)):
        return 0 if ok else 1

    h = hashlib.sha256(open(prereg, "rb").read()).hexdigest()
    check("prereg_hash == sha256(bundle/prereg.json)", h == case["verification"].get("prereg_hash"))

    vr = json.load(open(vrp))
    vrb = {c["id"]: c for c in vr.get("claims", [])}
    for cl in case.get("claims", []):
        v = vrb.get(cl["id"], {})
        traced = v.get("status") == "GROUNDED" and \
            abs(float(v.get("artifact", "nan")) - float(cl["value"])) < max(0.02, abs(cl["value"]) * 1e-3)
        check(f"claim {cl['id']} GROUNDED and value traces to verification_report", traced)
    n_grounded = sum(1 for c in vr.get("claims", []) if c.get("status") == "GROUNDED")
    check("verification.n_grounded == n_claims == grounded count",
          case["verification"].get("n_grounded") == case["verification"].get("n_claims") == n_grounded == len(case.get("claims", [])))
    check("replay_byte_identical is true", case["verification"].get("replay_byte_identical") is True)

    print("\nRESULT:", "PASS — invariants hold" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_case.py cases/<id>"); sys.exit(2)
    sys.exit(main(sys.argv[1]))
