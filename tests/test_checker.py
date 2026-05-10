import pytest
import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from checker.check_code import check_code
from checker.generate_report import save_result

# Create a temp good Python file for testing
GOOD_CODE = '''
# This is a sample assignment
# Written by student

def main():
    """Main function"""
    print("Hello from assignment!")
    return True

if __name__ == "__main__":
    main()
'''

# Create a temp bad Python file for testing
BAD_CODE = "x = ("  # syntax error

def create_temp_file(content, filename="temp_test.py"):
    with open(filename, "w") as f:
        f.write(content)
    return filename

def test_good_code_passes():
    """Good code should score at least 6/10"""
    f = create_temp_file(GOOD_CODE, "temp_good.py")
    result = check_code(f)
    os.remove(f)
    assert result["score"] >= 6

def test_bad_code_fails():
    """Bad code with syntax error should score low"""
    f = create_temp_file(BAD_CODE, "temp_bad.py")
    result = check_code(f)
    os.remove(f)
    assert result["score"] < 6

def test_result_has_required_keys():
    """Result must have all required fields"""
    f = create_temp_file(GOOD_CODE, "temp_keys.py")
    result = check_code(f)
    os.remove(f)
    assert "score" in result
    assert "status" in result
    assert "checks" in result
    assert "file" in result

def test_pass_status_when_high_score():
    """High scoring code should have PASS status"""
    f = create_temp_file(GOOD_CODE, "temp_pass.py")
    result = check_code(f)
    os.remove(f)
    assert result["status"] == "PASS"

def test_dashboard_health():
    """Dashboard app health check"""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dashboard'))
    from app import app
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200