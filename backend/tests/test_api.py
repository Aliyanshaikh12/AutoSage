"""Tests for the Auto Sage Flask API."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app  # noqa: E402
import inference_engine as engine  # noqa: E402


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.kb = engine.load_knowledge_base()
        cls.labels = {s["label"].lower(): s["symptom_id"] for s in cls.kb["symptoms"]}

    def setUp(self):
        self.c = app.test_client()

    def test_health(self):
        d = self.c.get("/api/health").get_json()
        self.assertTrue(d["knowledge_base_loadable"])
        self.assertEqual(d["dataset"]["integrated_rule_count"], 93)

    def test_categories(self):
        d = self.c.get("/api/categories").get_json()
        self.assertEqual(len(d["categories"]), 8)

    def test_symptoms(self):
        r = self.c.get("/api/symptoms?category=CAT_BRAKES")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json()["symptoms"])
        self.assertEqual(self.c.get("/api/symptoms?category=NOPE").status_code, 404)

    def test_diagnose_match(self):
        r = self.c.post("/api/diagnose", json={
            "category_id": "CAT_BRAKES", "symptom_ids": [self.labels["hard brake pedal"]]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["status"], "matched")

    def test_diagnose_no_match(self):
        r = self.c.post("/api/diagnose", json={
            "category_id": "CAT_EMISSIONS", "symptom_ids": [self.labels["check engine light on"]]})
        self.assertEqual(r.get_json()["status"], "no_match")

    def test_diagnose_invalid(self):
        self.assertEqual(self.c.post("/api/diagnose", data="x").status_code, 400)
        self.assertEqual(self.c.post("/api/diagnose", json={"category_id": "CAT_BRAKES", "symptom_ids": []}).status_code, 400)
        self.assertEqual(self.c.post("/api/diagnose", json={"category_id": "NOPE", "symptom_ids": ["a"]}).status_code, 404)
        self.assertEqual(self.c.post("/api/diagnose", json={"category_id": "CAT_BRAKES", "symptom_ids": ["<script>"]}).status_code, 400)
        self.assertNotIn("<script>", self.c.post("/api/diagnose", json={"category_id": "CAT_BRAKES", "symptom_ids": ["<script>"]}).get_data(as_text=True))

    def test_knowledge_base(self):
        d = self.c.get("/api/knowledge-base").get_json()
        self.assertEqual(len(d["rules"]), 93)
        self.assertTrue(all("image_url" in f for f in d["flowcharts"]))

    def test_flowchart(self):
        r = self.c.get("/api/flowcharts/FC_OVERHEATING")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.mimetype, "image/png")
        r.close()
        self.assertEqual(self.c.get("/api/flowcharts/NOPE").status_code, 404)

    def test_old_audio_routes_removed(self):
        for path in ("/api/states", "/api/conditions", "/api/recordings/x"):
            self.assertEqual(self.c.get(path).status_code, 404)

    def test_cors(self):
        r = self.c.get("/api/health", headers={"Origin": "http://127.0.0.1:5173"})
        self.assertEqual(r.headers.get("Access-Control-Allow-Origin"), "http://127.0.0.1:5173")
        r = self.c.get("/api/health", headers={"Origin": "http://evil.example"})
        self.assertIsNone(r.headers.get("Access-Control-Allow-Origin"))

    def test_follow_up_questions_api(self):
        r = self.c.post(
            "/api/follow-up-questions",
            json={"category_id": "CAT_BRAKES", "symptom_ids": ["SYM_HARD_BRAKE_PEDAL"]},
        )
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertEqual(d["category_id"], "CAT_BRAKES")
        self.assertTrue(len(d["questions"]) >= 1)

    def test_diagnose_with_follow_up_answers(self):
        r = self.c.post(
            "/api/diagnose",
            json={
                "category_id": "CAT_BRAKES",
                "symptom_ids": ["SYM_HARD_BRAKE_PEDAL"],
                "follow_up_answers": {"Q_BRK_BOOSTER_START": "no", "Q_BRK_BOOSTER_HISS": "yes"},
            },
        )
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertEqual(d["status"], "matched")
        self.assertTrue(d["reasoning_trail"])
        self.assertTrue(d["candidates_comparison"])
        top = d["matches"][0]
        self.assertIn("Corroborated", top["diagnosis_status"])


if __name__ == "__main__":
    unittest.main()
