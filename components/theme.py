"""
SmartCodeFlow — Design System & UI Components
Ultra-Premium 3D Glassmorphism Theme (matching Reference Dashboard)
Primary Accent: Burgundy Rose (#8B1E3F) | Wine Maroon (#6E1633)
Supporting: Soft Lavender (#C8B6FF), Blush Pink (#FFB5A7), Peach (#FCD5CE)
"""

import os
import re
import streamlit as st

# Color Constants
BURGUNDY_ROSE = "#8B1E3F"
WINE_MAROON = "#6E1633"
DEEP_WINE = "#380B1A"
SOFT_LAVENDER = "#C8B6FF"
BLUSH_PINK = "#FFB5A7"
SOFT_PEACH = "#FCD5CE"
MUTED_PURPLE = "#9D81BA"
CYAN_ACCENT = "#38BDF8"
BG_MAIN = "#F5F5F8"

def render_html(html_str: str):
    """Safely render minified HTML in Streamlit without newline markdown bugs."""
    single_line = re.sub(r'\s+', ' ', html_str).strip()
    if hasattr(st, "html"):
        st.html(single_line)
    else:
        st.markdown(single_line, unsafe_allow_html=True)


def get_logo_svg(size: int = 40) -> str:
    """Return an ultra-modern 3D vector SVG logo for SmartCodeFlow.
    Combines AI Neural Intelligence, Code Brackets < / >, and Dynamic Workflow Flow.
    """
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; filter: drop-shadow(0 6px 14px rgba(139, 30, 63, 0.28));">'
        f'<defs>'
        f'<linearGradient id="scfMainGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="#8B1E3F" />'
        f'<stop offset="60%" stop-color="#6E1633" />'
        f'<stop offset="100%" stop-color="#380B1A" />'
        f'</linearGradient>'
        f'<linearGradient id="scfFlowGrad" x1="0%" y1="100%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#C8B6FF" />'
        f'<stop offset="50%" stop-color="#FFB5A7" />'
        f'<stop offset="100%" stop-color="#FFFFFF" />'
        f'</linearGradient>'
        f'<linearGradient id="scfGlassShine" x1="0%" y1="0%" x2="100%" y2="50%">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.6" />'
        f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05" />'
        f'</linearGradient>'
        f'</defs>'
        # Rounded 3D Squircle Container
        f'<rect x="6" y="6" width="88" height="88" rx="24" fill="url(#scfMainGrad)" stroke="rgba(255, 255, 255, 0.65)" stroke-width="2"/>'
        f'<rect x="8" y="8" width="84" height="42" rx="22" fill="url(#scfGlassShine)"/>'
        # Ambient Glow Orb
        f'<circle cx="50" cy="50" r="28" fill="#C8B6FF" fill-opacity="0.22"/>'
        # Left Code Bracket <
        f'<path d="M34 32 L20 50 L34 68" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        # Right Code Bracket >
        f'<path d="M66 32 L80 50 L66 68" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        # Dynamic AI Flow Slash / S-Curve
        f'<path d="M60 26 C55 36, 45 64, 40 74" stroke="url(#scfFlowGrad)" stroke-width="5" stroke-linecap="round"/>'
        # Central AI Core Node
        f'<circle cx="50" cy="50" r="7" fill="#FFFFFF" stroke="#8B1E3F" stroke-width="2.5"/>'
        f'<circle cx="50" cy="50" r="3" fill="#8B1E3F"/>'
        # Flow Synapse Nodes
        f'<circle cx="32" cy="50" r="3" fill="#FFB5A7"/>'
        f'<circle cx="68" cy="50" r="3" fill="#C8B6FF"/>'
        f'</svg>'
    )


def load_custom_css():
    """Load and inject the global Ultra-Premium Glassmorphism stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    
    font_link = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
    )
    
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            render_html(f"{font_link}<style>{css_content}</style>")
            return
        except Exception:
            pass
            
    # Fallback inline basic styles
    render_html(f"""
    {font_link}
    <style>
    .stApp {{
        background-color: #F5F5F8 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    </style>
    """)


def render_top_header(active_page: str = "Dashboard"):
    """Render the top glass header matching the reference design:
    - Newly designed SmartCodeFlow Logo
    - Brand name
    - Pill Search Bar
    - Notification icon with glowing alert dot
    - User Profile icon & name
    """
    logo_svg = get_logo_svg(38)
    
    header_html = (
        f'<div class="scf-top-header">'
        # Brand lockup
        f'<a href="/" target="_self" class="scf-brand-lockup">'
        f'{logo_svg}'
        f'<div class="scf-brand-text">'
        f'<div class="scf-brand-title">SmartCode<span>Flow</span></div>'
        f'<div class="scf-brand-subtitle">AI Code Intelligence Platform</div>'
        f'</div>'
        f'</a>'
        # Search Bar
        f'<div class="scf-search-container">'
        f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7A7585" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>'
        f'</svg>'
        f'<input type="text" class="scf-search-input" placeholder="Search reviews, files, projects..." readonly />'
        f'</div>'
        # Right Actions: Notifications & User Avatar
        f'<div class="scf-header-actions">'
        f'<div class="scf-icon-pill-btn" title="Notifications">'
        f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1E1B24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>'
        f'<path d="M13.73 21a2 2 0 0 1-3.46 0"></path>'
        f'</svg>'
        f'<span class="scf-notification-dot"></span>'
        f'</div>'
        f'<div class="scf-user-badge">'
        f'<div class="scf-user-avatar">M</div>'
        f'<div class="scf-user-info">'
        f'<div class="scf-user-name">Developer</div>'
        f'<div class="scf-user-role">Code Reviewer</div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    render_html(header_html)


def render_welcome_banner(
    title: str = "Welcome Back, Developer!",
    subtitle: str = "Here's an overview of your code quality and review progress.",
    filter_label: str = "This Month ▾"
):
    """Render the welcome message block with filter pill as shown in reference image."""
    banner_html = (
        f'<div class="scf-welcome-box">'
        f'<div>'
        f'<h1 class="scf-welcome-title">{title}</h1>'
        f'<p class="scf-welcome-sub">{subtitle}</p>'
        f'</div>'
        f'<div class="scf-pill-filter">'
        f'<span>{filter_label}</span>'
        f'</div>'
        f'</div>'
    )
    render_html(banner_html)


def render_stat_card(
    label: str,
    value: str,
    delta: str,
    delta_type: str = "up",
    icon_type: str = "chart",
    color_class: str = "scf-stat-purple"
):
    """Render a 3D-inspired glassmorphic metric card matching the right column of the reference image."""
    # Select vector icon based on type
    if icon_type == "chart":
        icon_svg = (
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>'
            '</svg>'
        )
    elif icon_type == "users":
        icon_svg = (
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>'
            '</svg>'
        )
    elif icon_type == "score" or icon_type == "diamond":
        icon_svg = (
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>'
            '</svg>'
        )
    elif icon_type == "bug" or icon_type == "shield":
        icon_svg = (
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="6" y="8" width="12" height="12" rx="4"></rect><path d="M12 2v6"></path><path d="M4 14h3"></path><path d="M17 14h3"></path><path d="M5 19l2-2"></path><path d="M19 19l-2-2"></path>'
            '</svg>'
        )
    else: # folder / repo
        icon_svg = (
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>'
            '</svg>'
        )

    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "•")
    delta_class = "scf-delta-up" if delta_type == "up" else ("scf-delta-down" if delta_type == "down" else "scf-delta-neutral")

    card_html = (
        f'<div class="scf-stat-card">'
        f'<div class="scf-stat-icon-box {color_class}">{icon_svg}</div>'
        f'<div class="scf-stat-content">'
        f'<div class="scf-stat-label">{label}</div>'
        f'<div class="scf-stat-value">{value}</div>'
        f'<div class="scf-stat-delta {delta_class}">{arrow} {delta}</div>'
        f'</div>'
        f'</div>'
    )
    render_html(card_html)


def render_quick_action_cards():
    """Render the 4 bottom glassmorphic quick action cards from the reference image."""
    cards_html = (
        f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 14px; margin-bottom: 24px;">'
        # Card 1: New Code Review
        f'<a href="/2Submit_Code" target="_self" class="scf-quick-action-card">'
        f'<div class="scf-action-icon-box scf-stat-purple">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline>'
        f'</svg>'
        f'</div>'
        f'<div class="scf-action-title">New Code Review</div>'
        f'<div class="scf-action-subtitle">Upload source code & analyze</div>'
        f'</a>'
        # Card 2: Project Analysis
        f'<a href="/2Project_Analysis" target="_self" class="scf-quick-action-card">'
        f'<div class="scf-action-icon-box scf-stat-cyan">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>'
        f'<polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>'
        f'</svg>'
        f'</div>'
        f'<div class="scf-action-title">Project Analysis</div>'
        f'<div class="scf-action-subtitle">Upload ZIP & audit codebase</div>'
        f'</a>'
        # Card 3: GitHub Integration
        f'<a href="/9GitHub_Publisher" target="_self" class="scf-quick-action-card">'
        f'<div class="scf-action-icon-box scf-stat-coral">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<line x1="6" y1="3" x2="6" y2="15"></line><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><path d="M18 9a9 9 0 0 1-9 9"></path>'
        f'</svg>'
        f'</div>'
        f'<div class="scf-action-title">GitHub Integration</div>'
        f'<div class="scf-action-subtitle">Connect repo & push commits</div>'
        f'</a>'
        # Card 4: Review History
        f'<a href="/7Review_History" target="_self" class="scf-quick-action-card">'
        f'<div class="scf-action-icon-box scf-stat-amber">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>'
        f'</svg>'
        f'</div>'
        f'<div class="scf-action-title">Review History</div>'
        f'<div class="scf-action-subtitle">View past reviews & scores</div>'
        f'</a>'
        f'</div>'
    )
    render_html(cards_html)


def render_vs_code_editor_header(filename: str = "module.py", language: str = "python", lines_count: int = 0):
    """Render the VS Code-style macOS dark editor header tab inside light glassmorphism."""
    lines_str = f" • {lines_count} lines" if lines_count > 0 else ""
    header_html = (
        f'<div class="scf-editor-mac-header" style="border-top-left-radius: 18px; border-top-right-radius: 18px;">'
        f'<div style="display: flex; align-items: center; gap: 12px;">'
        f'<div class="scf-editor-dots">'
        f'<span class="scf-mac-dot red"></span>'
        f'<span class="scf-mac-dot yellow"></span>'
        f'<span class="scf-mac-dot green"></span>'
        f'</div>'
        f'<div class="scf-editor-tab">'
        f'<span style="color: #8B1E3F;">●</span> {filename}'
        f'</div>'
        f'</div>'
        f'<div style="color: #A1A1AA; font-size: 0.75rem; font-family: monospace;">'
        f'<span>UTF-8</span> • <span style="color: #FFB5A7; font-weight: 600;">{language.upper()}</span>{lines_str}'
        f'</div>'
        f'</div>'
    )
    render_html(header_html)


def render_finding_glass_card(finding: dict, index: int = 0):
    """Render a finding in an attractive glass card with severity indicator and suggested fixes."""
    severity = finding.get("severity", "Medium")
    sev_lower = severity.lower()
    
    badge_class = f"scf-badge-{sev_lower}"
    border_class = f"scf-finding-{sev_lower}"
    
    title = finding.get("title", "Review Finding")
    category = finding.get("category", "General")
    line = finding.get("line", "N/A")
    problem = finding.get("description", finding.get("problem", ""))
    fix = finding.get("suggested_fix", finding.get("fixed", finding.get("suggestion", "")))
    
    card_html = (
        f'<div class="scf-finding-card {border_class}">'
        f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">'
        f'<div style="font-weight: 700; color: #1E1B24; font-size: 0.95rem;">{title}</div>'
        f'<span class="scf-severity-badge {badge_class}">{severity}</span>'
        f'</div>'
        f'<div style="font-size: 0.78rem; color: #7A7585; margin-bottom: 8px;">'
        f'<span>Category: <strong>{category}</strong></span> • <span>Line: <strong>{line}</strong></span>'
        f'</div>'
        f'<div style="font-size: 0.84rem; color: #423E4B; line-height: 1.45; margin-bottom: 10px;">{problem}</div>'
        f'</div>'
    )
    render_html(card_html)


def set_chart_glass_theme(fig):
    """Apply transparent glassmorphic background, glowing palette, and clean typography to Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#423E4B", size=11),
        margin=dict(t=45, b=25, l=35, r=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10)
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(217, 160, 176, 0.18)",
        gridwidth=1,
        zeroline=False,
        linecolor="rgba(217, 160, 176, 0.35)"
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(217, 160, 176, 0.18)",
        gridwidth=1,
        zeroline=False,
        linecolor="rgba(217, 160, 176, 0.35)"
    )
    return fig
