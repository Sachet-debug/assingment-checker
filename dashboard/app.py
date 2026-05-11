from flask import Flask, render_template, jsonify
import json
import os
import requests

app = Flask(__name__)

# GitHub raw URL for live results
# Replace YOUR_USERNAME and YOUR_REPO
GITHUB_RAW_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/assignment-checker/main/dashboard/results.json"

LOCAL_RESULTS = os.path.join(os.path.dirname(__file__), "results.json")

def load_results():
    """Try GitHub first for live data, fallback to local"""
    # Try fetching live from GitHub
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"GitHub fetch failed: {e}")

    # Fallback to local file
    if os.path.exists(LOCAL_RESULTS):
        try:
            with open(LOCAL_RESULTS, "r") as f:
                return json.load(f)
        except:
            pass

    # Default empty state
    return {
        "latest": {
            "file": "No submissions yet",
            "type": "N/A",
            "score": 0,
            "max_score": 10,
            "status": "N/A",
            "timestamp": "N/A",
            "checks": []
        },
        "results": []
    }

@app.route("/")
def dashboard():
    data = load_results()
    return render_template("index.html", data=data)

@app.route("/api/results")
def api_results():
    return jsonify(load_results())

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)