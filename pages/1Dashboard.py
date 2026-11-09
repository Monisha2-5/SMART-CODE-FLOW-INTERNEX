import sys
import importlib
import streamlit as st

for mod in ["components.theme", "components.sidebar", "backend.database"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from components.sidebar import show_sidebar
from components.theme import (
    load_custom_css,
    render_top_header,
    render_welcome_banner,
    render_stat_card,
    render_quick_action_cards,
    set_chart_glass_theme,
    render_html
)
from backend.database import get_dashboard_analytics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Executive Dashboard | SmartCodeFlow",
    page_icon="⚡",
    layout="wide"
)

load_custom_css()
show_sidebar(active_page="Dashboard")
render_top_header(active_page="Dashboard")
render_welcome_banner(
    title="Executive Dashboard",
    subtitle="High-level engineering telemetry, code security, and repository health.",
    filter_label="Overview ▾"
)

stats = get_dashboard_analytics()
total_reviews = stats.get("total_reviews", 5)
avg_score = stats.get("avg_score", 85)
total_issues = stats.get("total_issues", 30)
projects_count = stats.get("projects_count", 2)

left_col, right_col = st.columns([1.85, 1.0], gap="large")

with left_col:
    # Code Quality Trend
    timeline_df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Score": [68, 74, 79, 82, 85, 88]
    })
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=timeline_df["Month"],
        y=timeline_df["Score"],
        mode="lines+markers",
        name="Quality",
        line=dict(color="#8B1E3F", width=4, shape="spline"),
        marker=dict(size=8, color="#FFFFFF", line=dict(color="#8B1E3F", width=2.5)),
        fill="tozeroy",
        fillcolor="rgba(200, 182, 255, 0.28)"
    ))
    fig_line.update_layout(
        title=dict(text="<b>Code Quality Analytics</b>", font=dict(size=16, color="#1E1B24")),
        height=270,
        margin=dict(t=50, b=30, l=35, r=20),
        yaxis=dict(range=[50, 100])
    )
    set_chart_glass_theme(fig_line)
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        donut_df = pd.DataFrame({
            "Severity": ["Critical", "High", "Medium", "Low"],
            "Count": [stats.get("critical", 1) or 1, stats.get("high", 4) or 4, stats.get("medium", 6) or 6, stats.get("low", 12) or 12]
        })
        fig_donut = px.pie(
            donut_df,
            names="Severity",
            values="Count",
            hole=0.68,
            color="Severity",
            color_discrete_map={"Critical": "#8B1E3F", "High": "#F97316", "Medium": "#9D81BA", "Low": "#38BDF8"}
        )
        fig_donut.add_annotation(
            text=f"<b>{avg_score}%</b><br><span style='font-size:10px;color:#7A7585;'>Quality</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#1E1B24")
        )
        fig_donut.update_layout(title="<b>Project Overview</b>", height=250, margin=dict(t=40, b=30, l=15, r=15))
        set_chart_glass_theme(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with c2:
        weekly_df = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Reviews": [4, 7, 12, 16, 14, 6, 9]
        })
        fig_bar = px.bar(weekly_df, x="Day", y="Reviews", color="Day", color_discrete_sequence=["#38BDF8", "#818CF8", "#A78BFA", "#F472B6", "#FB7185", "#FDBA74", "#F59E0B"])
        fig_bar.update_layout(title="<b>Weekly Activity</b>", height=250, showlegend=False, margin=dict(t=40, b=30, l=25, r=15))
        set_chart_glass_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with right_col:
    render_stat_card("Total Code Reviews", str(total_reviews), "12% from last month", "up", "chart", "scf-stat-purple")
    render_stat_card("Code Quality Score", f"{avg_score}%", "8% improvement", "up", "diamond", "scf-stat-cyan")
    render_stat_card("Issues Detected", str(total_issues), "15% resolved", "down", "bug", "scf-stat-coral")
    render_stat_card("Projects Analyzed", str(projects_count), "3 active repositories", "up", "folder", "scf-stat-amber")

st.markdown("---")
render_quick_action_cards()
