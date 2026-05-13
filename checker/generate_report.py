import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from checker.check_pdf import check_pdf
from checker.check_code import check_code
from checker.check_ieee import check_ieee

RESULTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dashboard", "results.json"
)

def is_ieee_paper(filepath):
    """Quick check if PDF looks like IEEE paper"""
    try:
        with open(filepath, "rb") as f:
            import PyPDF2
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:3]:
                try:
                    text += page.extract_text().lower()
                except:
                    pass
            ieee_indicators = ["ieee", "abstract", "index terms", "doi"]
            return sum(1 for i in ieee_indicators if i in text) >= 2
    except:
        return False

def detect_and_check(submissions_folder="submissions"):
    """Detects file type and runs appropriate checker"""
    submission_file = None
    for f in os.listdir(submissions_folder):
        if f.endswith(".pdf") or f.endswith(".py"):
            if f != ".gitkeep":
                submission_file = os.path.join(submissions_folder, f)
                break

    if not submission_file:
        print("❌ No submission file found!")
        sys.exit(1)

    print(f"📁 Found submission: {submission_file}")

    # Run correct checker
    if submission_file.endswith(".pdf"):
        if is_ieee_paper(submission_file):
            print("📄 Detected: IEEE Research Paper")
            result = check_ieee(submission_file)
        else:
            print("📄 Detected: Regular PDF submission")
            result = check_pdf(submission_file)
    elif submission_file.endswith(".py"):
        print("🐍 Detected: Python code submission")
        result = check_code(submission_file)

    # Add timestamp
    result["timestamp"] = datetime.now().strftime("%d %b %Y %I:%M %p")
    result["filename"] = os.path.basename(submission_file)

    # Save results
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

    # Print missing sections for IEEE
    if result.get("missing_sections"):
        print(f"\n⚠️  Missing sections: {', '.join(result['missing_sections'])}")

    return result

def save_result(result):
    """Save result to results.json"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {"results": []}
    else:
        data = {"results": []}

    data["results"].insert(0, result)
    data["results"] = data["results"][:20]
    data["latest"] = result

    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Result saved to results.json")

if __name__ == "__main__":
    detect_and_check()