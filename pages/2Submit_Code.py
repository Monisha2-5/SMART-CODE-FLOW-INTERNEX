import sys
import importlib
import streamlit as st
import pandas as pd
import zipfile
import io
import json

for mod in ["components.theme", "components.sidebar", "backend.database", "backend.ai_reviewer"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_vs_code_editor_header,
    render_finding_glass_card,
    render_stat_card,
    render_html
)
from backend.ai_reviewer import review_code_with_gemini
from backend.database import save_full_review

st.set_page_config(
    page_title="AI Code Review | SmartCodeFlow",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Code Review")
render_top_header(active_page="Code Review")

# Page Header
render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'AI-Powered <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Code Review</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Submit source code to inspect bugs, security vulnerabilities, code smells, and get AI-assisted refactoring fixes.'
    '</p>'
    '</div>'
)

# Initialize Session State
if "submitted_code" not in st.session_state:
    # Load sample buggy code by default if available for immediate demonstration
    try:
        with open("sample_buggy_code.py", "r", encoding="utf-8") as f:
            st.session_state.submitted_code = f.read()
    except Exception:
        st.session_state.submitted_code = ""

if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = "sample_buggy_code.py"

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Two-Column Split Layout (Left Panel: Input & VS Code Editor | Right Panel: AI Review & Findings)
left_panel, right_panel = st.columns([1.1, 1.15], gap="large")

with left_panel:
    render_html(
        '<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">'
        '<span style="color: #8B1E3F;">⚙️</span> Review Configuration & Code'
        '</div>'
    )
    
    # 1. Configuration Controls
    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    with col_cfg1:
        language = st.selectbox(
            "Language",
            ["Python", "Java", "JavaScript", "C++", "C", "TypeScript", "Go"],
            index=0
        )
    with col_cfg2:
        coding_standard = st.selectbox(
            "Standard",
            ["PEP 8", "Google Style Guide", "Clean Code", "Enterprise Security"],
            index=0
        )
    with col_cfg3:
        project_name = st.text_input("Project Name", value="SmartCodeFlow-Core")

    # 2. File Upload Box
    uploaded_file = st.file_uploader(
        "Upload Source File (or ZIP / Diff)",
        type=["py", "java", "js", "cpp", "c", "zip", "diff", "patch"],
        help="Upload single source code file, a ZIP archive, or patch file."
    )
    
    if uploaded_file is not None:
        st.session_state.current_file_name = uploaded_file.name
        if uploaded_file.name.endswith(".zip"):
            try:
                with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as z:
                    code_files = [n for n in z.namelist() if n.endswith((".py", ".java", ".js", ".c", ".cpp")) and not n.startswith("__")]
                    if code_files:
                        sub_file = st.selectbox("Select file inside ZIP", code_files)
                        st.session_state.submitted_code = z.read(sub_file).decode("utf-8", errors="replace")
                        st.session_state.current_file_name = sub_file
            except Exception as e:
                st.error(f"ZIP error: {e}")
        else:
            st.session_state.submitted_code = uploaded_file.getvalue().decode("utf-8", errors="replace")

    # 3. Professional VS Code-Style Dark Code Editor inside Light Glass Interface
    code_text = st.session_state.submitted_code
    lines_count = len(code_text.splitlines()) if code_text else 0
    render_vs_code_editor_header(
        filename=st.session_state.current_file_name,
        language=language.lower(),
        lines_count=lines_count
    )
    
    # Code Text Area styled as code editor
    code_input = st.text_area(
        label="VS Code Workspace",
        value=st.session_state.submitted_code,
        height=320,
        label_visibility="collapsed",
        placeholder="# Paste or type code here for AI analysis..."
    )
    st.session_state.submitted_code = code_input

    # 4. Analyze Code Button with Burgundy Rose Gradient
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Analyze Code & Run AI Review", type="primary", use_container_width=True)

    if analyze_clicked:
        if not code_input.strip():
            st.warning("Please upload or paste some code first.")
        else:
            with st.spinner("AI Engine & Linters inspecting source code..."):
                review_resp = review_code_with_gemini(code_input, file_name=st.session_state.current_file_name)
                findings = review_resp.get("findings", [])
                
                # Compute quality score & counts
                crit = sum(1 for f in findings if f.get("severity") == "Critical")
                high = sum(1 for f in findings if f.get("severity") == "High")
                med = sum(1 for f in findings if f.get("severity") == "Medium")
                low = sum(1 for f in findings if f.get("severity") == "Low")
                info = sum(1 for f in findings if f.get("severity") == "Informational")
                
                deduction = (crit * 25) + (high * 15) + (med * 8) + (low * 3) + (info * 1)
                score = max(10, 100 - deduction)
                
                st.session_state.analysis_results = {
                    "score": score,
                    "findings": findings,
                    "critical": crit,
                    "high": high,
                    "medium": med,
                    "low": low,
                    "info": info,
                    "file_name": st.session_state.current_file_name,
                    "language": language,
                    "coding_standard": coding_standard
                }
                
                # Persist to database
                save_full_review(
                    file_name=st.session_state.current_file_name,
                    language=language,
                    coding_standard=coding_standard,
                    quality_score=score,
                    total_findings=len(findings),
                    critical_count=crit,
                    high_count=high,
                    medium_count=med,
                    low_count=low,
                    submitted_code=code_input,
                    findings_json=findings
                )
                st.success("Review complete and saved to Review History!")

with right_panel:
    render_html(
        '<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">'
        '<span style="color: #8B1E3F;">🔍</span> AI Review Findings & Quality Report'
        '</div>'
    )
    
    # Check if analysis has been performed or load initial demo findings
    results = st.session_state.analysis_results
    
    if not results:
        # Pre-populate demo findings on initial load so the panel is stunning right away
        res = review_code_with_gemini(st.session_state.submitted_code, st.session_state.current_file_name)
        demo_findings = res.get("findings", [])
        crit = sum(1 for f in demo_findings if f.get("severity") == "Critical")
        high = sum(1 for f in demo_findings if f.get("severity") == "High")
        med = sum(1 for f in demo_findings if f.get("severity") == "Medium")
        low = sum(1 for f in demo_findings if f.get("severity") == "Low")
        info = sum(1 for f in demo_findings if f.get("severity") == "Informational")
        score = max(15, 100 - ((crit * 25) + (high * 15) + (med * 8) + (low * 3)))
        results = {
            "score": score,
            "findings": demo_findings,
            "critical": crit,
            "high": high,
            "medium": med,
            "low": low,
            "info": info,
            "file_name": st.session_state.current_file_name,
            "language": language,
            "coding_standard": coding_standard
        }
        st.session_state.analysis_results = results

    score = results.get("score", 85)
    findings = results.get("findings", [])
    
    # 1. AI Review Summary & Score Bar
    render_html(
        f'<div style="background: rgba(255, 255, 255, 0.65); backdrop-filter: blur(24px); border: 1.2px solid rgba(255, 255, 255, 0.85); border-radius: 20px; padding: 18px 22px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(110, 22, 51, 0.04);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
        f'<div>'
        f'<div style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #7A7585;">Overall Code Quality</div>'
        f'<div style="font-size: 2.1rem; font-weight: 800; color: #1E1B24; letter-spacing: -0.03em;">{score} <span style="font-size: 1.05rem; font-weight: 600; color: #7A7585;">/ 100</span></div>'
        f'</div>'
        f'<div style="text-align: right;">'
        f'<span class="scf-badge scf-badge-burgundy" style="font-size: 0.82rem; padding: 5px 14px;">{"A - Excellent" if score >= 85 else ("B - Moderate" if score >= 70 else "C - Action Required")}</span>'
        f'<div style="font-size: 0.75rem; color: #7A7585; margin-top: 5px;">{len(findings)} Total Findings</div>'
        f'</div>'
        f'</div>'
        f'<div style="width: 100%; height: 8px; background: rgba(217, 160, 176, 0.3); border-radius: 10px; overflow: hidden;">'
        f'<div style="width: {score}%; height: 100%; background: linear-gradient(90deg, #8B1E3F 0%, #C8B6FF 50%, #38BDF8 100%); border-radius: 10px;"></div>'
        f'</div>'
        f'</div>'
    )
    
    # 2. Metric Pills Breakdown: Bugs, Security, Smells, Maintainability, Complexity
    c_bug, c_sec, c_smell, c_maint = st.columns(4)
    with c_bug:
        render_html(
            f'<div style="background: rgba(255, 255, 255, 0.60); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 14px; padding: 10px 12px; text-align: center;">'
            f'<div style="font-size: 0.70rem; font-weight: 700; color: #EA580C; text-transform: uppercase;">Bugs</div>'
            f'<div style="font-size: 1.35rem; font-weight: 800; color: #1E1B24;">{results.get("high", 0) + results.get("critical", 0)}</div>'
            f'</div>'
        )
    with c_sec:
        render_html(
            f'<div style="background: rgba(255, 255, 255, 0.60); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 14px; padding: 10px 12px; text-align: center;">'
            f'<div style="font-size: 0.70rem; font-weight: 700; color: #DC2626; text-transform: uppercase;">Security</div>'
            f'<div style="font-size: 1.35rem; font-weight: 800; color: #1E1B24;">{results.get("critical", 0)}</div>'
            f'</div>'
        )
    with c_smell:
        render_html(
            f'<div style="background: rgba(255, 255, 255, 0.60); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 14px; padding: 10px 12px; text-align: center;">'
            f'<div style="font-size: 0.70rem; font-weight: 700; color: #0284C7; text-transform: uppercase;">Smells</div>'
            f'<div style="font-size: 1.35rem; font-weight: 800; color: #1E1B24;">{results.get("low", 0)}</div>'
            f'</div>'
        )
    with c_maint:
        render_html(
            f'<div style="background: rgba(255, 255, 255, 0.60); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 14px; padding: 10px 12px; text-align: center;">'
            f'<div style="font-size: 0.70rem; font-weight: 700; color: #7C3AED; text-transform: uppercase;">Maintain</div>'
            f'<div style="font-size: 1.35rem; font-weight: 800; color: #1E1B24;">{results.get("medium", 0) + results.get("info", 0)}</div>'
            f'</div>'
        )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    
    # 3. Findings Cards with Severity Badges & Expandable Fixes
    if not findings:
        st.success("✨ Zero issues detected! Your code adheres strictly to quality standards.")
    else:
        render_html(f'<div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; color: #7A7585; letter-spacing: 0.06em; margin-bottom: 8px;">Detected Findings ({len(findings)})</div>')
        for idx, finding in enumerate(findings):
            render_finding_glass_card(finding, index=idx)
            
            # Interactive Expandable Code Fix & Action Buttons
            with st.expander(f"Suggested Refactoring for {finding.get('title', 'Issue')}"):
                st.markdown(f"**Root Cause:** {finding.get('problem', '')}")
                st.markdown("**Proposed Fix:**")
                st.code(finding.get('suggested_fix', '# Apply input validation'), language=language.lower())
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("Accept Fix", key=f"btn_acc_{idx}"):
                        st.success("Fix accepted and scheduled for patch!")
                with col_btn2:
                    if st.button("Reject", key=f"btn_rej_{idx}"):
                        st.info("Finding dismissed.")
                with col_btn3:
                    if st.button("Verify", key=f"btn_ver_{idx}"):
                        st.warning("Flagged for senior engineer verification.")
