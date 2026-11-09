import sys
import importlib
import streamlit as st
import pandas as pd

for mod in ["components.theme", "components.sidebar", "backend.database"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_finding_glass_card,
    render_stat_card,
    render_html
)
from backend.ai_reviewer import review_code_with_gemini

st.set_page_config(
    page_title="AI Code Review Results | SmartCodeFlow",
    page_icon="🔍",
    layout="wide"
)

load_custom_css()
show_sidebar(active_page="Code Review")
render_top_header(active_page="Code Review")

render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'AI & Static <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Review Findings</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Comprehensive diagnostic audit generated via Google Gemini AI, Pylint, and Bandit security linters.'
    '</p>'
    '</div>'
)

# Fetch current analysis from session state, or generate from sample code
current_code = st.session_state.get("submitted_code", "")
current_file = st.session_state.get("current_file_name", "sample_buggy_code.py")

if not current_code:
    try:
        with open("sample_buggy_code.py", "r") as f:
            current_code = f.read()
    except Exception:
        current_code = "def sample(): pass"

review_resp = review_code_with_gemini(current_code, file_name=current_file)
findings = review_resp.get("findings", [])

crit = sum(1 for f in findings if f.get("severity") == "Critical")
high = sum(1 for f in findings if f.get("severity") == "High")
med = sum(1 for f in findings if f.get("severity") == "Medium")
low = sum(1 for f in findings if f.get("severity") == "Low")
score = max(15, 100 - ((crit * 25) + (high * 15) + (med * 8) + (low * 3)))

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_stat_card("Target File", current_file, "Active module", "neutral", "folder", "scf-stat-purple")
with c2:
    render_stat_card("Quality Score", f"{score}%", "Audit grade", "up", "diamond", "scf-stat-cyan")
with c3:
    render_stat_card("Critical Bugs", str(crit + high), "Requires fix", "down", "bug", "scf-stat-coral")
with c4:
    render_stat_card("Total Findings", str(len(findings)), "Linters & AI", "neutral", "chart", "scf-stat-amber")

st.markdown("---")

col_left, col_right = st.columns([1.2, 1.0], gap="large")

with col_left:
    render_html(f'<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">Diagnostic Findings ({len(findings)})</div>')
    for idx, f in enumerate(findings):
        render_finding_glass_card(f, index=idx)
        with st.expander(f"Suggested Patch for {f.get('title')}"):
            st.markdown(f"**Description:** {f.get('problem')}")
            st.code(f.get('suggested_fix', '# Suggested patch'), language="python")
            
            c_a, c_b = st.columns(2)
            with c_a:
                st.button("Accept Patch", key=f"p3_acc_{idx}", use_container_width=True)
            with c_b:
                st.button("Dismiss", key=f"p3_dis_{idx}", use_container_width=True)

with col_right:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">Submitted Source Code</div>')
    st.code(current_code, language="python", line_numbers=True)
    
    st.markdown("---")
    render_html(
        '<div style="background: rgba(255, 255, 255, 0.60); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 16px; padding: 16px;">'
        '<div style="font-size: 0.85rem; font-weight: 700; color: #8B1E3F; margin-bottom: 6px;">Automated Linter Status</div>'
        '<div style="font-size: 0.80rem; color: #423E4B; margin-bottom: 4px;">• Pylint Coding Standards: <strong>Checked</strong></div>'
        '<div style="font-size: 0.80rem; color: #423E4B; margin-bottom: 4px;">• Bandit AST Security Scanner: <strong>Active</strong></div>'
        '<div style="font-size: 0.80rem; color: #423E4B;">• Gemini Semantic Reasoning: <strong>Synchronized</strong></div>'
        '</div>'
    )
