from flask import Flask, render_template, jsonify, Response
import json
import os
import sys
from prometheus_client import (
    Counter, Gauge, generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results.json")

# ── Prometheus Metrics ──────────────────────
TOTAL_SUBMISSIONS = Counter(
    "assignment_total_submissions",
    "Total submissions checked"
)
PASS_COUNTER = Counter(
    "assignment_pass_total",
    "Total passed submissions"
)
FAIL_COUNTER = Counter(
    "assignment_fail_total",
    "Total failed submissions"
)
LATEST_SCORE = Gauge(
    "assignment_latest_score",
    "Latest submission score"
)
AVERAGE_SCORE = Gauge(
    "assignment_average_score",
    "Average score of all submissions"
)
MISSING_SECTIONS_GAUGE = Gauge(
    "assignment_ieee_missing_sections",
    "Missing sections in latest IEEE paper"
)

def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                data = json.load(f)
                update_metrics(data)
                return data
        except:
            pass
    return {
        "latest": {
            "file": "No submissions yet",
            "type": "N/A",
            "score": 0,
            "max_score": 10,
            "status": "N/A",
            "timestamp": "N/A",
            "checks": [],
            "missing_sections": [],
            "present_sections": []
        },
        "results": []
    }

def update_metrics(data):
    """Update Prometheus metrics"""
    try:
        results = data.get("results", [])
        latest = data.get("latest", {})

        if not results:
            return

        LATEST_SCORE.set(latest.get("score", 0))

        scores = [r.get("score", 0) for r in results]
        AVERAGE_SCORE.set(sum(scores) / len(scores))

        missing = len(latest.get("missing_sections", []))
        MISSING_SECTIONS_GAUGE.set(missing)

    except Exception as e:
        print(f"Metrics error: {e}")

@app.route("/")
def dashboard():
    data = load_results()
    return render_template("index.html", data=data)

@app.route("/api/results")
def api_results():
    return jsonify(load_results())

@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    load_results()
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)