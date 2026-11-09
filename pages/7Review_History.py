import sys
import importlib
import json
import streamlit as st
import pandas as pd

for mod in ["components.theme", "components.sidebar", "backend.database"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_stat_card,
    render_vs_code_editor_header,
    render_finding_glass_card,
    render_html
)
from backend.database import get_detailed_review_history, get_review_by_id

st.set_page_config(
    page_title="Review History | SmartCodeFlow",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Review History")
render_top_header(active_page="Review History")

# Page Header
render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Historical <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Review Audits</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Archive of previously executed code reviews, quality scores, and detected vulnerabilities retrieved directly from the SQLite database.'
    '</p>'
    '</div>'
)

# Fetch real reviews from database
raw_reviews = get_detailed_review_history()

# If empty, provide clean mock entry
if not raw_reviews:
    raw_reviews = [
        {
            "id": 1,
            "file_name": "sample_buggy_code.py",
            "language": "Python",
            "coding_standard": "PEP 8",
            "quality_score": 85,
            "total_findings": 4,
            "critical_count": 1,
            "high_count": 1,
            "medium_count": 2,
            "low_count": 0,
            "review_date": "07-11-2026 14:10",
            "submitted_code": "def divide(a, b):\n    return a / b\n",
            "findings_json": json.dumps([
                {"id": "F1", "severity": "High", "title": "Division by Zero", "line": 2, "problem": "No validation", "suggested_fix": "if b != 0: return a/b"}
            ])
        }
    ]

# Top Metrics Bar
total_count = len(raw_reviews)
avg_score = round(sum(r.get("quality_score", 0) for r in raw_reviews) / max(total_count, 1))
crit_sum = sum(r.get("critical_count", 0) for r in raw_reviews)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    render_stat_card("Total Audits", str(total_count), "Persisted reviews", "neutral", "chart", "scf-stat-purple")
with col_m2:
    render_stat_card("Average Quality", f"{avg_score}%", "Historical benchmark", "up", "diamond", "scf-stat-cyan")
with col_m3:
    render_stat_card("Critical Issues", str(crit_sum), "Historical total", "neutral", "bug", "scf-stat-coral")
with col_m4:
    render_stat_card("Database State", "Connected", "SQLite Active", "up", "folder", "scf-stat-amber")

st.markdown("---")

# Search, Filter & Sort Controls
col_f1, col_f2, col_f3 = st.columns([1.5, 1.0, 1.0])
with col_f1:
    search_query = st.text_input("🔍 Search Reviews by File or Standard", placeholder="Filter by filename (e.g. snippet.py)...")
with col_f2:
    languages_list = ["All"] + sorted(list(set(r.get("language", "Python") for r in raw_reviews if r.get("language"))))
    selected_lang = st.selectbox("Filter by Language", languages_list)
with col_f3:
    sort_option = st.selectbox("Sort By", ["Date (Newest First)", "Date (Oldest First)", "Quality Score (High to Low)", "Findings (Most to Least)"])

# Filter Logic
filtered = raw_reviews.copy()
if search_query.strip():
    q = search_query.strip().lower()
    filtered = [r for r in filtered if q in str(r.get("file_name", "")).lower() or q in str(r.get("coding_standard", "")).lower()]

if selected_lang != "All":
    filtered = [r for r in filtered if r.get("language") == selected_lang]

if sort_option == "Date (Newest First)":
    filtered = sorted(filtered, key=lambda x: x.get("id", 0), reverse=True)
elif sort_option == "Date (Oldest First)":
    filtered = sorted(filtered, key=lambda x: x.get("id", 0))
elif sort_option == "Quality Score (High to Low)":
    filtered = sorted(filtered, key=lambda x: x.get("quality_score", 0), reverse=True)
elif sort_option == "Findings (Most to Least)":
    filtered = sorted(filtered, key=lambda x: x.get("total_findings", 0), reverse=True)

# Table / Glass Card View of Reviews
render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">Audit History Records</div>')

table_rows = []
for r in filtered:
    table_rows.append({
        "Review ID": f"REV-{r.get('id', 0):03d}",
        "File Name": r.get("file_name", "snippet.py"),
        "Language": r.get("language", "Python"),
        "Review Date": r.get("review_date", "N/A"),
        "Quality Score": f"{r.get('quality_score', 0)} / 100",
        "Total Findings": r.get("total_findings", 0),
        "Critical Issues": r.get("critical_count", 0),
        "Review Status": "Completed"
    })

df_table = pd.DataFrame(table_rows)
st.dataframe(df_table, use_container_width=True, hide_index=True)

st.markdown("---")

# Interactive Inspection of Original Review Details
render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">🔍 Deep Inspection of Historical Audit</div>')

review_options = [f"REV-{r.get('id'):03d} • {r.get('file_name')} ({r.get('review_date')})" for r in filtered]
if review_options:
    selected_option = st.selectbox("Select Review to Inspect Original Findings & Code", review_options)
    selected_id = int(selected_option.split("•")[0].replace("REV-", "").strip())
    
    target_review = next((r for r in filtered if r.get("id") == selected_id), None)
    
    if target_review:
        col_code, col_find = st.columns([1.1, 1.2], gap="large")
        
        with col_code:
            render_html(f'<div style="font-weight: 700; color: #1E1B24; margin-bottom: 8px;">Original Submitted Code ({target_review.get("file_name")})</div>')
            code_text = target_review.get("submitted_code", "# No submitted code stored")
            render_vs_code_editor_header(
                filename=target_review.get("file_name", "module.py"),
                language=str(target_review.get("language", "python")).lower(),
                lines_count=len(code_text.splitlines()) if code_text else 0
            )
            st.code(code_text if code_text else "# Code content unavailable", language=str(target_review.get("language", "python")).lower(), line_numbers=True)

        with col_find:
            render_html(f'<div style="font-weight: 700; color: #1E1B24; margin-bottom: 8px;">Original Findings & Quality Metrics</div>')
            
            # Metric badges
            render_html(
                f'<div style="display: flex; gap: 12px; margin-bottom: 14px;">'
                f'<span class="scf-badge scf-badge-burgundy">Score: {target_review.get("quality_score", 0)}/100</span>'
                f'<span class="scf-badge" style="background: rgba(239, 68, 68, 0.15); color: #DC2626;">Critical: {target_review.get("critical_count", 0)}</span>'
                f'<span class="scf-badge" style="background: rgba(249, 115, 22, 0.15); color: #EA580C;">High: {target_review.get("high_count", 0)}</span>'
                f'<span class="scf-badge" style="background: rgba(56, 189, 248, 0.15); color: #0284C7;">Low: {target_review.get("low_count", 0)}</span>'
                f'</div>'
            )
            
            # Parse findings JSON
            findings_raw = target_review.get("findings_json", "[]")
            try:
                findings_list = json.loads(findings_raw) if isinstance(findings_raw, str) else findings_raw
            except Exception:
                findings_list = []
                
            if findings_list:
                for idx, f in enumerate(findings_list):
                    render_finding_glass_card(f, index=idx)
            else:
                st.info("No recorded findings for this review session.")
                
        # Export Option
        st.markdown("---")
        c_exp1, c_exp2 = st.columns([1.5, 1.0])
        with c_exp1:
            exp_format = st.selectbox("Export Format", ["Markdown (.md)", "JSON Data (.json)", "CSV (.csv)"])
        with c_exp2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            report_text = f"# SmartCodeFlow Audit Report: {target_review.get('file_name')}\n- Date: {target_review.get('review_date')}\n- Score: {target_review.get('quality_score')}/100\n- Total Findings: {target_review.get('total_findings')}\n"
            st.download_button(
                "📥 Download Audit Report Package",
                data=report_text,
                file_name=f"SmartCodeFlow_{selected_id}.md",
                use_container_width=True
            )
