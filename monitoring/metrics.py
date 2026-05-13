from prometheus_client import Counter, Gauge, Histogram, generate_latest
import json
import os

# ── Prometheus Metrics ──────────────────────
TOTAL_SUBMISSIONS = Counter(
    "assignment_total_submissions",
    "Total number of submissions checked"
)

PASS_COUNTER = Counter(
    "assignment_pass_total",
    "Total number of passed submissions"
)

FAIL_COUNTER = Counter(
    "assignment_fail_total",
    "Total number of failed submissions"
)

AVERAGE_SCORE = Gauge(
    "assignment_average_score",
    "Average score of all submissions"
)

LATEST_SCORE = Gauge(
    "assignment_latest_score",
    "Score of the most recent submission"
)

PDF_SUBMISSIONS = Counter(
    "assignment_pdf_submissions_total",
    "Total PDF submissions"
)

CODE_SUBMISSIONS = Counter(
    "assignment_code_submissions_total",
    "Total Python code submissions"
)

IEEE_SUBMISSIONS = Counter(
    "assignment_ieee_submissions_total",
    "Total IEEE paper submissions"
)

MISSING_SECTIONS = Gauge(
    "assignment_ieee_missing_sections",
    "Number of missing sections in latest IEEE paper"
)

def update_metrics(results_file):
    """Update Prometheus metrics from results.json"""
    try:
        with open(results_file) as f:
            data = json.load(f)

        results = data.get("results", [])
        latest = data.get("latest", {})

        if not results:
            return

        # Update latest score
        LATEST_SCORE.set(latest.get("score", 0))

        # Update average score
        scores = [r.get("score", 0) for r in results]
        avg = sum(scores) / len(scores) if scores else 0
        AVERAGE_SCORE.set(avg)

        # Update missing sections for IEEE
        missing = len(latest.get("missing_sections", []))
        MISSING_SECTIONS.set(missing)

        print("✅ Prometheus metrics updated!")

    except Exception as e:
        print(f"❌ Metrics update failed: {e}")