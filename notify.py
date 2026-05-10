import json
import requests
import os

# Load results
try:
    with open("dashboard/results.json") as f:
        data = json.load(f)
except Exception as e:
    print(f"Could not load results.json: {e}")
    data = {"latest": {}}

r = data.get("latest", {})
checks = r.get("checks", [])

# Build breakdown text
breakdown = "\n".join([
    ("✅ " if c["passed"] else "❌ ") + c["name"]
    for c in checks
]) if checks else "No checks found"

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
        f"{status_icon} *Status:* {status}\n\n"
        f"*Score Breakdown:*\n{breakdown}\n\n"
        f"🕐 *Checked at:* {r.get('timestamp', 'N/A')}\n"
        f"🔗 *Dashboard:* {os.environ.get('RENDER_URL', 'https://your-app.onrender.com')}"
    )
}

# Send to Slack
webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")

if not webhook_url:
    print("❌ SLACK_WEBHOOK_URL not set!")
else:
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("✅ Slack notification sent successfully!")
    else:
        print(f"❌ Slack error: {response.status_code} - {response.text}")