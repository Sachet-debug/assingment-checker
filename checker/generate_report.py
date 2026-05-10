import json
import os
import sys
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from checker.check_pdf import check_pdf
from checker.check_code import check_code

RESULTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dashboard", "results.json"
)

def detect_and_check(submissions_folder="submissions"):
    """
    Detects file type and runs appropriate checker
    """
    # Find submission file
    submission_file = None
    for f in os.listdir(submissions_folder):
        if f.endswith(".pdf") or f.endswith(".py"):
            if f != ".gitkeep":
                submission_file = os.path.join(submissions_folder, f)
                break

    if not submission_file:
        print("❌ No submission file found in submissions/ folder!")
        sys.exit(1)

    print(f"📁 Found submission: {submission_file}")

    # Run correct checker based on file type
    if submission_file.endswith(".pdf"):
        print("📄 Detected: PDF submission")
        result = check_pdf(submission_file)
    elif submission_file.endswith(".py"):
        print("🐍 Detected: Python code submission")
        result = check_code(submission_file)

    # Add timestamp
    result["timestamp"] = datetime.now().strftime("%d %b %Y %I:%M %p")
    result["filename"] = os.path.basename(submission_file)

    # Save to results.json
    save_result(result)

    # Print summary
    print("\n" + "="*40)
    print(f"📊 RESULT: {result['file']}")
    print(f"⭐ Score: {result['score']}/{result['max_score']}")
    print(f"{'✅ PASS' if result['status'] == 'PASS' else '❌ FAIL'}")
    print("="*40)

    for check in result["checks"]:
        icon = "✅" if check["passed"] else "❌"
        print(f"{icon} {check['name']}: {check['message']}")

    return result

def save_result(result):
    """Save result to results.json for dashboard"""
    # Load existing results
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {"results": []}
    else:
        data = {"results": []}

    # Add new result at top
    data["results"].insert(0, result)

    # Keep only last 20 results
    data["results"] = data["results"][:20]
    data["latest"] = result

    # Save back
    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Result saved to results.json")

if __name__ == "__main__":
    detect_and_check()