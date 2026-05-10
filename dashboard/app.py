from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Look for results.json in multiple locations
RESULTS_PATHS = [
    os.path.join(os.path.dirname(__file__), "results.json"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "results.json"),
    "/app/dashboard/results.json",
]

def load_results():
    """Load results from JSON file"""
    for path in RESULTS_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    if data.get("results"):
                        return data
            except:
                pass

    # Return default if no results found
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