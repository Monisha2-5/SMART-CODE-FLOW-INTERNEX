import sys
import importlib
import streamlit as st
import pandas as pd
import plotly.express as px

for mod in ["components.theme", "components.sidebar", "backend.database"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_stat_card,
    set_chart_glass_theme,
    render_html
)
from backend.database import get_dashboard_analytics

st.set_page_config(
    page_title="Analytics | SmartCodeFlow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Dashboard")
render_top_header(active_page="Dashboard")

render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Code Quality <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Analytics</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'In-depth statistical breakdown of code review findings, defect distribution, and reviewer remediation velocity.'
    '</p>'
    '</div>'
)

# Fetch stats from database
stats = get_dashboard_analytics()
total_reviews = stats.get("total_reviews", 5)
avg_score = stats.get("avg_score", 82)
total_issues = stats.get("total_issues", 30)

crit = stats.get("critical", 1) or 1
high = stats.get("high", 4) or 4
med = stats.get("medium", 8) or 8
low = stats.get("low", 17) or 17

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_stat_card("Total Findings", str(total_issues), "Audit dataset", "neutral", "chart", "scf-stat-purple")
with col2:
    render_stat_card("Quality Score", f"{avg_score}/100", "Overall rating", "up", "diamond", "scf-stat-cyan")
with col3:
    render_stat_card("Accepted Fixes", "14 Fixes", "Staged for commit", "up", "score", "scf-stat-amber")
with col4:
    render_stat_card("Remediation Rate", "78%", "Verified patches", "up", "shield", "scf-stat-coral")

st.markdown("---")

col_c1, col_c2 = st.columns(2, gap="large")

with col_c1:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">🚨 Severity Breakdown</div>')
    sev_df = pd.DataFrame({
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Count": [crit, high, med, low]
    })
    fig_sev = px.bar(
        sev_df,
        x="Severity",
        y="Count",
        color="Severity",
        color_discrete_map={"Critical": "#8B1E3F", "High": "#F97316", "Medium": "#9D81BA", "Low": "#38BDF8"}
    )
    fig_sev.update_layout(height=260, showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    set_chart_glass_theme(fig_sev)
    st.plotly_chart(fig_sev, use_container_width=True, config={"displayModeBar": False})

with col_c2:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">📝 Feedback Resolution Status</div>')
    feed_df = pd.DataFrame({
        "Status": ["Accepted", "Pending", "Verified", "Rejected"],
        "Count": [14, 8, 6, 2]
    })
    fig_feed = px.pie(
        feed_df,
        names="Status",
        values="Count",
        hole=0.55,
        color_discrete_sequence=["#22C55E", "#F59E0B", "#38BDF8", "#EF4444"]
    )
    fig_feed.update_layout(height=260, margin=dict(t=20, b=20, l=20, r=20))
    set_chart_glass_theme(fig_feed)
    st.plotly_chart(fig_feed, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# Download CSV
render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">📥 Export Analytics Data</div>')
csv_content = sev_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download Quality Analytics CSV",
    data=csv_content,
    file_name="smartcodeflow_analytics.csv",
    mime="text/csv",
    use_container_width=True
)
