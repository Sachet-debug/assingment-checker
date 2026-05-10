import PyPDF2
import os

# Keywords that should be in assignment
REQUIRED_KEYWORDS = [
    "introduction",
    "conclusion",
    "references"
]

def check_pdf(filepath):
    """
    Checks a PDF file and returns a score out of 10
    with detailed breakdown
    """
    results = {
        "file": os.path.basename(filepath),
        "type": "PDF",
        "checks": [],
        "score": 0,
        "max_score": 10,
        "status": "FAIL"
    }

    # ── CHECK 1: Can we open the PDF? (2 points) ──
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages = reader.pages
            num_pages = len(pages)

            results["checks"].append({
                "name": "File is readable",
                "passed": True,
                "points": 2,
                "message": "PDF opened successfully"
            })
            results["score"] += 2

            # ── CHECK 2: Minimum 2 pages (2 points) ──
            if num_pages >= 2:
                results["checks"].append({
                    "name": "Minimum page count",
                    "passed": True,
                    "points": 2,
                    "message": f"PDF has {num_pages} pages"
                })
                results["score"] += 2
            else:
                results["checks"].append({
                    "name": "Minimum page count",
                    "passed": False,
                    "points": 0,
                    "message": f"PDF has only {num_pages} page — minimum 2 required"
                })

            # Extract all text from PDF
            full_text = ""
            for page in pages:
                full_text += page.extract_text().lower()

            # ── CHECK 3: Word count minimum 200 (2 points) ──
            word_count = len(full_text.split())
            if word_count >= 200:
                results["checks"].append({
                    "name": "Word count sufficient",
                    "passed": True,
                    "points": 2,
                    "message": f"Word count: {word_count} words"
                })
                results["score"] += 2
            else:
                results["checks"].append({
                    "name": "Word count sufficient",
                    "passed": False,
                    "points": 0,
                    "message": f"Only {word_count} words — minimum 200 required"
                })

            # ── CHECK 4: Required keywords (2 points) ──
            found_keywords = [k for k in REQUIRED_KEYWORDS if k in full_text]
            if len(found_keywords) >= 2:
                results["checks"].append({
                    "name": "Required keywords found",
                    "passed": True,
                    "points": 2,
                    "message": f"Found: {', '.join(found_keywords)}"
                })
                results["score"] += 2
            else:
                results["checks"].append({
                    "name": "Required keywords found",
                    "passed": False,
                    "points": 0,
                    "message": f"Missing keywords. Found only: {found_keywords}"
                })

            # ── CHECK 5: References section (2 points) ──
            if "references" in full_text or "bibliography" in full_text:
                results["checks"].append({
                    "name": "References section present",
                    "passed": True,
                    "points": 2,
                    "message": "References section found"
                })
                results["score"] += 2
            else:
                results["checks"].append({
                    "name": "References section present",
                    "passed": False,
                    "points": 0,
                    "message": "No references section found"
                })

    except Exception as e:
        results["checks"].append({
            "name": "File is readable",
            "passed": False,
            "points": 0,
            "message": f"Could not open PDF: {str(e)}"
        })

    # Set pass/fail status
    results["status"] = "PASS" if results["score"] >= 6 else "FAIL"
    return results


if __name__ == "__main__":
    # Test locally
    result = check_pdf("../submissions/assignment.pdf")
    print(result)