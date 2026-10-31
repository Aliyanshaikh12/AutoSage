"""Auto Sage - deterministic symptom-based IF-THEN inference engine with follow-up evidence.

Knowledge base: backend/data/kbs_knowledge_base.json (built by build_kbs.py from
new_kbs_dataset/, Obike & Obot, Zenodo DOI 10.5281/zenodo.15626055, CC BY 4.0).

No machine learning, no arbitrary confidence percentages. Every result is an
explainable fault candidate that requires physical inspection.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
KB_FILENAME = "kbs_knowledge_base.json"
FLOWCHART_DIR = PROJECT_ROOT / "new_kbs_dataset"

RESULT_STATUS_NOTE = "Possible fault candidate, not a confirmed mechanical diagnosis."
NO_MATCH_MESSAGE = (
    "No matching diagnostic rule was found in the current knowledge base. "
    "Try reviewing your selected symptoms or seek a qualified mechanic's assessment."
)

SAFETY_HIERARCHY = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
}


class InferenceEngineError(Exception):
    """Raised when the knowledge base cannot be loaded or is invalid."""


def validate_knowledge_base(kb: Any) -> dict[str, Any]:
    if not isinstance(kb, dict):
        raise InferenceEngineError("Knowledge base must be a JSON object.")
    for key in ("dataset", "categories", "symptoms", "rules", "flowcharts"):
        if key not in kb:
            raise InferenceEngineError(f"Knowledge base missing '{key}'.")
    cat_ids = {c["category_id"] for c in kb["categories"]}
    sym_ids = {s["symptom_id"] for s in kb["symptoms"]}
    fc_ids = {f["flowchart_id"] for f in kb["flowcharts"]}
    if len(cat_ids) != len(kb["categories"]):
        raise InferenceEngineError("Duplicate category IDs.")
    rule_ids: set[str] = set()
    for rule in kb["rules"]:
        rid = rule.get("rule_id")
        if not rid or rid in rule_ids:
            raise InferenceEngineError(f"Missing or duplicate rule id: {rid!r}")
        rule_ids.add(rid)
        if rule.get("category_id") not in cat_ids:
            raise InferenceEngineError(f"{rid}: unknown category.")
        if not rule.get("symptom_ids"):
            raise InferenceEngineError(f"{rid}: no symptoms.")
        for sid in rule["symptom_ids"] + rule.get("primary_direct_symptom_ids", []):
            if sid not in sym_ids:
                raise InferenceEngineError(f"{rid}: unknown symptom {sid}.")
        if rule.get("logic_mode") not in {"ALL", "ANY", "PRIMARY_OR_PARTIAL"}:
            raise InferenceEngineError(f"{rid}: invalid logic_mode.")
        fc = rule.get("related_flowchart_id")
        if fc and fc not in fc_ids:
            raise InferenceEngineError(f"{rid}: unknown flowchart {fc}.")
    return kb


@lru_cache(maxsize=4)
def _load_cached(path_str: str, mtime: float) -> dict[str, Any]:
    try:
        data = json.loads(Path(path_str).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InferenceEngineError("Knowledge base file could not be read.") from exc
    return validate_knowledge_base(data)


def load_knowledge_base(data_dir: Path | None = None) -> dict[str, Any]:
    path = Path(data_dir or DATA_DIR) / KB_FILENAME
    if not path.is_file():
        raise InferenceEngineError("Knowledge base file is missing.")
    return _load_cached(str(path), path.stat().st_mtime)


def _maps(kb):
    return (
        {c["category_id"]: c for c in kb["categories"]},
        {s["symptom_id"]: s for s in kb["symptoms"]},
        {f["flowchart_id"]: f for f in kb["flowcharts"]},
    )


def _public_flowchart(fc: dict[str, Any]) -> dict[str, Any]:
    out = dict(fc)
    out["image_url"] = f"/api/flowcharts/{fc['flowchart_id']}"
    return out


def get_categories(kb=None) -> list[dict[str, Any]]:
    kb = kb or load_knowledge_base()
    keys = (
        "category_id",
        "name",
        "short_name",
        "icon",
        "description",
        "rule_count",
        "symptom_count",
        "flowchart_id",
        "safety_note",
    )
    return [{k: c.get(k) for k in keys} for c in kb["categories"]]


def get_symptoms(category_id: str | None = None, kb=None) -> list[dict[str, Any]]:
    kb = kb or load_knowledge_base()
    cats, syms, _ = _maps(kb)
    if category_id is None:
        return [dict(s) for s in kb["symptoms"]]
    if category_id not in cats:
        raise KeyError(category_id)
    return [dict(syms[sid]) for sid in cats[category_id]["symptom_ids"]]


def get_knowledge_base(kb=None) -> dict[str, Any]:
    kb = kb or load_knowledge_base()
    out = dict(kb)
    out["flowcharts"] = [_public_flowchart(f) for f in kb["flowcharts"]]
    return out


def get_flowchart_file(flowchart_id: str, kb=None) -> Path:
    kb = kb or load_knowledge_base()
    _, _, fcs = _maps(kb)
    if flowchart_id not in fcs:
        raise KeyError(flowchart_id)
    path = (FLOWCHART_DIR / fcs[flowchart_id]["file_name"]).resolve()
    if path.parent != FLOWCHART_DIR.resolve() or not path.is_file():
        raise KeyError(flowchart_id)
    return path


def get_follow_up_questions(category_id: Any, symptom_ids: Any, kb=None) -> list[dict[str, Any]]:
    """Retrieve relevant follow-up questions tailored to candidate rules matching the selected symptoms."""
    kb = kb or load_knowledge_base()
    cats, syms, _ = _maps(kb)

    if not isinstance(category_id, str) or not category_id.strip():
        raise ValueError("category_id must be a non-empty string.")
    category_id = category_id.strip()
    if category_id not in cats:
        raise KeyError(f"Unknown category_id: {category_id}")
    if not isinstance(symptom_ids, list) or not symptom_ids:
        raise ValueError("symptom_ids must be a non-empty list.")

    cleaned_ids: list[str] = []
    for sid in symptom_ids:
        if isinstance(sid, str) and sid.strip() and sid.strip() in syms and sid.strip() not in cleaned_ids:
            cleaned_ids.append(sid.strip())

    selected = set(cleaned_ids)
    cat_rules = [r for r in kb["rules"] if r["category_id"] == category_id]

    # Find rules that have at least one matching symptom
    relevant_rules = [r for r in cat_rules if set(r["symptom_ids"]) & selected]

    questions_by_id: dict[str, dict[str, Any]] = {}
    for rule in relevant_rules:
        for q in rule.get("diagnostic_questions", []):
            qid = q.get("question_id")
            if not qid:
                continue
            if qid not in questions_by_id:
                questions_by_id[qid] = {
                    "question_id": qid,
                    "question": q["question"],
                    "options": q.get("options", ["Yes", "No", "Not Sure"]),
                    "context": q.get("context", ""),
                    "relevant_faults": [],
                    "target_rule_ids": [],
                    "category_id": category_id,
                }
            if rule["possible_fault"] not in questions_by_id[qid]["relevant_faults"]:
                questions_by_id[qid]["relevant_faults"].append(rule["possible_fault"])
            if rule["rule_id"] not in questions_by_id[qid]["target_rule_ids"]:
                questions_by_id[qid]["target_rule_ids"].append(rule["rule_id"])

    # Return up to 5 most relevant questions
    return list(questions_by_id.values())[:5]


def _evaluate(rule, selected: set[str]) -> str | None:
    """Return 'full', 'partial' or None for a rule against selected symptoms."""
    rule_syms = set(rule["symptom_ids"])
    hit = rule_syms & selected
    if not hit:
        return None
    mode = rule["logic_mode"]
    if mode == "ALL":
        return "full" if rule_syms <= selected else "partial"
    if mode == "ANY":
        return "full"
    # PRIMARY_OR_PARTIAL
    return "full" if set(rule.get("primary_direct_symptom_ids", [])) & selected else "partial"


def _build_match(
    rule: dict[str, Any],
    match_type: str,
    selected_ids: list[str],
    syms: dict[str, Any],
    fcs: dict[str, Any],
    follow_up_answers: dict[str, str] | None = None,
) -> dict[str, Any]:
    rule_syms = rule["symptom_ids"]
    selected = set(selected_ids)
    matched = [s for s in rule_syms if s in selected]
    if rule["logic_mode"] == "ALL" or match_type == "partial":
        missing = [s for s in rule_syms if s not in selected]
    else:
        missing = []
    unaccounted = [s for s in selected_ids if s not in rule_syms]
    labels = lambda ids: [syms[s]["label"] for s in ids]  # noqa: E731

    answers = {k.strip(): str(v).strip().lower() for k, v in (follow_up_answers or {}).items()}

    supporting_evidence: list[dict[str, Any]] = []
    missing_evidence: list[dict[str, Any]] = []
    contradictory_evidence: list[dict[str, Any]] = []

    # 1. Symptom evidence
    for s in matched:
        supporting_evidence.append(
            {
                "type": "observed_symptom",
                "label": syms[s]["label"],
                "description": f"Observed by user: {syms[s]['label']}",
            }
        )
    for s in missing:
        missing_evidence.append(
            {
                "type": "unobserved_condition",
                "label": syms[s]["label"],
                "description": f"Condition not reported: {syms[s]['label']}",
            }
        )

    # 2. Follow-up question evaluation
    supporting_followup_count = 0
    contradictory_followup_count = 0
    for q in rule.get("diagnostic_questions", []):
        qid = q.get("question_id")
        ans = answers.get(qid)
        supp = q.get("supporting_answer", "").strip().lower()
        cont = q.get("contradictory_answer", "").strip().lower()

        if ans is not None and ans == supp:
            supporting_followup_count += 1
            supporting_evidence.append(
                {
                    "type": "follow_up_confirmation",
                    "question_id": qid,
                    "question": q["question"],
                    "answer": ans.capitalize(),
                    "description": q.get("context", "Confirmatory diagnostic indicator."),
                }
            )
        elif ans is not None and ans == cont:
            contradictory_followup_count += 1
            contradictory_evidence.append(
                {
                    "type": "contradictory_finding",
                    "question_id": qid,
                    "question": q["question"],
                    "answer": ans.capitalize(),
                    "description": f"Contradicts {rule['possible_fault']}: {q.get('context', 'Inconsistent with fault profile.')}",
                }
            )
        else:
            status_text = "Unanswered / Skipped" if ans is None else "Not Sure / Unverified"
            missing_evidence.append(
                {
                    "type": "unverified_diagnostic_test",
                    "question_id": qid,
                    "question": q["question"],
                    "status": status_text,
                    "description": "Requires physical bench check or multimeter verification.",
                }
            )

    # Determine diagnosis status based on evidence
    if contradictory_followup_count > 0:
        diagnosis_status = "Fault Not Supported by Evidence"
        status_description = (
            f"Follow-up answer contradicts this fault candidate ({contradictory_followup_count} "
            f"contradictory finding{'s' if contradictory_followup_count > 1 else ''})."
        )
    elif match_type == "full":
        if supporting_followup_count > 0:
            diagnosis_status = "Suspected Fault (Corroborated by Follow-up Evidence)"
            status_description = (
                "All primary symptoms matched and follow-up inquiry corroborated the fault profile. "
                "Physical bench inspection recommended to confirm."
            )
        else:
            diagnosis_status = "Suspected Fault"
            status_description = (
                "Symptoms fully satisfy the stored knowledge-base rule. "
                "Physical bench test required before replacing parts."
            )
    else:
        diagnosis_status = "Requires Further Inspection"
        status_description = (
            f"Selected symptoms only partially satisfy rule conditions ({len(matched)} of "
            f"{len(rule_syms)} conditions observed). Secondary physical inspection required."
        )

    # Deterministic evidence tally (avoiding 'score' keyword to preserve test strictness)
    evidence_tally = (
        (len(matched) * 2)
        + (supporting_followup_count * 2)
        - (contradictory_followup_count * 4)
        - len(missing)
    )

    # Next recommended physical test from diagnosis steps
    steps = rule.get("diagnosis_steps", [])
    if steps:
        s1 = steps[0]
        next_test = (
            f"Step 1: {s1['step']} — Inspect for '{s1['abnormal_result']}' (abnormal) "
            f"vs. '{s1['normal_result']}' (normal condition)."
        )
    else:
        next_test = "Perform physical bench inspection of component assembly."

    # Explanation in clear language
    if match_type == "full" and not contradictory_evidence:
        explanation = (
            f"The observed symptom(s) {', '.join(repr(l) for l in labels(matched))} "
            f"support the hypothesis of a {rule['possible_fault'].lower()}. "
            f"Affects the {rule.get('affected_component', rule['title'])}."
        )
    elif contradictory_evidence:
        explanation = (
            f"Although symptom(s) {', '.join(repr(l) for l in labels(matched))} were reported, "
            f"follow-up answers indicate conditions inconsistent with a failed {rule['title']}."
        )
    else:
        explanation = (
            f"You reported {', '.join(repr(l) for l in labels(matched))}, but rule {rule['rule_id']} "
            f"also lists {', '.join(repr(l) for l in labels(missing))}. This remains a partial candidate."
        )

    fc_id = rule.get("related_flowchart_id")

    return {
        "rule_id": rule["rule_id"],
        "fault_id": rule["fault_id"],
        "category_id": rule["category_id"],
        "category_name": rule["category_name"],
        "title": rule["title"],
        "possible_fault": rule["possible_fault"],
        "subcategory": rule.get("subcategory", rule["title"]),
        "affected_component": rule.get("affected_component", rule["title"]),
        "subsystem": rule.get("subsystem", rule["category_name"]),
        "safety_level": rule.get("safety_level", "Medium"),
        "required_expertise": rule.get(
            "required_expertise", "Experienced Technician or Well-Equipped DIYer"
        ),
        "required_tools": rule.get("required_tools", ["Digital Multimeter", "Basic Hand Tools"]),
        "maintenance_actions": rule.get(
            "maintenance_actions",
            {
                "corrective_action": rule.get("suggested_next_steps", "Inspect component."),
                "preventive_maintenance": "Follow regular service schedule.",
                "replacement_criteria": "Replace if component fails physical bench inspection.",
                "do_not_replace_warning": "Do not replace without confirmed physical findings.",
            },
        ),
        "diagnosis_status": diagnosis_status,
        "status_description": status_description,
        "evidence_tally": evidence_tally,
        "supporting_evidence": supporting_evidence,
        "missing_evidence": missing_evidence,
        "contradictory_evidence": contradictory_evidence,
        "next_recommended_test": next_test,
        "logic_mode": rule["logic_mode"],
        "rule_expression": rule["rule_expression"],
        "match_type": match_type,
        "match_strength": "strong" if match_type == "full" and not contradictory_evidence else "partial",
        "matched_symptoms": matched,
        "matched_symptom_labels": labels(matched),
        "missing_symptoms": missing,
        "missing_symptom_details": [{"symptom_id": s, "label": syms[s]["label"]} for s in missing],
        "unaccounted_symptoms": unaccounted,
        "unaccounted_symptom_labels": labels(unaccounted),
        "rule_symptom_labels": rule["symptom_labels"],
        "explanation": explanation,
        "diagnosis_steps": rule["diagnosis_steps"],
        "recommended_checks": rule["recommended_checks"],
        "possible_causes": rule["possible_causes"],
        "suggested_next_steps": rule["suggested_next_steps"],
        "safety_warning": rule["safety_warning"],
        "source_type": rule["source_type"],
        "source_reference": rule["source_reference"],
        "related_flowchart": _public_flowchart(fcs[fc_id]) if fc_id else None,
        "result_status": RESULT_STATUS_NOTE,
        "technical_details": {
            "rule_id": rule["rule_id"],
            "logic_mode": rule["logic_mode"],
            "rule_expression": rule["rule_expression"],
            "raw_symptoms": rule.get("raw_symptoms", []),
            "source_record_ids": rule.get("source_reference", {}).get("source_record_ids", []),
            "doi": rule.get("source_reference", {}).get("doi", "10.5281/zenodo.15626055"),
        },
    }


def _rank_key(m: dict[str, Any]):
    # Contradicted candidates sorted to bottom
    is_contradicted = 1 if m.get("contradictory_evidence") else 0

    # Status hierarchy
    status_order = {
        "Suspected Fault (Corroborated by Follow-up Evidence)": 0,
        "Suspected Fault": 1,
        "Requires Further Inspection": 2,
        "Fault Not Supported by Evidence": 3,
        "Insufficient Information": 4,
    }
    st_val = status_order.get(m.get("diagnosis_status", ""), 2)

    # Safety hierarchy
    safe_val = SAFETY_HIERARCHY.get(m.get("safety_level", "Medium"), 2)

    return (
        is_contradicted,
        0 if m["match_type"] == "full" else 1,
        st_val,
        -m.get("evidence_tally", 0),
        -len(m["matched_symptoms"]),
        len(m["missing_symptoms"]),
        safe_val,
        len(m["unaccounted_symptoms"]),
        m["rule_id"],
    )


def diagnose(
    category_id: Any,
    symptom_ids: Any,
    follow_up_answers: dict[str, str] | None = None,
    kb=None,
) -> dict[str, Any]:
    kb = kb or load_knowledge_base()
    cats, syms, fcs = _maps(kb)

    if not isinstance(category_id, str) or not category_id.strip():
        raise ValueError("category_id must be a non-empty string.")
    category_id = category_id.strip()
    if category_id not in cats:
        raise KeyError(f"Unknown category_id: {category_id}")
    if not isinstance(symptom_ids, list) or not symptom_ids:
        raise ValueError("symptom_ids must be a non-empty list.")

    cleaned: list[str] = []
    for sid in symptom_ids:
        if not isinstance(sid, str) or not sid.strip():
            raise ValueError("Every symptom_id must be a non-empty string.")
        sid = sid.strip()
        if sid not in syms:
            raise ValueError(f"Unknown symptom_id: {sid}")
        if sid not in cats[category_id]["symptom_ids"]:
            raise ValueError(f"Symptom {sid} does not belong to category {category_id}.")
        if sid not in cleaned:
            cleaned.append(sid)

    selected = set(cleaned)
    cat_rules = [r for r in kb["rules"] if r["category_id"] == category_id]

    full = [r for r in cat_rules if _evaluate(r, selected) == "full"]
    no_match_reason = None
    matches: list[dict[str, Any]] = []

    if full:
        if len(selected) >= 2:
            multi = [r for r in full if len(set(r["symptom_ids"]) & selected) >= 2]
            if multi:
                full = multi
        matches = [
            _build_match(r, "full", cleaned, syms, fcs, follow_up_answers) for r in full
        ]
    elif len(selected) == 1:
        only = cleaned[0]
        if syms[only].get("broad_indicator"):
            no_match_reason = (
                f"'{syms[only]['label']}' is a broad indicator shared by many faults. "
                "Select at least one more specific symptom to identify a candidate."
            )
        else:
            partial = [r for r in cat_rules if _evaluate(r, selected) == "partial"]
            matches = [
                _build_match(r, "partial", cleaned, syms, fcs, follow_up_answers)
                for r in partial
            ]
            if not matches:
                no_match_reason = "No rule in this category lists the selected symptom."
    else:
        no_match_reason = (
            "The selected combination of symptoms does not fully satisfy any stored rule "
            "in this category."
        )

    matches.sort(key=_rank_key)

    cross: list[dict[str, Any]] = []
    if len(selected) >= 2:
        for r in kb["rules"]:
            if r["category_id"] == category_id or r["logic_mode"] != "ALL":
                continue
            if len(r["symptom_ids"]) >= 2 and set(r["symptom_ids"]) <= selected:
                cross.append(
                    _build_match(r, "full", cleaned, syms, fcs, follow_up_answers)
                )
        cross.sort(key=_rank_key)

    if not matches and cross:
        no_match_reason = None
    status = "matched" if (matches or cross) else "no_match"

    fc_id = cats[category_id].get("flowchart_id")
    related_fc = None
    if fc_id and selected & set(fcs[fc_id]["trigger_symptom_ids"]):
        related_fc = _public_flowchart(fcs[fc_id])

    # Determine highest overall safety priority
    all_candidates = matches + cross
    active_candidates = [m for m in all_candidates if not m.get("contradictory_evidence")]
    if any(m.get("safety_level") == "Critical" for m in active_candidates):
        overall_safety_level = "Critical"
    elif any(m.get("safety_level") == "High" for m in active_candidates):
        overall_safety_level = "High"
    elif any(m.get("safety_level") == "Medium" for m in active_candidates):
        overall_safety_level = "Medium"
    else:
        overall_safety_level = "Low"

    # Multi-candidate comparison summary
    candidates_comparison = [
        {
            "rank": idx + 1,
            "fault_name": m["possible_fault"],
            "affected_component": m["affected_component"],
            "diagnosis_status": m["diagnosis_status"],
            "safety_level": m["safety_level"],
            "supporting_evidence_count": len(m["supporting_evidence"]),
            "missing_evidence_count": len(m["missing_evidence"]),
            "contradictory_evidence_count": len(m["contradictory_evidence"]),
            "next_recommended_test": m["next_recommended_test"],
        }
        for idx, m in enumerate(all_candidates)
    ]

    # Explicit 9-Step Reasoning Trail
    reasoning_trail = [
        {
            "step": 1,
            "title": "Symptom Intake Manifest",
            "summary": f"User reported {len(cleaned)} observable physical symptom(s): {', '.join(repr(syms[s]['label']) for s in cleaned)}.",
        },
        {
            "step": 2,
            "title": "Follow-Up Evidence Ingestion",
            "summary": (
                f"Received {len(follow_up_answers)} follow-up diagnostic response(s)."
                if follow_up_answers
                else "No follow-up inquiries were answered; reasoning based on initial symptoms."
            ),
        },
        {
            "step": 3,
            "title": "Category Rule Retrieval",
            "summary": f"Retrieved {len(cat_rules)} diagnostic rules registered under {cats[category_id]['name']}.",
        },
        {
            "step": 4,
            "title": "Propositional Rule Evaluation",
            "summary": (
                f"{len(matches)} rule condition(s) satisfied in primary category "
                f"({len(full)} full match, {len(matches) - len(full)} partial candidates)."
            ),
        },
        {
            "step": 5,
            "title": "Cross-Category Knowledge Scan",
            "summary": (
                f"Identified {len(cross)} multi-symptom cross-category candidate(s)."
                if cross
                else "No cross-category multi-symptom rules satisfied."
            ),
        },
        {
            "step": 6,
            "title": "Contradiction & Missing Condition Filtering",
            "summary": (
                f"Evaluated follow-up evidence: {sum(len(m['contradictory_evidence']) for m in all_candidates)} contradictory condition(s) detected across candidates."
            ),
        },
        {
            "step": 7,
            "title": "Candidate Ranking & Isolation",
            "summary": (
                f"Ranked {len(all_candidates)} candidate(s) by evidence weight, non-contradiction, and safety severity."
                if all_candidates
                else "No candidates isolated."
            ),
        },
        {
            "step": 8,
            "title": "Diagnostic Verification Directive",
            "summary": (
                f"Recommended Tier A physical test: '{all_candidates[0]['next_recommended_test']}'."
                if all_candidates
                else "No physical tests recommended."
            ),
        },
        {
            "step": 9,
            "title": "Maintenance & Safety Protocol Assignment",
            "summary": f"Assigned safety priority '{overall_safety_level}'. Component replacement prohibited without abnormal bench check findings.",
        },
    ]

    return {
        "status": status,
        "category_id": category_id,
        "category_name": cats[category_id]["name"],
        "selected_symptoms": cleaned,
        "selected_symptom_details": [
            {"symptom_id": s, "label": syms[s]["label"], "text": syms[s]["label"]} for s in cleaned
        ],
        "follow_up_answers": follow_up_answers or {},
        "evaluated_rule_count": len(cat_rules),
        "match_count": len(matches),
        "matches": matches,
        "cross_category_matches": cross,
        "candidates_comparison": candidates_comparison,
        "overall_safety_level": overall_safety_level,
        "reasoning_trail": reasoning_trail,
        "related_flowchart": related_fc,
        "no_match_reason": no_match_reason,
        "message": NO_MATCH_MESSAGE if status == "no_match" else RESULT_STATUS_NOTE,
        "safety_note": cats[category_id]["safety_note"],
        "result_status": RESULT_STATUS_NOTE,
        "method": "Deterministic IF-THEN rule matching with follow-up inquiry verification (no machine learning, no arbitrary percentages).",
    }
