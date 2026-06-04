from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

from src.rule_engine import apply_rules
from src.bmi import calculate_bmi, classify_bmi
from src.db import get_db
from src.user_input import validate_recommend_input

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    parsed, error = validate_recommend_input(data)
    if error:
        return jsonify({"error": error}), 400

    bmi = calculate_bmi(parsed["height"], parsed["weight"])
    bmi_category = classify_bmi(bmi)

    raw = apply_rules(
        parsed["conditions"], parsed["pain_area"], parsed["goal"],
        parsed["age"], float(bmi)
    )

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
            "input": parsed,
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
