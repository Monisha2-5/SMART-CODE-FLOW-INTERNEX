import sys
import importlib
import time
import streamlit as st

for mod in ["components.theme", "components.sidebar"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_stat_card,
    render_html
)

st.set_page_config(
    page_title="Audit Reports | SmartCodeFlow",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Dashboard")
render_top_header(active_page="Dashboard")

render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Comprehensive <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Audit Reports</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Generate, view, and export executive-level security and maintainability summaries formatted for stakeholders and compliance audits.'
    '</p>'
    '</div>'
)

# Top Telemetry Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_stat_card("Report Scope", "Repository Audit", "Full project scan", "up", "folder", "scf-stat-purple")
with col2:
    render_stat_card("Audit Grade", "A- (88/100)", "High quality", "up", "diamond", "scf-stat-cyan")
with col3:
    render_stat_card("Compliance", "OWASP & PEP 8", "Passed rules", "up", "shield", "scf-stat-coral")
with col4:
    render_stat_card("Export Formats", "PDF, MD, JSON", "Stakeholder ready", "neutral", "chart", "scf-stat-amber")

st.markdown("---")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">⚙️ Report Parameters</div>')
    report_type = st.selectbox("Report Scope", ["Full Repository Audit", "Security & Vulnerabilities Only", "Code Maintainability Index"])
    report_format = st.selectbox("Export Format", ["Markdown (.md)", "JSON Data (.json)", "HTML Web Page (.html)"])
    
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    if st.button("📥 Generate & Download Report Package", type="primary", use_container_width=True):
        with st.spinner("Compiling full project analysis..."):
            time.sleep(1.2)
        sample_content = (
            f"# SmartCodeFlow Executive Audit Report\n"
            f"- Scope: {report_type}\n"
            f"- Generated Date: 2026-11-09\n"
            f"- Maintainability Score: 88/100\n"
            f"- Critical Findings: Parameterized query fixes suggested for SQL injection prevention.\n"
        )
        ext = "md" if "md" in report_format.lower() else ("json" if "json" in report_format.lower() else "html")
        st.download_button(
            label=f"Click to Save {ext.upper()} File",
            data=sample_content,
            file_name=f"SmartCodeFlow_Audit_Report.{ext}",
            use_container_width=True
        )
        st.success("Report generated and ready for download!")

with col_right:
    render_html(
        '<div style="background: rgba(255, 255, 255, 0.60); border: 1.2px solid rgba(255, 255, 255, 0.85); border-radius: 20px; padding: 22px 24px; box-shadow: 0 8px 24px rgba(110, 22, 51, 0.04);">'
        '<div style="font-weight: 800; font-size: 1.10rem; color: #1E1B24; margin-bottom: 10px;">Executive Summary Preview</div>'
        '<div style="font-size: 0.84rem; color: #423E4B; line-height: 1.6;">'
        '<strong>Audit Date:</strong> November 9, 2026<br>'
        '<strong>Analyzed Files:</strong> Python modules & project repository<br>'
        '<strong>Overall Maintainability:</strong> A- (88/100)<br>'
        '<strong>Critical Vulnerabilities:</strong> 1 (Division by Zero in <code>sample_buggy_code.py</code>)<br>'
        '<strong>PEP 8 Compliance:</strong> 96%<br>'
        '<strong>AST Security Status:</strong> Bandit clean with zero open high severity vulnerabilities after remediation.'
        '</div>'
        '</div>'
    )
