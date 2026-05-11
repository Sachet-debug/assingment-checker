from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results.json")

def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                return json.load(f)
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