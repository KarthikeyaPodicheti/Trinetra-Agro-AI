"""Trinetra Agro AI — SaaS Dashboard with JWT auth verification."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from frontend.api_client import login, register, logout, verify_session

st.set_page_config(page_title="Trinetra Agro AI", page_icon="🔱", layout="wide")

API = "http://localhost:8000"

# ---- CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.hero { background: linear-gradient(135deg, #E8F5E9, #fff, #F1F8E9); border-radius: 18px; padding: 2rem; text-align: center; border: 1px solid #C8E6C9; margin-bottom: 1.5rem; }
.hero h1 { color: #2E7D32; font-size: 2.2rem; margin: 0; }
.hero p { color: #66BB6A; font-size: 1rem; margin-top: .3rem; }
.stButton > button { background: linear-gradient(135deg, #43A047, #66BB6A) !important; color: #fff !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #FAFFFE, #E8F5E9) !important; }
</style>
""", unsafe_allow_html=True)

# ---- Session init ----
if "page" not in st.session_state:
    qp = st.query_params
    url_page = qp.get("page", None)
    st.session_state.page = url_page if url_page else "dashboard"

# ---- Auth check ----
st.session_state.authenticated = verify_session()

# ---- Auth Gate (center-screen) ----
if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .auth-card {
        max-width: 420px; margin: 5rem auto 0 auto;
        background: #fff; border-radius: 18px;
        padding: 2.5rem 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid #E8F5E9;
        text-align: center;
    }
    .auth-card h1 { color: #2E7D32; font-size: 1.8rem; margin-bottom: 0.3rem; }
    .auth-card p { color: #81C784; font-size: 0.9rem; margin-bottom: 1.5rem; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
    <div class="auth-card">
        <h1>🔱 Trinetra Agro AI</h1>
        <p>Vision Beyond the Fields</p>
    </div>
    """, unsafe_allow_html=True)

    tab = st.radio("Auth Mode", ["Login", "Register"], horizontal=True, label_visibility="collapsed")
    if tab == "Login":
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="demo@farm.com")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if login(email, password):
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    else:
        with st.form("register_form"):
            email = st.text_input("Email")
            name = st.text_input("Full Name")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                if register(email, password, name):
                    st.rerun()
                else:
                    st.error("Registration failed — email may already exist")
    st.stop()

# Authenticated — show user info and navigation in the sidebar
with st.sidebar:
    user = st.session_state.get("user", {})
    st.markdown(f"### 👨‍🌾 Welcome, {user.get('full_name', user.get('email', 'Farmer'))}")

    st.markdown("#### Navigation")
    pages = ["📊 Dashboard", "🌱 AI Advisor", "🔬 Disease Scanner",
             "📈 Market Intelligence", "💬 AI Chatbot", "📝 Feedback"]
    page_keys = ["dashboard", "ai_advisor", "disease_scanner",
                 "market_intelligence", "chatbot", "feedback"]

    current_key = st.session_state.get("page", "dashboard")
    default_idx = page_keys.index(current_key) if current_key in page_keys else 0

    choice = st.radio("Navigate", pages, index=default_idx, label_visibility="collapsed")

    st.session_state.page = page_keys[pages.index(choice)]
    st.query_params["page"] = st.session_state.page

    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        logout()
        st.rerun()

# ---- Main Content ----

page = st.session_state.page
if page == "dashboard":
    from frontend.views import dashboard; dashboard.show()
elif page == "ai_advisor":
    from frontend.views import advisor; advisor.show()
elif page == "disease_scanner":
    from frontend.views import disease; disease.show()
elif page == "market_intelligence":
    from frontend.views import market; market.show()
elif page == "chatbot":
    from frontend.views import chatbot; chatbot.show()
elif page == "feedback":
    from frontend.views import feedback; feedback.show()
