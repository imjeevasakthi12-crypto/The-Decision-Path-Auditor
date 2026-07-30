import streamlit as st
import requests
import os
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS for theme consistency & high contrast
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
    div.stButton > button:hover * {
        color: #1e40af !important;
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

    .page-header {
        background: white;
        padding: 20px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #e0e6ed;
    }
    .page-header h1 { margin: 0; font-size: 1.8rem; color: #0f172a; font-weight: 700; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        text-align: center;
    }
    .metric-title { font-size: 0.9rem; color: #475569; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
    .metric-value { font-size: 2rem; font-weight: 800; color: #1d4ed8; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <div style="font-size: 45px; margin-bottom: 5px;">📊</div>
    <div style="font-weight: 800; font-size: 1.2rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GOVAUDIT AI</div>
    <div style="font-size: 0.75rem; color: #94a3b8; letter-spacing: 0.05em;">ANALYTICS & METRICS</div>
</div>
<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 20px;">
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📊 Enterprise Governance Dashboard</h1>
    <p style="margin: 5px 0 0 0; color: #666;">Global overview of AI decision metrics, compliance ratios, and execution volume</p>
</div>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.info("💡 You are currently viewing in guest mode. Login to unlock advanced governance controls.")

# Initialize dynamic audit logs list if empty
if "audit_history_logs" not in st.session_state:
    st.session_state.audit_history_logs = []

# Base historical counts
base_approved = 95
base_rejected = 35
base_flagged = 12

# Synchronize live audit logs from session state
live_logs = st.session_state.audit_history_logs

# If user_inputs is present in session state but not yet in history_logs, ensure it's counted
user_inputs = st.session_state.get("user_inputs", {})
if user_inputs and not any(log.get("subject") == user_inputs.get("subject") for log in live_logs):
    live_logs.append({
        "subject": user_inputs.get("subject", "Unspecified Subject"),
        "domain": st.session_state.get("domain", "Education"),
        "outcome": user_inputs.get("outcome", "REJECTED"),
        "risk": user_inputs.get("risk", "HIGH"),
        "fields": user_inputs.get("fields", []),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

# Count outcomes dynamically
live_approved = sum(1 for log in live_logs if log.get("outcome") in ["APPROVED", "STABLE_DISCHARGE", "PASS", "ALLOWED"])
live_rejected = sum(1 for log in live_logs if log.get("outcome") in ["REJECTED", "BLOCKED", "CRITICAL_CARE", "FAIL"])
live_flagged = sum(1 for log in live_logs if log.get("outcome") in ["REFERRAL_REQUIRED", "MANUAL_REVIEW_REQUIRED", "CONDITIONAL_APPROVAL", "MFA_CHALLENGE", "UNDER_REVIEW"])

total_approved = base_approved + live_approved
total_rejected = base_rejected + live_rejected
total_flagged = base_flagged + live_flagged
total_audited = total_approved + total_rejected + total_flagged

approval_rate = (total_approved / total_audited * 100) if total_audited > 0 else 0.0
rejection_rate = (total_rejected / total_audited * 100) if total_audited > 0 else 0.0

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Audited Sessions</div>
        <div class="metric-value">{total_audited}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Approval Rate</div>
        <div class="metric-value" style="color: #16a34a;">{approval_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Rejection Rate</div>
        <div class="metric-value" style="color: #dc2626;">{rejection_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Avg Execution Time</div>
        <div class="metric-value" style="color: #2563eb;">1.2s</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Decision Distribution")
    df_pie = pd.DataFrame({
        'Outcome': ['Approved', 'Rejected', 'Flagged for Manual Review'],
        'Count': [total_approved, total_rejected, total_flagged]
    })
    fig_pie = px.pie(df_pie, values='Count', names='Outcome', color='Outcome',
                     color_discrete_map={'Approved':'#16a34a', 'Rejected':'#dc2626', 'Flagged for Manual Review':'#f59e0b'},
                     hole=0.4)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(color='#0f172a')))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.subheader("Audit Volume Over Time")
    today_count = 23 + len(live_logs)
    df_line = pd.DataFrame({
        'Date': pd.date_range(start='2026-07-24', periods=7),
        'Audits': [14, 18, 22, 19, 25, 21, today_count]
    })
    fig_line = px.line(df_line, x='Date', y='Audits', markers=True)
    fig_line.update_traces(line_color='#1d4ed8', line_width=3)
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#0f172a'))
    st.plotly_chart(fig_line, use_container_width=True)

# Recent Live Audit Logs Table
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Recent Audit Requests & Dynamic Ledger Logs")

if live_logs:
    table_data = []
    for log in reversed(live_logs):
        fields_summary = " | ".join([f"{k}: {v}" for k, v in log.get("fields", [])[:2]]) if log.get("fields") else "Custom Parameters"
        table_data.append({
            "Timestamp": log.get("timestamp", "2026-07-30 18:12:00"),
            "Subject Name": log.get("subject"),
            "Domain": log.get("domain"),
            "Decision Outcome": log.get("outcome"),
            "Risk Index": log.get("risk"),
            "Key Parameters": fields_summary
        })
    df_logs = pd.DataFrame(table_data)
    st.dataframe(df_logs, use_container_width=True)
else:
    st.info("No live audit sessions executed yet. Run an audit on the Home page to populate real-time activity.")
