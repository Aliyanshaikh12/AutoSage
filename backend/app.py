"""Auto Sage - Flask REST API for the symptom-based Knowledge-Based System."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

BACKEND_DIR = Path(__file__).resolve().parent
DATA_DIR = BACKEND_DIR / "data"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import inference_engine as engine  # noqa: E402
from inference_engine import InferenceEngineError  # noqa: E402

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [re.compile(r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$")],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,120}$")


def _error(message: str, code: int):
    return jsonify({"status": "error", "message": message}), code


def _safe(text: str) -> str:
    """Drop user-supplied IDs from error text unless they look like safe IDs."""
    if ": " in text:
        prefix, value = text.rsplit(": ", 1)
        if not _SAFE_ID_RE.match(value.split(" ")[0]):
            return prefix + "."
    return text


def _kb():
    return engine.load_knowledge_base(DATA_DIR)


@app.errorhandler(413)
def too_large(_err):
    return _error("Request body is too large.", 413)


@app.errorhandler(404)
def not_found(_err):
    return _error("Endpoint not found.", 404)


@app.errorhandler(405)
def bad_method(_err):
    return _error("Method not allowed.", 405)


@app.route("/api/health", methods=["GET"])
def health():
    try:
        ds = _kb()["dataset"]
        return jsonify({
            "status": "ok",
            "message": "Auto Sage symptom KBS API is running.",
            "knowledge_base_loadable": True,
            "dataset": {k: ds[k] for k in (
                "title", "doi", "license", "category_count",
                "integrated_rule_count", "canonical_symptom_count", "flowchart_count")},
        })
    except InferenceEngineError:
        return jsonify({
            "status": "ok",
            "message": "API running, but the knowledge base could not be loaded.",
            "knowledge_base_loadable": False,
        })


@app.route("/api/categories", methods=["GET"])
def categories():
    try:
        return jsonify({"categories": engine.get_categories(_kb())})
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)


@app.route("/api/symptoms", methods=["GET"])
def symptoms():
    category = request.args.get("category")
    try:
        kb = _kb()
        if category is not None:
            category = category.strip()
            if not category:
                return _error("category must not be empty.", 400)
        return jsonify({"category_id": category, "symptoms": engine.get_symptoms(category, kb)})
    except KeyError:
        return _error(_safe(f"Unknown category_id: {category}"), 404)
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)


@app.route("/api/follow-up-questions", methods=["POST"])
def follow_up_questions():
    payload: Any = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error("Request body must be a JSON object.", 400)
    try:
        cat_id = payload.get("category_id")
        sym_ids = payload.get("symptom_ids")
        questions = engine.get_follow_up_questions(cat_id, sym_ids, _kb())
        return jsonify({
            "category_id": cat_id,
            "questions": questions,
            "count": len(questions),
        })
    except KeyError as exc:
        return _error(_safe(str(exc.args[0]) if exc.args else "Unknown category_id."), 404)
    except ValueError as exc:
        return _error(_safe(str(exc)), 400)
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)


@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    payload: Any = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error("Request body must be a JSON object.", 400)
    try:
        answers = payload.get("follow_up_answers")
        if answers is not None and not isinstance(answers, dict):
            return _error("follow_up_answers must be a dictionary of question IDs to answers.", 400)
        return jsonify(
            engine.diagnose(
                payload.get("category_id"),
                payload.get("symptom_ids"),
                follow_up_answers=answers,
                kb=_kb(),
            )
        )
    except KeyError as exc:
        return _error(_safe(str(exc.args[0]) if exc.args else "Unknown category_id."), 404)
    except ValueError as exc:
        return _error(_safe(str(exc)), 400)
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)


@app.route("/api/knowledge-base", methods=["GET"])
def knowledge_base():
    try:
        return jsonify(engine.get_knowledge_base(_kb()))
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)


@app.route("/api/flowcharts/<flowchart_id>", methods=["GET"])
def flowchart(flowchart_id: str):
    if not _SAFE_ID_RE.match(flowchart_id):
        return _error("Unknown flowchart.", 404)
    try:
        path = engine.get_flowchart_file(flowchart_id, _kb())
    except KeyError:
        return _error("Unknown flowchart.", 404)
    except InferenceEngineError:
        return _error("Knowledge base unavailable.", 500)
    return send_file(path, mimetype="image/png", conditional=False)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=debug,
        use_reloader=debug and os.environ.get("AUTO_SAGE_NO_RELOADER") != "1",
    )
