import streamlit as st
import os
from components.theme import load_custom_css, get_logo_svg, render_html

def show_sidebar(active_page: str = "Dashboard"):
    """Render the translucent glass sidebar inspired by the reference design."""
    load_custom_css()
    
    with st.sidebar:
        # SmartCodeFlow Logo & Title
        logo_svg = get_logo_svg(36)
        brand_html = (
            f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">'
            f'{logo_svg}'
            f'<div>'
            f'<div style="font-size: 1.22rem; font-weight: 800; color: #1E1B24; letter-spacing: -0.02em; line-height: 1.15;">'
            f'SmartCode<span style="color: #8B1E3F;">Flow</span>'
            f'</div>'
            f'<div style="font-size: 0.68rem; font-weight: 600; text-transform: uppercase; color: #7A7585; letter-spacing: 0.08em;">AI Code Review</div>'
            f'</div>'
            f'</div>'
        )
        render_html(brand_html)
        
        st.markdown("---")
        
        # Navigation Items
        render_html('<div style="font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #8B1E3F; margin-bottom: 8px; margin-left: 8px;">Main Menu</div>')
        
        # 1. Dashboard
        st.page_link("app.py", label="Dashboard", icon="🏠")
        
        # 2. Code Review
        st.page_link("pages/2Submit_Code.py", label="Code Review", icon="⚡")
        
        # 3. Project Analysis
        if os.path.exists("pages/2Project_Analysis.py"):
            st.page_link("pages/2Project_Analysis.py", label="Project Analysis", icon="📦")
        elif os.path.exists("pages/6Analytics.py"):
            st.page_link("pages/6Analytics.py", label="Project Analysis", icon="📦")
            
        # 4. Review History
        st.page_link("pages/7Review_History.py", label="Review History", icon="📜")
        
        # 5. GitHub Integration
        st.page_link("pages/9GitHub_Publisher.py", label="GitHub Integration", icon="🚀")
        
        # 6. Team Collaboration / AI Chat
        st.page_link("pages/5AI_Reviewer_Chat.py", label="Team Collaboration", icon="👥")
        
        # 7. Settings
        st.page_link("pages/10Settings.py", label="Settings", icon="⚙️")
        
        st.markdown("---")
        
        # Secondary Tools
        render_html('<div style="font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #7A7585; margin-bottom: 8px; margin-left: 8px;">Deep Tools</div>')
        st.page_link("pages/4Security_Scanner.py", label="Security Scanner", icon="🛡️")
        st.page_link("pages/6Analytics.py", label="Quality Analytics", icon="📊")
        st.page_link("pages/8_Reports.py", label="Audit Reports", icon="📋")
        
        st.markdown("---")
        
        # Engine Telemetry Glass Card
        telemetry_html = (
            f'<div style="background: rgba(255, 255, 255, 0.60); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.85); border-radius: 16px; padding: 14px 16px; box-shadow: 0 4px 16px rgba(139, 30, 63, 0.04);">'
            f'<div style="font-size: 0.74rem; font-weight: 700; text-transform: uppercase; color: #8B1E3F; letter-spacing: 0.06em; margin-bottom: 8px;">Engine Telemetry</div>'
            f'<div style="font-size: 0.78rem; color: #423E4B; margin-bottom: 5px; display: flex; align-items: center; gap: 6px;">'
            f'<span style="width: 7px; height: 7px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 6px #22C55E;"></span>'
            f'<span>AI Engine: <strong>Gemini 1.5 / 2.5</strong></span>'
            f'</div>'
            f'<div style="font-size: 0.78rem; color: #423E4B; margin-bottom: 5px; display: flex; align-items: center; gap: 6px;">'
            f'<span style="width: 7px; height: 7px; border-radius: 50%; background: #38BDF8; box-shadow: 0 0 6px #38BDF8;"></span>'
            f'<span>Linters: <strong>Pylint & Bandit</strong></span>'
            f'</div>'
            f'<div style="font-size: 0.78rem; color: #423E4B; display: flex; align-items: center; gap: 6px;">'
            f'<span style="width: 7px; height: 7px; border-radius: 50%; background: #8B1E3F; box-shadow: 0 0 6px #8B1E3F;"></span>'
            f'<span>Database: <strong>SQLite Synchronized</strong></span>'
            f'</div>'
            f'</div>'
        )
        render_html(telemetry_html)
        
        st.caption("SmartCodeFlow v2.5 • AI Code Review Platform")
