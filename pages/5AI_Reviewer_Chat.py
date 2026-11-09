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
    page_title="Team Collaboration & AI Chat | SmartCodeFlow",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()
show_sidebar(active_page="Team Collaboration")
render_top_header(active_page="Team Collaboration")

# Page Header
render_html(
    '<div style="margin-bottom: 20px;">'
    '<h1 style="font-size: 1.85rem; font-weight: 800; color: #1E1B24; margin: 0; letter-spacing: -0.025em;">'
    'Team Collaboration & <span style="background: linear-gradient(135deg, #8B1E3F, #D9A0B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Reviewer Chat</span>'
    '</h1>'
    '<p style="color: #7A7585; font-size: 0.92rem; margin-top: 4px;">'
    'Collaborate with team reviewers and interact with the AI Code Reviewer to clarify architectural patterns and security fixes.'
    '</p>'
    '</div>'
)

# Top Telemetry Cards
col_c1, col_c2, col_c3, col_c4 = st.columns(4)
with col_c1:
    render_stat_card("AI Reviewer", "Online", "Gemini 1.5 / 2.5", "up", "score", "scf-stat-purple")
with col_c2:
    render_stat_card("Active Reviewers", "3 Online", "Monisha, Dev, SecOps", "up", "users", "scf-stat-cyan")
with col_c3:
    render_stat_card("Collaborations", "18 Threads", "Code annotations", "neutral", "chart", "scf-stat-amber")
with col_c4:
    render_stat_card("Response Time", "420 ms", "AST + LLM Hybrid", "up", "diamond", "scf-stat-coral")

st.markdown("---")

submitted_code = st.session_state.get("submitted_code", "")
if not submitted_code:
    try:
        with open("sample_buggy_code.py", "r") as f:
            submitted_code = f.read()
    except Exception:
        submitted_code = "def sample(): pass"

language = st.session_state.get("selected_language", "Python")

# View Context Code Expander
with st.expander("📄 Active Code Context Being Discussed", expanded=False):
    st.code(submitted_code, language=language.lower() if language != "C++" else "cpp", line_numbers=True)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {
            "role": "assistant",
            "content": "👋 Hello Developer! I am your SmartCodeFlow AI Assistant. Ask me anything about bug detection, security vulnerabilities, or refactoring in your submitted codebase."
        }
    ]

# Suggested Prompt Pills
render_html('<div style="font-size: 0.85rem; font-weight: 700; color: #8B1E3F; margin-bottom: 8px;">Suggested Questions</div>')
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Explain potential bugs", use_container_width=True):
        st.session_state["suggested_question"] = "Explain the potential bugs in the code and how to fix them."
with col2:
    if st.button("🛡️ Audit security vulnerabilities", use_container_width=True):
        st.session_state["suggested_question"] = "Identify any hardcoded credentials or SQL injection vulnerabilities in my code."
with col3:
    if st.button("✨ Refactor to Clean Code", use_container_width=True):
        st.session_state["suggested_question"] = "Provide a clean, refactored version of this code conforming to PEP 8 standards."

st.markdown("---")

# Render Conversation
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

suggested_question = st.session_state.pop("suggested_question", None)
user_question = st.chat_input("Ask a question about your code or leave a review note for the team...")

if suggested_question:
    user_question = suggested_question

if user_question:
    st.session_state["chat_history"].append({"role": "user", "content": user_question})
    
    with st.chat_message("user"):
        st.markdown(user_question)
        
    with st.chat_message("assistant"):
        # Formulate intelligent response using Gemini or local rules
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"You are SmartCodeFlow, an expert AI code reviewer. Code:\n```\n{submitted_code}\n```\nQuestion: {user_question}"
                resp = model.generate_content(prompt)
                answer = resp.text
            except Exception as e:
                answer = f"I analyzed your code context. In `{language}`, you should validate inputs before arithmetic operations, extract secrets to environment variables, and use logging rather than print statements. (API Error: {str(e)})"
        else:
            # Smart contextual response
            if "bug" in user_question.lower() or "division" in user_question.lower():
                answer = "In your submitted code, `divide_numbers(10, 0)` triggers a `ZeroDivisionError` at runtime. Similarly, `calculate_average([])` divides by `len(numbers)`, which is `0` when empty. \n\n**Recommendation:** Add validation `if b != 0:` and `if len(numbers) > 0:` before performing division."
            elif "security" in user_question.lower() or "password" in user_question.lower():
                answer = "A critical security issue is present: `get_user_password()` contains hardcoded credentials (`password = 'admin123'`). Hardcoded passwords risk credential exposure if committed to version control. \n\n**Recommendation:** Use `os.getenv('ADMIN_PASSWORD')` instead."
            else:
                answer = "I've reviewed the code structure. Key improvements include replacing `print()` calls with structured Python `logging`, adding type hints (`def divide_numbers(a: float, b: float) -> float:`), and guarding against zero-length collections."
                
        st.markdown(answer)
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})

st.markdown("---")
if st.button("🗑️ Clear Conversation"):
    st.session_state["chat_history"] = []
    st.rerun()
