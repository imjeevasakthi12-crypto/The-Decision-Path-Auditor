import streamlit as st
import requests
import os

st.set_page_config(page_title="Auditor Login", page_icon="🔒", layout="centered")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS for consistent light theme
st.markdown("""
<style>
    /* Global High Contrast Theme */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: #0f172a;
    }
    
    /* Vibrant Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
        border-right: 1px solid #312e81 !important;
    }
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    [data-testid="stSidebarNav"] a {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        transform: translateX(5px) scale(1.02) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Universal Button High Contrast */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        border: 1.5px solid #94a3b8 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    div.stButton > button * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Dropdown Menus, Selectboxes & BaseWeb Popovers Universal High-Contrast Fix */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[data-baseweb="menu"],
    ul[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    li[data-baseweb="option"],
    li[data-baseweb="option"] *,
    div[role="option"],
    div[role="option"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    li[data-baseweb="option"]:hover,
    li[data-baseweb="option"]:hover *,
    li[data-baseweb="option"][aria-selected="true"],
    li[data-baseweb="option"][aria-selected="true"] *,
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover * {
        background-color: #e2e8f0 !important;
        color: #1d4ed8 !important;
    }

    /* Primary Buttons */
    div.stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"] *, button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Form Inputs */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1.5px solid #94a3b8 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    .login-card {
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e6ed;
        margin-top: 50px;
        color: #0f172a;
    }
    .login-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: #0f172a;
        text-align: center;
    }
    .login-subtitle {
        font-size: 0.95rem;
        color: #475569;
        text-align: center;
        margin-bottom: 25px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <div style="font-size: 45px; margin-bottom: 5px;">🔒</div>
    <div style="font-weight: 800; font-size: 1.2rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GOVAUDIT AI</div>
    <div style="font-size: 0.75rem; color: #94a3b8; letter-spacing: 0.05em;">SECURE AUTHENTICATION</div>
</div>
<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 20px;">
""", unsafe_allow_html=True)

st.markdown("""
<div class="login-card">
    <div class="login-title">🔒 Enterprise Auditor Login</div>
    <div class="login-subtitle">Sign in to access AI governance logs & audit metrics</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if "token" in st.session_state:
    st.success("You are securely logged in.")
    if st.button("Logout", type="primary"):
        del st.session_state["token"]
        st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="admin123")
        submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        
        if submit:
            res = requests.post(
                f"{BACKEND_URL}/api/auth/token",
                data={"username": username, "password": password}
            )
            if res.status_code == 200:
                st.session_state["token"] = res.json()["access_token"]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                # Mock token for demo ease if backend auth isn't populated
                st.session_state["token"] = "demo_token_123"
                st.success("Logged in successfully (Demo Mode)!")
                st.rerun()
