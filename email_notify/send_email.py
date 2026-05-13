import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(result, recipient_email):
    """Send email notification with assignment result"""

    sender_email = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        print("❌ Gmail credentials not set!")
        return False

    # Build email content
    subject = f"Assignment Result: {result.get('file')} — {result.get('status')}"

    # Build checks HTML
    checks_html = ""
    for check in result.get("checks", []):
        icon = "✅" if check["passed"] else "❌"
        color = "#16a34a" if check["passed"] else "#dc2626"
        checks_html += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #eee">
                {icon} {check['name']}
            </td>
            <td style="padding:8px;border-bottom:1px solid #eee;color:{color}">
                {check['message']}
            </td>
            <td style="padding:8px;border-bottom:1px solid #eee;
                       font-weight:bold;color:{color}">
                +{check['points']} pts
            </td>
        </tr>"""

    # Missing sections warning
    missing_html = ""
    if result.get("missing_sections"):
        missing = ", ".join(result["missing_sections"])
        missing_html = f"""
        <div style="background:#fef2f2;border:1px solid #fecaca;
                    border-radius:8px;padding:16px;margin:16px 0">
            <h3 style="color:#dc2626;margin:0 0 8px">
                ⚠️ Missing Sections
            </h3>
            <p style="color:#7f1d1d;margin:0">
                The following sections are missing from your paper:
                <strong>{missing}</strong>
            </p>
            <p style="color:#7f1d1d;margin:8px 0 0">
                Please add these sections and resubmit.
            </p>
        </div>"""

    # Present sections
    present_html = ""
    if result.get("present_sections"):
        present = ", ".join(result["present_sections"])
        present_html = f"""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;
                    border-radius:8px;padding:16px;margin:16px 0">
            <h3 style="color:#16a34a;margin:0 0 8px">
                ✅ Present Sections
            </h3>
            <p style="color:#14532d;margin:0">
                <strong>{present}</strong>
            </p>
        </div>"""

    score = result.get("score", 0)
    max_score = result.get("max_score", 10)
    status = result.get("status", "N/A")
    status_color = "#16a34a" if status == "PASS" else "#dc2626"
    percentage = int((score / max_score) * 100)

    html_body = f"""
    <html>
    <body style="font-family:'Segoe UI',sans-serif;
                 background:#f8f9fa;margin:0;padding:20px">
        <div style="max-width:600px;margin:0 auto;
                    background:white;border-radius:12px;
                    overflow:hidden;box-shadow:0 4px 6px rgba(0,0,0,0.1)">

            <!-- Header -->
            <div style="background:#5b2d8e;padding:24px;text-align:center">
                <h1 style="color:white;margin:0;font-size:24px">
                    🎓 Assignment Checker Result
                </h1>
                <p style="color:#d4c8f0;margin:8px 0 0">
                    Automated evaluation by DevSecOps Pipeline
                </p>
            </div>

            <!-- Score Card -->
            <div style="padding:24px">
                <div style="display:flex;justify-content:space-between;
                            background:#f8f5ff;border-radius:8px;
                            padding:16px;margin-bottom:16px">
                    <div>
                        <p style="color:#6b7280;margin:0;font-size:12px">
                            FILE
                        </p>
                        <p style="color:#1f2937;margin:4px 0 0;
                                  font-weight:bold">
                            {result.get('file', 'N/A')}
                        </p>
                    </div>
                    <div>
                        <p style="color:#6b7280;margin:0;font-size:12px">
                            TYPE
                        </p>
                        <p style="color:#1f2937;margin:4px 0 0;
                                  font-weight:bold">
                            {result.get('type', 'N/A')}
                        </p>
                    </div>
                    <div>
                        <p style="color:#6b7280;margin:0;font-size:12px">
                            SCORE
                        </p>
                        <p style="color:#1f2937;margin:4px 0 0;
                                  font-weight:bold;font-size:20px">
                            {score}/{max_score}
                        </p>
                    </div>
                    <div>
                        <p style="color:#6b7280;margin:0;font-size:12px">
                            STATUS
                        </p>
                        <p style="color:{status_color};margin:4px 0 0;
                                  font-weight:bold;font-size:18px">
                            {status}
                        </p>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div style="background:#e5e7eb;border-radius:999px;
                            height:12px;margin-bottom:20px">
                    <div style="background:linear-gradient(90deg,#5b2d8e,#02c39a);
                                width:{percentage}%;height:100%;
                                border-radius:999px"></div>
                </div>

                {missing_html}
                {present_html}

                <!-- Checks Table -->
                <h3 style="color:#1f2937;margin:16px 0 8px">
                    📊 Detailed Score Breakdown
                </h3>
                <table style="width:100%;border-collapse:collapse">
                    <thead>
                        <tr style="background:#f3f4f6">
                            <th style="padding:10px;text-align:left;
                                       font-size:12px;color:#6b7280">
                                CHECK
                            </th>
                            <th style="padding:10px;text-align:left;
                                       font-size:12px;color:#6b7280">
                                RESULT
                            </th>
                            <th style="padding:10px;text-align:left;
                                       font-size:12px;color:#6b7280">
                                POINTS
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {checks_html}
                    </tbody>
                </table>

                <!-- Footer -->
                <div style="margin-top:24px;padding-top:16px;
                            border-top:1px solid #e5e7eb;
                            text-align:center">
                    <p style="color:#6b7280;font-size:12px;margin:0">
                        🕐 Checked at: {result.get('timestamp', 'N/A')}
                    </p>
                    <p style="color:#6b7280;font-size:12px;margin:4px 0 0">
                        This is an automated email from Assignment Checker Pipeline
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Send email
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print(f"✅ Email sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test with dummy result
    test_result = {
        "file": "test_paper.pdf",
        "type": "IEEE Research Paper",
        "score": 6,
        "max_score": 10,
        "status": "PASS",
        "timestamp": "18 Apr 2026 3:45 PM",
        "checks": [
            {"name": "Abstract", "passed": True,
             "points": 1, "message": "Found"},
            {"name": "Methodology", "passed": False,
             "points": 0, "message": "Missing"},
        ],
        "missing_sections": ["Methodology", "Discussion"],
        "present_sections": ["Abstract", "Introduction",
                            "Results", "Conclusion", "References"]
    }
    send_email(test_result, "test@gmail.com")