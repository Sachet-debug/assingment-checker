import json
import requests
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

def load_env_file():
    """Load simple KEY=VALUE pairs from .env for local runs."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_env_file()

# Load results
try:
    with open("dashboard/results.json") as f:
        data = json.load(f)
except Exception as e:
    print(f"Could not load results.json: {e}")
    data = {"latest": {}}

r = data.get("latest", {})
checks = r.get("checks", [])

# Build breakdown
breakdown = "\n".join([
    ("✅ " if c["passed"] else "❌ ") + c["name"]
    for c in checks
]) if checks else "No checks found"

# Missing sections warning
missing_text = ""
if r.get("missing_sections"):
    missing = ", ".join(r["missing_sections"])
    missing_text = f"\n⚠️ *Missing Sections:* {missing}"

score = r.get("score", 0)
max_score = r.get("max_score", 10)
status = r.get("status", "N/A")
status_icon = "✅" if status == "PASS" else "❌"

# Build Slack message
message = {
    "text": (
        "🎓 *Assignment Checker Result*\n\n"
        f"📁 *File:* {r.get('file', 'N/A')}\n"
        f"📝 *Type:* {r.get('type', 'N/A')}\n"
        f"⭐ *Score:* {score}/{max_score}\n"
        f"{status_icon} *Status:* {status}"
        f"{missing_text}\n\n"
        f"*Score Breakdown:*\n{breakdown}\n\n"
        f"🕐 *Checked at:* {r.get('timestamp', 'N/A')}\n"
        f"🔗 *Dashboard:* "
        f"{os.environ.get('RENDER_URL', 'https://your-app.onrender.com')}"
    )
}

# Send Slack notification
webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
if not webhook_url:
    print("❌ SLACK_WEBHOOK_URL not set!")
else:
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("✅ Slack notification sent!")
    else:
        print(f"❌ Slack error: {response.status_code}")

# Send email notification
recipient = os.environ.get("TEACHER_EMAIL") or os.environ.get("RECIPIENT_EMAIL", "")
if recipient:
    sys.path.insert(0, "email_notify")
    from send_email import send_email
    send_email(r, recipient)
else:
    print("⚠️ RECIPIENT_EMAIL not set — skipping email")
