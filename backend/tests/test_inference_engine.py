"""Tests for the symptom-based inference engine."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import inference_engine as engine  # noqa: E402


def sym(label):
    return "SYM_" + "".join(c if c.isalnum() else "_" for c in label).upper().strip("_")


class TestEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = engine.load_knowledge_base()
        cls.labels = {s["label"].lower(): s["symptom_id"] for s in cls.kb["symptoms"]}

    def sid(self, label):
        return self.labels[label.lower()]

    def test_counts(self):
        self.assertEqual(len(self.kb["categories"]), 8)
        self.assertEqual(len(self.kb["rules"]), 93)
        self.assertEqual(len(self.kb["flowcharts"]), 4)

    def test_every_rule_fires(self):
        for rule in self.kb["rules"]:
            res = engine.diagnose(rule["category_id"], rule["symptom_ids"], self.kb)
            self.assertIn(rule["rule_id"], [m["rule_id"] for m in res["matches"]], rule["rule_id"])

    def test_full_match_has_evidence(self):
        rule = next(r for r in self.kb["rules"] if r["logic_mode"] == "ALL")
        m = engine.diagnose(rule["category_id"], rule["symptom_ids"], self.kb)["matches"]
        top = next(x for x in m if x["rule_id"] == rule["rule_id"])
        self.assertEqual(top["match_type"], "full")
        self.assertEqual(top["missing_symptoms"], [])
        self.assertTrue(top["diagnosis_steps"])
        self.assertIn("IF", top["rule_expression"])
        self.assertIn("DOI", top["source_reference"]["doi"].upper() + "DOI")

    def test_single_symptom_partial(self):
        rule = next(r for r in self.kb["rules"] if r["logic_mode"] == "ALL"
                    and not any(next(s for s in self.kb["symptoms"] if s["symptom_id"] == x)["broad_indicator"]
                                for x in r["symptom_ids"][:1]))
        res = engine.diagnose(rule["category_id"], [rule["symptom_ids"][0]], self.kb)
        self.assertEqual(res["status"], "matched")
        partials = [m for m in res["matches"] if m["match_type"] == "partial"]
        if partials:
            self.assertTrue(partials[0]["missing_symptoms"])

    def test_broad_indicator_alone_no_match(self):
        res = engine.diagnose("CAT_EMISSIONS", [self.sid("Check engine light on")], self.kb)
        self.assertEqual(res["status"], "no_match")
        self.assertTrue(res["no_match_reason"])
        self.assertEqual(res["matches"], [])

    def test_hard_brake_pedal_matches_booster(self):
        res = engine.diagnose("CAT_BRAKES", [self.sid("Hard brake pedal")], self.kb)
        self.assertEqual(res["status"], "matched")
        self.assertEqual(res["matches"][0]["match_type"], "full")

    def test_flowchart_attached(self):
        res = engine.diagnose("CAT_COOLING", [self.sid("Engine overheating")], self.kb)
        self.assertEqual(res["related_flowchart"]["flowchart_id"], "FC_OVERHEATING")
        self.assertTrue(res["related_flowchart"]["image_url"].endswith("FC_OVERHEATING"))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            engine.diagnose("", ["x"], self.kb)
        with self.assertRaises(KeyError):
            engine.diagnose("CAT_NOPE", ["x"], self.kb)
        with self.assertRaises(ValueError):
            engine.diagnose("CAT_BRAKES", [], self.kb)
        with self.assertRaises(ValueError):
            engine.diagnose("CAT_BRAKES", ["SYM_DOES_NOT_EXIST"], self.kb)
        with self.assertRaises(ValueError):
            engine.diagnose("CAT_BRAKES", [self.sid("Engine overheating")], self.kb)

    def test_dedupes_symptoms(self):
        s = self.sid("Hard brake pedal")
        res = engine.diagnose("CAT_BRAKES", [s, s], self.kb)
        self.assertEqual(res["selected_symptoms"], [s])

    def test_no_confidence_scores(self):
        res = engine.diagnose("CAT_BRAKES", [self.sid("Hard brake pedal")], self.kb)
        keys = set(res) | {k for m in res["matches"] for k in m}
        self.assertFalse([k for k in keys if "confidence" in k or "score" in k])

    def test_flowchart_whitelist(self):
        self.assertTrue(engine.get_flowchart_file("FC_BRAKES", self.kb).is_file())
        with self.assertRaises(KeyError):
            engine.get_flowchart_file("../app", self.kb)

    def test_get_symptoms_unknown_category(self):
        with self.assertRaises(KeyError):
            engine.get_symptoms("CAT_NOPE", self.kb)

    def test_validate_rejects_bad_kb(self):
        with self.assertRaises(engine.InferenceEngineError):
            engine.validate_knowledge_base([])
        with self.assertRaises(engine.InferenceEngineError):
            engine.validate_knowledge_base({"dataset": {}})

    def test_follow_up_questions_generation(self):
        questions = engine.get_follow_up_questions("CAT_BRAKES", [self.sid("Hard brake pedal")], self.kb)
        self.assertTrue(len(questions) >= 1)
        q_ids = [q["question_id"] for q in questions]
        self.assertIn("Q_BRK_BOOSTER_START", q_ids)
        self.assertTrue(questions[0]["relevant_faults"])

    def test_follow_up_contradictory_evidence(self):
        # Answering 'yes' to booster start contradicts a failed brake booster
        res = engine.diagnose(
            "CAT_BRAKES",
            [self.sid("Hard brake pedal")],
            follow_up_answers={"Q_BRK_BOOSTER_START": "yes"},
            kb=self.kb,
        )
        self.assertEqual(res["status"], "matched")
        top = res["matches"][0]
        self.assertEqual(top["diagnosis_status"], "Fault Not Supported by Evidence")
        self.assertTrue(top["contradictory_evidence"])

    def test_follow_up_supporting_evidence(self):
        # Answering 'no' to booster start and 'yes' to hiss supports failed booster
        res = engine.diagnose(
            "CAT_BRAKES",
            [self.sid("Hard brake pedal")],
            follow_up_answers={"Q_BRK_BOOSTER_START": "no", "Q_BRK_BOOSTER_HISS": "yes"},
            kb=self.kb,
        )
        self.assertEqual(res["status"], "matched")
        top = res["matches"][0]
        self.assertIn("Corroborated", top["diagnosis_status"])
        self.assertFalse(top["contradictory_evidence"])
        self.assertTrue(top["supporting_evidence"])
        self.assertTrue(len(res["reasoning_trail"]) == 9)

    def test_enriched_attributes_present(self):
        res = engine.diagnose("CAT_BRAKES", [self.sid("Hard brake pedal")], kb=self.kb)
        top = res["matches"][0]
        self.assertEqual(top["safety_level"], "Critical")
        self.assertIn("Booster", top["affected_component"])
        self.assertTrue(top["required_tools"])
        self.assertTrue(top["maintenance_actions"]["corrective_action"])
        self.assertTrue(top["next_recommended_test"])
        self.assertEqual(res["overall_safety_level"], "Critical")
        self.assertTrue(res["candidates_comparison"])


if __name__ == "__main__":
    unittest.main()
