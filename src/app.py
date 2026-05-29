from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

from src.rule_engine import apply_rules
from src.db import get_db

load_dotenv()

app = Flask(__name__)
CORS(app)


def _calculate_bmi(height_cm: float, weight_kg: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def _classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "저체중"
    if bmi < 23:
        return "정상"
    if bmi < 25:
        return "과체중"
    return "비만"


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "요청 본문이 없습니다."}), 400

    age = data.get("age")
    height = data.get("height")
    weight = data.get("weight")
    conditions = data.get("conditions", [])
    pain_area = data.get("pain_area", "없음")
    goal = data.get("goal", "건강 관리")

    if not all([age, height, weight]):
        return jsonify({"error": "age, height, weight 는 필수입니다."}), 400

    bmi = _calculate_bmi(height, weight)
    bmi_category = _classify_bmi(bmi)

    raw = apply_rules(conditions, pain_area, goal, int(age), float(bmi))

    recommended = [
        {"name": name, "intensity": intensity, "duration": duration, "score": round(score, 2)}
        for name, intensity, duration, score in raw["recommended"]
    ]

    response = {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "recommended": recommended,
        "forbidden_by_source": raw["forbidden_by_source"],
        "cautions": raw["cautions"],
        "goal_notes": raw["goal_notes"],
    }

    db = get_db()
    if db is not None:
        db.history.insert_one({
            "input": data,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "result": response,
            "created_at": datetime.now(timezone.utc),
        })

    return jsonify(response), 200


@app.route("/api/history", methods=["GET"])
def history():
    db = get_db()
    if db is None:
        return jsonify([])

    records = list(
        db.history.find({}, {"_id": 0}).sort("created_at", -1).limit(20)
    )
    return jsonify(records), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=os.getenv("FLASK_ENV") == "development", port=port)
