"""
Simple Flask App with Health Check and Logging
Good DevOps-friendly example
"""

from flask import Flask, jsonify
import logging
import os

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.route("/")
def home():
    logging.info("Home endpoint accessed")
    return jsonify({
        "message": "DevOps Assignment Project Running nicely",
        "version": VERSION,
        "status": "success"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
