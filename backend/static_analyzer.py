import subprocess
import json
import os

def run_pylint(file_path):
    """Run Pylint on a Python file and return structured findings."""
    try:
        # Run pylint with json output format
        cmd = ["pylint", "--output-format=json", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            return json.loads(result.stdout)
        return []
    except Exception as e:
        return [{"type": "error", "message": f"Pylint execution failed: {str(e)}"}]

def run_bandit(file_path):
    """Run Bandit security linter on a Python file and return security findings."""
    try:
        # Run bandit with json format output
        cmd = ["bandit", "-f", "json", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            data = json.loads(result.stdout)
            return data.get("results", [])
        return []
    except Exception as e:
        return [{"issue_text": f"Bandit execution failed: {str(e)}"}]

def analyze_file(file_path):
    """Run both static analyzers on a single file and aggregate results."""
    pylint_results = run_pylint(file_path)
    bandit_results = run_bandit(file_path)
    
    return {
        "file": file_path,
        "pylint_issues": pylint_results,
        "bandit_issues": bandit_results
    }