import subprocess
import os
import ast

# Required functions student must implement
REQUIRED_FUNCTIONS = ["main"]

def check_code(filepath):
    """
    Checks a Python file and returns score out of 10
    """
    results = {
        "file": os.path.basename(filepath),
        "type": "Python Code",
        "checks": [],
        "score": 0,
        "max_score": 10,
        "status": "FAIL"
    }

    # ── CHECK 1: File exists and not empty (2 points) ──
    try:
        with open(filepath, "r") as f:
            code = f.read()

        if len(code.strip()) > 10:
            results["checks"].append({
                "name": "File is not empty",
                "passed": True,
                "points": 2,
                "message": f"File has {len(code.split())} words of code"
            })
            results["score"] += 2
        else:
            results["checks"].append({
                "name": "File is not empty",
                "passed": False,
                "points": 0,
                "message": "File is empty or too short"
            })
            return results

    except Exception as e:
        results["checks"].append({
            "name": "File is not empty",
            "passed": False,
            "points": 0,
            "message": f"Could not read file: {str(e)}"
        })
        return results

    # ── CHECK 2: Valid Python syntax (2 points) ──
    try:
        ast.parse(code)
        results["checks"].append({
            "name": "Valid Python syntax",
            "passed": True,
            "points": 2,
            "message": "No syntax errors found"
        })
        results["score"] += 2
    except SyntaxError as e:
        results["checks"].append({
            "name": "Valid Python syntax",
            "passed": False,
            "points": 0,
            "message": f"Syntax error at line {e.lineno}: {e.msg}"
        })

    # ── CHECK 3: Code runs without errors (2 points) ──
    try:
        run = subprocess.run(
            ["python", filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if run.returncode == 0:
            results["checks"].append({
                "name": "Code runs without errors",
                "passed": True,
                "points": 2,
                "message": "Code executed successfully"
            })
            results["score"] += 2
        else:
            results["checks"].append({
                "name": "Code runs without errors",
                "passed": False,
                "points": 0,
                "message": f"Runtime error: {run.stderr[:100]}"
            })
    except subprocess.TimeoutExpired:
        results["checks"].append({
            "name": "Code runs without errors",
            "passed": False,
            "points": 0,
            "message": "Code took too long to run (timeout 10s)"
        })

    # ── CHECK 4: Required functions exist (2 points) ──
    try:
        tree = ast.parse(code)
        functions = [n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)]
        found = [f for f in REQUIRED_FUNCTIONS if f in functions]

        if len(found) == len(REQUIRED_FUNCTIONS):
            results["checks"].append({
                "name": "Required functions present",
                "passed": True,
                "points": 2,
                "message": f"Found functions: {', '.join(found)}"
            })
            results["score"] += 2
        else:
            missing = [f for f in REQUIRED_FUNCTIONS if f not in functions]
            results["checks"].append({
                "name": "Required functions present",
                "passed": False,
                "points": 0,
                "message": f"Missing functions: {', '.join(missing)}"
            })
    except Exception:
        pass

    # ── CHECK 5: Has comments/documentation (2 points) ──
    comment_lines = [l for l in code.split("\n")
                    if l.strip().startswith("#") or '"""' in l]
    if len(comment_lines) >= 2:
        results["checks"].append({
            "name": "Has comments/documentation",
            "passed": True,
            "points": 2,
            "message": f"Found {len(comment_lines)} comment lines"
        })
        results["score"] += 2
    else:
        results["checks"].append({
            "name": "Has comments/documentation",
            "passed": False,
            "points": 0,
            "message": "Not enough comments — add at least 2 comments"
        })

    results["status"] = "PASS" if results["score"] >= 6 else "FAIL"
    return results


if __name__ == "__main__":
    result = check_code("../submissions/assignment.py")
    print(result)