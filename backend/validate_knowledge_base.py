"""Validate backend/data/kbs_knowledge_base.json.

Run:  python backend/validate_knowledge_base.py
"""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

import inference_engine as engine  # noqa: E402


def main() -> int:
    try:
        kb = engine.load_knowledge_base()
    except engine.InferenceEngineError as exc:
        print(f"FAILED: {exc}")
        return 1
    errors: list[str] = []
    ds = kb["dataset"]
    if len(kb["rules"]) != ds["integrated_rule_count"]:
        errors.append("Rule count does not match dataset metadata.")
    for fc in kb["flowcharts"]:
        try:
            engine.get_flowchart_file(fc["flowchart_id"], kb)
        except KeyError:
            errors.append(f"Flowchart image missing: {fc['file_name']}")
    valid_safety_levels = {"Critical", "High", "Medium", "Low"}
    # Every rule must fire when given its own symptoms, and must possess complete domain attributes.
    for rule in kb["rules"]:
        rid = rule["rule_id"]
        if not rule.get("affected_component"):
            errors.append(f"{rid} is missing 'affected_component'.")
        if rule.get("safety_level") not in valid_safety_levels:
            errors.append(f"{rid} has invalid safety_level: {rule.get('safety_level')}")
        if not rule.get("required_tools") or not isinstance(rule["required_tools"], list):
            errors.append(f"{rid} is missing 'required_tools' list.")
        ma = rule.get("maintenance_actions")
        if not ma or not isinstance(ma, dict) or not ma.get("corrective_action") or not ma.get("replacement_criteria"):
            errors.append(f"{rid} is missing complete 'maintenance_actions' structure.")
        dq = rule.get("diagnostic_questions")
        if not dq or not isinstance(dq, list) or len(dq) == 0:
            errors.append(f"{rid} is missing 'diagnostic_questions'.")
        for q in (dq or []):
            if not q.get("question_id") or not q.get("question") or not q.get("supporting_answer") or not q.get("contradictory_answer"):
                errors.append(f"{rid} question {q.get('question_id')} is missing mandatory question fields.")
        if not rule.get("contradictory_evidence") or not isinstance(rule["contradictory_evidence"], list):
            errors.append(f"{rid} is missing 'contradictory_evidence' list.")
        sh = rule.get("system_hierarchy")
        if not sh or not isinstance(sh, dict) or not sh.get("component") or not sh.get("system"):
            errors.append(f"{rid} is missing 'system_hierarchy'.")

        res = engine.diagnose(rule["category_id"], list(rule["symptom_ids"]), kb=kb)
        ids = [m["rule_id"] for m in res["matches"] if m["match_type"] == "full"]
        if rid not in ids:
            errors.append(f"{rid} did not fire for its own symptoms.")
    if errors:
        print("Validation FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print(
        f"Knowledge base validation PASSED: {len(kb['categories'])} categories, "
        f"{len(kb['rules'])} rules, {len(kb['symptoms'])} symptoms, "
        f"{len(kb['flowcharts'])} flowcharts; every rule fires on its own symptoms."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
