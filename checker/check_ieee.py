import PyPDF2
import os
import re

# All IEEE sections to check
IEEE_SECTIONS = [
    "abstract",
    "introduction",
    "methodology",
    "results",
    "discussion",
    "conclusion",
    "references"
]

def check_ieee(filepath):
    """
    Checks if PDF is an IEEE research paper
    and validates all required sections
    """
    results = {
        "file": os.path.basename(filepath),
        "type": "IEEE Research Paper",
        "checks": [],
        "score": 0,
        "max_score": 10,
        "status": "FAIL",
        "missing_sections": [],
        "present_sections": [],
        "details": {}
    }

    # ── CHECK 1: Can we open the PDF? ──
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages = reader.pages
            num_pages = len(pages)

            # Extract full text
            full_text = ""
            for page in pages:
                try:
                    full_text += page.extract_text().lower()
                except:
                    pass

            # ── CHECK 2: Is it an IEEE paper? ──
            ieee_indicators = [
                "ieee", "abstract", "index terms",
                "doi", "arxiv", "proceedings"
            ]
            ieee_score = sum(1 for i in ieee_indicators if i in full_text)

            if ieee_score >= 2:
                results["checks"].append({
                    "name": "Valid IEEE Paper Format",
                    "passed": True,
                    "points": 1,
                    "message": f"IEEE indicators found: {ieee_score}/6"
                })
                results["score"] += 1
            else:
                results["checks"].append({
                    "name": "Valid IEEE Paper Format",
                    "passed": False,
                    "points": 0,
                    "message": "Does not appear to be an IEEE format paper"
                })

            # ── CHECK 3: Check all sections (1 point each) ──
            for section in IEEE_SECTIONS:
                # Check variations of section names
                variations = [
                    section,
                    section.upper(),
                    section.title(),
                    f"{section}s",
                    f"ii. {section}",
                    f"i. {section}",
                ]

                found = any(v in full_text for v in variations)

                if found:
                    results["checks"].append({
                        "name": f"Section: {section.title()}",
                        "passed": True,
                        "points": 1,
                        "message": f"{section.title()} section found ✅"
                    })
                    results["score"] += 1
                    results["present_sections"].append(section.title())
                else:
                    results["checks"].append({
                        "name": f"Section: {section.title()}",
                        "passed": False,
                        "points": 0,
                        "message": f"{section.title()} section MISSING ❌"
                    })
                    results["missing_sections"].append(section.title())

            # ── CHECK 4: Page count ──
            results["details"]["pages"] = num_pages
            results["details"]["word_count"] = len(full_text.split())
            results["details"]["present_sections"] = results["present_sections"]
            results["details"]["missing_sections"] = results["missing_sections"]

    except Exception as e:
        results["checks"].append({
            "name": "File Readable",
            "passed": False,
            "points": 0,
            "message": f"Could not open PDF: {str(e)}"
        })

    # Set status
    results["status"] = "PASS" if results["score"] >= 7 else "FAIL"
    return results


if __name__ == "__main__":
    result = check_ieee("../submissions/assignment.pdf")
    import json
    print(json.dumps(result, indent=2))