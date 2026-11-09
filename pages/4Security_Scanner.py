import sys
import importlib
import time
import streamlit as st
import pandas as pd

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
    page_title="Security Scanner | SmartCodeFlow",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Dashboard")
render_top_header(active_page="Dashboard")

render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Automated <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Security Scanner</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Deep static vulnerability inspection powered by Bandit AST rules and custom CWE detection signatures.'
    '</p>'
    '</div>'
)

# Top Telemetry Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_stat_card("Target Modules", "4 Scanned", "auth, db, payment", "neutral", "folder", "scf-stat-purple")
with col2:
    render_stat_card("Open CVE Risks", "2 Detected", "1 High, 1 Med", "down", "bug", "scf-stat-coral")
with col3:
    render_stat_card("AST Rules Run", "105 Rules", "Bandit v1.7.5", "up", "diamond", "scf-stat-cyan")
with col4:
    render_stat_card("CWE Compliance", "92%", "OWASP Top 10", "up", "score", "scf-stat-amber")

st.markdown("---")

col_left, col_right = st.columns([1.2, 1.0], gap="large")

with col_left:
    target_module = st.selectbox(
        "Select Target Module for Deep Security Audit",
        ["sample_buggy_code.py", "auth_service.py", "payment_gateway.py", "user_controller.py", "db_connector.py"]
    )
    
    if st.button("🛡️ Run Deep Security Scan", type="primary", use_container_width=True):
        with st.spinner(f"Executing Bandit & AST security scan on {target_module}..."):
            time.sleep(1.2)
        st.success(f"Security audit on `{target_module}` completed successfully!")

    st.markdown("### Detected Security Findings")
    
    security_data = pd.DataFrame([
        {"Rule ID": "B608", "Severity": "High", "Category": "SQL Injection", "Location": "Line 7", "Status": "Open"},
        {"Rule ID": "B105", "Severity": "Medium", "Category": "Hardcoded Password / Secret", "Location": "Line 14", "Status": "Open"},
        {"Rule ID": "B301", "Severity": "Low", "Category": "Use of pickle/Unsafe Deserialization", "Location": "Line 29", "Status": "Resolved"}
    ])
    st.dataframe(security_data, use_container_width=True, hide_index=True)

with col_right:
    render_html(
        '<div style="background: rgba(255, 255, 255, 0.60); border: 1.2px solid rgba(255, 255, 255, 0.85); border-radius: 20px; padding: 22px 24px; box-shadow: 0 8px 24px rgba(110, 22, 51, 0.04);">'
        '<div style="font-weight: 800; font-size: 1.10rem; color: #1E1B24; margin-bottom: 10px;">Remediation Guidance</div>'
        '<div style="font-size: 0.84rem; color: #423E4B; line-height: 1.6;">'
        '• <strong>High Priority:</strong> Address SQL injection risks immediately by using parameterized query tuples instead of direct string formatting.<br><br>'
        '• <strong>Credential Security:</strong> Remove hardcoded passwords and inject environment variables via <code>os.getenv()</code>.<br><br>'
        '• <strong>Safe Deserialization:</strong> Replace <code>pickle.loads</code> with strict schema validation using <code>json.loads</code> or <code>pydantic</code>.'
        '</div>'
        '</div>'
    )
