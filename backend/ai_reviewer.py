import os
import json
import ast
import re

# Safely attempt to load dotenv if available, else fallback cleanly
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_gemini_api_key():
    """Retrieve Gemini API key from environment or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            key = ""
    return key

def run_ast_heuristic_review(code_snippet: str, file_name: str = "module.py"):
    """Robust fallback AST and semantic analyzer when Gemini API is unavailable or offline."""
    findings = []
    lines = code_snippet.splitlines()
    total_lines = len(lines)
    
    # 1. Regex & Pattern Checks across lines
    for idx, line in enumerate(lines, start=1):
        # Division by zero risk
        if re.search(r'/\s*0(?!\d)', line):
            findings.append({
                "id": f"BUG-{idx}",
                "title": "Division by Zero Detected",
                "severity": "Critical",
                "category": "Bug Detection",
                "line": idx,
                "problem": "Explicit division by zero causes a ZeroDivisionError at runtime.",
                "suggested_fix": line.replace("/ 0", "/ 1  # Verify denominator is non-zero")
            })
        elif re.search(r'/\s*[a-zA-Z_]\w*', line) and "len(" in line and "if len(" not in line:
            findings.append({
                "id": f"BUG-{idx}",
                "title": "Potential Division by Empty Sequence",
                "severity": "High",
                "category": "Bug Detection",
                "line": idx,
                "problem": "Dividing by length of an unvalidated collection may raise ZeroDivisionError if empty.",
                "suggested_fix": f"if len(numbers) > 0:\n    {line.strip()}\nelse:\n    return 0"
            })
            
        # Hardcoded credentials
        if re.search(r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
            findings.append({
                "id": f"SEC-{idx}",
                "title": "Hardcoded Credential or Secret",
                "severity": "High",
                "category": "Security Vulnerability",
                "line": idx,
                "problem": "Hardcoded secrets in source files risk credential exposure in version control.",
                "suggested_fix": line.split("=")[0].strip() + ' = os.getenv("' + line.split("=")[0].strip().upper() + '")'
            })
            
        # SQL Injection risks
        if re.search(r'SELECT\s+.*(format\(|f["\']|\+|%s)', line, re.IGNORECASE):
            findings.append({
                "id": f"SEC-SQL-{idx}",
                "title": "SQL Injection Vulnerability",
                "severity": "Critical",
                "category": "Security Vulnerability",
                "line": idx,
                "problem": "Dynamic string interpolation inside SQL queries permits injection attacks.",
                "suggested_fix": 'cursor.execute("SELECT * FROM table WHERE id = ?", (user_id,))'
            })
            
        # Print statements in production code
        if re.search(r'^\s*print\(', line):
            findings.append({
                "id": f"SMELL-{idx}",
                "title": "Unstructured Print Statement",
                "severity": "Low",
                "category": "Code Smell",
                "line": idx,
                "problem": "Direct print() calls lack log-level filtering and structured timestamping.",
                "suggested_fix": line.replace("print(", "logger.info(")
            })

    # 2. Python AST Analysis
    try:
        tree = ast.parse(code_snippet)
        for node in ast.walk(tree):
            # Bare except clause
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    findings.append({
                        "id": f"MAINT-{getattr(node, 'lineno', 1)}",
                        "title": "Bare Exception Handler",
                        "severity": "Medium",
                        "category": "Maintainability Issue",
                        "line": getattr(node, "lineno", 1),
                        "problem": "Handling bare 'except:' catches system exits and hides unintended defects.",
                        "suggested_fix": "except Exception as exc:\n    logger.error(f'Error occurred: {exc}')"
                    })
            # Missing function docstrings
            elif isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    findings.append({
                        "id": f"DOC-{node.lineno}",
                        "title": f"Missing Docstring in `{node.name}()`",
                        "severity": "Informational",
                        "category": "Recommended Improvement",
                        "line": node.lineno,
                        "problem": f"Public function `{node.name}` does not specify parameter or return semantics.",
                        "suggested_fix": f'"""Execute {node.name} workflow.\\n\\nReturns:\\n    Result value.\\n"""'
                    })
    except Exception:
        pass
        
    return {"findings": findings}

def review_code_with_gemini(code_snippet, file_name="module.py"):
    """Use Google Gemini AI to perform a deep semantic review, falling back to AST analyzer."""
    api_key = get_gemini_api_key()
    if not api_key:
        return run_ast_heuristic_review(code_snippet, file_name)
        
    prompt = f"""
    You are an expert Principal Software Engineer and Security Auditor. 
    Analyze the following code ({file_name}) and return code review findings in strict valid JSON format.
    
    Code:
    ```
    {code_snippet}
    ```
    
    Return a JSON object containing a list of findings under the key "findings". Each finding must have:
    - "id": string like "BUG-1"
    - "title": Short description of the issue
    - "severity": "Critical", "High", "Medium", "Low", or "Informational"
    - "category": e.g., "Bug Detection", "Security Vulnerability", "Code Smell", "Maintainability Issue", "Complexity Analysis", "Recommended Improvement"
    - "line": Integer line number
    - "problem": Explanation of why this is an issue
    - "suggested_fix": Concrete code recommendation or fix
    """
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        parsed = json.loads(text)
        if isinstance(parsed, dict) and "findings" in parsed:
            return parsed
        return run_ast_heuristic_review(code_snippet, file_name)
    except Exception:
        return run_ast_heuristic_review(code_snippet, file_name)
