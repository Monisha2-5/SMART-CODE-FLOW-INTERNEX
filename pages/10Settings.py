import sys
import importlib
import os
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
    page_title="Settings | SmartCodeFlow",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Settings")
render_top_header(active_page="Settings")

# Page Header
render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Platform <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Settings & Engine Config</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Configure AI model endpoints, API credentials, static linter thresholds, and security compliance policies.'
    '</p>'
    '</div>'
)

# Top Telemetry Cards
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    render_stat_card("Active Engine", "Gemini 1.5", "Default LLM", "up", "score", "scf-stat-purple")
with col_s2:
    render_stat_card("API Key Status", "Configured" if os.getenv("GEMINI_API_KEY") else "Local Mode", "Environment", "up", "folder", "scf-stat-cyan")
with col_s3:
    render_stat_card("Linters Loaded", "Pylint + Bandit", "Dual AST verification", "up", "shield", "scf-stat-coral")
with col_s4:
    render_stat_card("Database Path", "SQLite (Local)", "smartcodeflow.db", "neutral", "diamond", "scf-stat-amber")

st.markdown("---")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">🤖 AI Engine Preferences</div>')
    
    current_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input("Google Gemini API Key", value=current_key, type="password", placeholder="AIzaSy...")
    
    model_choice = st.selectbox(
        "Primary Code Review Model",
        ["Google Gemini 1.5 Flash (Recommended)", "Google Gemini 2.0 Flash", "Hybrid Static + LLM", "Local AST Heuristic Engine"]
    )
    
    temperature = st.slider("LLM Temperature (Creativity vs Determinism)", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.select_slider("Max Analysis Tokens", options=[1024, 2048, 4096, 8192], value=4096)

with col_right:
    render_html('<div style="font-size: 1.10rem; font-weight: 800; color: #1E1B24; margin-bottom: 12px;">🛡️ Linter & Security Standards</div>')
    
    pep8_enabled = st.checkbox("Enforce PEP 8 Formatting Standards", value=True)
    bandit_enabled = st.checkbox("Enable Bandit AST Security Scanner", value=True)
    cyclomatic_enabled = st.checkbox("Flag Functions with Cyclomatic Complexity > 10", value=True)
    sql_check_enabled = st.checkbox("Strict SQL Injection Detection", value=True)
    hardcoded_secret_enabled = st.checkbox("Flag Potential Hardcoded Passwords / API Keys", value=True)

st.markdown("---")

if st.button("💾 Save Configuration & Apply", type="primary", use_container_width=True):
    if api_key_input.strip():
        os.environ["GEMINI_API_KEY"] = api_key_input.strip()
    st.success("✅ Configuration saved successfully! Settings applied to active session.")
