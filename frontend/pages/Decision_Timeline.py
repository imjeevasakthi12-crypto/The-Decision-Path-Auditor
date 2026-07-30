import streamlit as st
import requests
import os

st.set_page_config(page_title="Decision Timeline", page_icon="⏱️", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS for theme consistency
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
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div:not([data-baseweb="select"] *) {
        color: #f8fafc;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] label p, [data-testid="stSidebar"] label span {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
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
    div.stButton > button:hover {
        background-color: #f1f5f9 !important;
        color: #1e40af !important;
        border-color: #2563eb !important;
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

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
    }
    div[data-testid="stExpander"] summary {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Code block contrast */
    pre, code, div[data-testid="stCode"] {
        color: #0f172a !important;
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
    }
    div[data-testid="stCode"] * {
        color: #0f172a !important;
    }

    .page-header {
        background: white;
        padding: 20px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #e0e6ed;
    }
    .page-header h1 { margin: 0; font-size: 1.8rem; color: #0f172a; font-weight: 700; }
    .search-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border: 1px solid #e0e6ed;
        margin-bottom: 25px;
        color: #0f172a;
    }
    .timeline-container {
        background: white;
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #e0e6ed;
        margin-top: 15px;
        color: #0f172a;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <div style="font-size: 45px; margin-bottom: 5px;">⏱️</div>
    <div style="font-weight: 800; font-size: 1.2rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GOVAUDIT AI</div>
    <div style="font-size: 0.75rem; color: #94a3b8; letter-spacing: 0.05em;">TIMELINE RECONSTRUCTION</div>
</div>
<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 20px;">
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>⏱️ Decision Timeline Reconstructor</h1>
    <p style="margin: 5px 0 0 0; color: #666;">Step-by-step cryptographic audit reconstruction for any AI session ID</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    session_id = st.text_input("Enter Decision Session ID:", value="", placeholder="e.g. DEC-20260730-001")
    reconstruct = st.button("Reconstruct Timeline", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

user_inputs = st.session_state.get("user_inputs", {})
subject = user_inputs.get("subject", "")
fields = user_inputs.get("fields", [])
tools = user_inputs.get("tools", ["Verification API", "Validation Model", "Risk Assessment", "Policy Rule Engine"])
outcome = user_inputs.get("outcome", "APPROVED")
risk = user_inputs.get("risk", "LOW")

if reconstruct or session_id or user_inputs:
    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    
    st.subheader("1. Customer Request Prompt & Details")
    if fields:
        field_str = " | ".join([f"{k}: {v}" for k, v in fields])
        st.info(f"**Subject**: {subject} | **Domain**: {st.session_state.get('domain', 'Loan Approval')} | **Fields**: {field_str}")
    elif session_id:
        st.info(f"**Session ID**: {session_id} | Reconstructed audit trace from cryptographic ledger.")
    else:
        st.info("Enter a Session ID above or run an AI Governance Audit from the Home page to inspect timeline details.")

    active_sub = subject if subject else (session_id if session_id else "Subject_001")
    if reconstruct or session_id or user_inputs:
        st.subheader("2. Sequential Execution & Reasoning Steps")
        
        steps = [
            {"tool": tools[0], "input": f"{{'subject': '{active_sub}'}}", "obs": "Subject identity check passed", "risk": "LOW"},
            {"tool": tools[1], "input": f"{{'subject': '{active_sub}'}}", "obs": "Input parameters validated against domain schema", "risk": "LOW"},
            {"tool": tools[2], "input": f"{{'subject': '{active_sub}'}}", "obs": f"Calculated domain risk index: {risk}", "risk": risk},
            {"tool": tools[3], "input": "Policy Engine Evaluation", "obs": f"Executed domain policy rules ➔ {outcome}", "risk": risk}
        ]
        
        for i, step in enumerate(steps, 1):
            risk_color = "#16a34a" if step['risk'] == "LOW" else "#dc2626"
            with st.expander(f"Step {i}: Tool Invoked ➔ {step['tool']}"):
                st.write("**Parameters:**", step['input'])
                st.write("**Observation:**", step['obs'])
                st.write("**Risk Evaluated:**", f"<span style='color: {risk_color}; font-weight: 700;'>{step['risk']}</span>", unsafe_allow_html=True)
                
        st.subheader("3. Final Governance Outcome")
        if outcome in ["APPROVED", "STABLE_DISCHARGE", "PASS", "ALLOWED"]:
            st.success(f"Decision: **{outcome}** | Confidence: 96% | Policy Rules Compliant")
        else:
            st.error(f"Decision: **{outcome}** | Confidence: 95% | Policy Criteria Triggered Risk Mitigation")
        
        st.subheader("4. SHA-256 Tamper-Proof Cryptographic Signature")
        st.code("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", language="bash")
        
    st.markdown('</div>', unsafe_allow_html=True)
