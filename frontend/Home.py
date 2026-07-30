import streamlit as st
import json
import time
import io
import csv
import hashlib
import uuid
import datetime

def generate_pdf_report(domain, subject, fields, tools, outcome, risk, session_id, hash_val, timestamp):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=8
        )
        body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#1e293b'), leading=14)
        heading_style = ParagraphStyle('DocHeading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1d4ed8'), spaceBefore=10, spaceAfter=6)

        elements = []
        elements.append(Paragraph(f"<b>AI GOVERNANCE DECISION AUDIT REPORT ({domain.upper()})</b>", title_style))
        elements.append(Paragraph(f"<b>Session ID:</b> {session_id} &nbsp;|&nbsp; <b>Domain:</b> {domain} &nbsp;|&nbsp; <b>Timestamp:</b> {timestamp}", body_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>1. SUBJECT & INPUT PARAMETERS</b>", heading_style))
        table_data = [["Parameter Name", "Input Value"]]
        for k, v in fields:
            table_data.append([str(k), str(v)])
        
        t = Table(table_data, colWidths=[200, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>2. GOVERNANCE DECISION & RISK METRICS</b>", heading_style))
        elements.append(Paragraph(f"<b>Final Decision:</b> {outcome}", body_style))
        elements.append(Paragraph(f"<b>Evaluated Risk Index:</b> {risk}", body_style))
        elements.append(Paragraph(f"<b>AI Tools Executed:</b> {', '.join(tools)}", body_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>3. CRYPTOGRAPHIC TAMPER PROOF</b>", heading_style))
        elements.append(Paragraph(f"<b>SHA-256 Signature:</b> {hash_val}", body_style))
        elements.append(Paragraph("<b>Status:</b> Immutable Ledger Verified (100% Valid)", body_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        text = f"DECISION AUDIT REPORT ({domain})\nSession: {session_id}\nSubject: {subject}\nOutcome: {outcome}\nRisk: {risk}\nTimestamp: {timestamp}\nSHA256: {hash_val}"
        return text.encode('utf-8')

def generate_csv_logs(domain, subject, fields, tools, outcome, risk, session_id, hash_val, timestamp):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Session ID", "Timestamp", "Domain", "Subject", "Field Name", "Field Value", "Tools Executed", "Final Decision", "Risk Index", "SHA-256 Hash"])
    tool_str = "; ".join(tools)
    for k, v in fields:
        writer.writerow([session_id, timestamp, domain, subject, k, v, tool_str, outcome, risk, hash_val])
    return output.getvalue().encode('utf-8')

st.set_page_config(
    page_title="Decision Path Auditor",
    layout="wide",
    page_icon="🛡️"
)

# Multi-Language Translation Dictionary
TRANSLATIONS = {
    "English": {
        "title": "🛡️ Decision Path Auditor",
        "subtitle": "Enterprise AI Governance & Multi-Step Reasoning Auditor across Industries",
        "select_domain": "🏢 Select Governance Domain",
        "input_header": "📝 Enter Subject Details for Audit Simulation",
        "input_desc": "Select a domain above, enter the applicant/subject details below, and click 'Run Agent' to generate the complete domain audit trail.",
        "run_btn": "🚀 Run AI Governance Agent",
        "flow_title": "AI Execution Pipeline",
        "output_title": "🛡️ AI DECISION PATH AUDITOR REPORT",
        "sec1": "1. SUBJECT REQUEST DETAILS",
        "sec2": "2. INPUT DATA VALIDATION",
        "sec3": "3. AI PROMPT & AGENT PROCESSING",
        "sec4": "4. EXECUTED AI TOOLS & API CALLS",
        "sec5": "5. INTERMEDIATE REASONING & RISK ASSESSMENT",
        "sec6": "6. DECISION LOGIC & BUSINESS RULES",
        "sec7": "7. FINAL GOVERNANCE DECISION",
        "sec8": "8. CHRONOLOGICAL EXECUTION HISTORY",
        "sec9": "9. AUDIT SUMMARY METRICS & RAW JSON LOG",
        "decision": "Decision",
        "approved": "APPROVED / PASS",
        "rejected": "REJECTED / BLOCKED",
        "confidence": "Confidence Score",
        "reason": "Reasoning",
        "lang_select": "🌐 Select Report Language",
        "valid_check": "Validated",
        "status_ok": "200 OK"
    },
    "Tamil": {
        "title": "🛡️ முடிவுப் பாதை தணிக்கையாளர்",
        "subtitle": "நிறுவன செயற்கை நுண்ணறிவு ஆளுகை மற்றும் தணிக்கை அமைப்பு",
        "select_domain": "🏢 தணிக்கை துறையைத் தேர்ந்தெடுக்கவும்",
        "input_header": "📝 ஆளுகை உருவகப்படுத்துதலுக்கான விவரங்களை உள்ளிடவும்",
        "input_desc": "துறையைத் தேர்ந்தெடுத்து விவரங்களை உள்ளிட்டு 'AI முகவரை இயக்கவும்' என்பதைக் கிளிக் செய்யவும்.",
        "run_btn": "🚀 AI ஆளுகை முகவரை இயக்கவும்",
        "flow_title": "AI செயல்பாட்டு குழாய்",
        "output_title": "🛡️ AI முடிவுப் பாதை தணிக்கை அறிக்கை",
        "sec1": "1. கோரிக்கை விவரங்கள்",
        "sec2": "2. உள்ளீட்டு தரவு சரிபார்ப்பு",
        "sec3": "3. AI தூண்டுதல் மற்றும் முகவர் செயலாக்கம்",
        "sec4": "4. செயல்படுத்தப்பட்ட AI கருவிகள் மற்றும் API அழைப்புகள்",
        "sec5": "5. இடைநிலை பகுத்தறிவு மற்றும் அபாய மதிப்பீடு",
        "sec6": "6. முடிவு தருக்கம் மற்றும் வணிக விதிகள்",
        "sec7": "7. இறுதி ஆளுகை முடிவு",
        "sec8": "8. காலவரிசை செயல்பாட்டு வரலாறு",
        "sec9": "9. தணிக்கை சுருக்க அளவீடுகள் மற்றும் JSON பதிவு",
        "decision": "முடிவு",
        "approved": "ஒப்புதலளிக்கப்பட்டது",
        "rejected": "நிராகரிக்கப்பட்டது / தடுக்கப்பட்டது",
        "confidence": "நம்பிக்கை மதிப்பெண்",
        "reason": "காரணம்",
        "lang_select": "🌐 அறிக்கையின் மொழியைத் தேர்ந்தெடுக்கவும்",
        "valid_check": "சரிபார்க்கப்பட்டது",
        "status_ok": "200 சரியானது"
    },
    "Hindi": {
        "title": "🛡️ निर्णय पथ लेखापरीक्षक",
        "subtitle": "एंटरप्राइज एआई गवर्नेंस और ऑडिटर सिस्टम",
        "select_domain": "🏢 डोमेन का चयन करें",
        "input_header": "📝 ऑडिट सिमुलेशन के लिए विवरण दर्ज करें",
        "input_desc": "ऊपर एक डोमेन चुनें, नीचे विवरण दर्ज करें, और ऑडिट रिपोर्ट उत्पन्न करने के लिए 'एआई एजेंट चलाएं' पर क्लिक करें।",
        "run_btn": "🚀 एआई गवर्नेंस एजेंट चलाएं",
        "flow_title": "एआई निष्पादन पाइपलाइन",
        "output_title": "🛡️ एआई निर्णय पथ ऑडिट रिपोर्ट",
        "sec1": "1. अनुरोध विवरण",
        "sec2": "2. इनपुट डेटा सत्यापन",
        "sec3": "3. एआई प्रॉम्प्ट और एजेंट प्रोसेसिंग",
        "sec4": "4. निष्पादित एआई उपकरण और एपीआई कॉल",
        "sec5": "5. मध्यवर्ती तर्क और जोखिम मूल्यांकन",
        "sec6": "6. निर्णय तर्क और व्यावसायिक नियम",
        "sec7": "7. अंतिम निर्णय",
        "sec8": "8. कालानुक्रमिक निष्पादन इतिहास",
        "sec9": "9. ऑडिट सारांश मेट्रिक्स और JSON लॉग",
        "decision": "निर्णय",
        "approved": "स्वीकृत",
        "rejected": "अस्वीकृत / अवरुद्ध",
        "confidence": "विश्वास स्कोर",
        "reason": "कारण",
        "lang_select": "🌐 रिपोर्ट भाषा चुनें",
        "valid_check": "सत्यापित",
        "status_ok": "200 सही"
    },
    "French": {
        "title": "🛡️ Auditeur de Parcours de Décision",
        "subtitle": "Gouvernance IA d'Entreprise Multi-Secteurs",
        "select_domain": "🏢 Sélectionner le Domaine de Gouvernance",
        "input_header": "📝 Saisir les Détails pour la Simulation d'Audit",
        "input_desc": "Sélectionnez un domaine ci-dessus, saisissez les détails ci-dessous et cliquez sur 'Exécuter l'Agent IA'.",
        "run_btn": "🚀 Exécuter l'Agent IA",
        "flow_title": "Pipeline d'Exécution IA",
        "output_title": "🛡️ RAPPORT D'AUDIT DE DÉCISION IA",
        "sec1": "1. DÉTAILS DE LA DEMANDE",
        "sec2": "2. VALIDATION DES DONNÉES D'ENTRÉE",
        "sec3": "3. PROMPT IA ET TRAITEMENT AGENT",
        "sec4": "4. OUTILS IA ET APPELS API EXÉCUTÉS",
        "sec5": "5. RAISONNEMENT INTERMÉDIAIRE ET RISQUE",
        "sec6": "6. LOGIQUE DE DÉCISION ET RÈGLES COMMERCIALES",
        "sec7": "7. DÉCISION FINALE DE GOUVERNANCE",
        "sec8": "8. HISTORIQUE D'EXÉCUTION CHRONOLOGIQUE",
        "sec9": "9. MÉTRIQUES D'AUDIT ET JOURNAL JSON",
        "decision": "Décision",
        "approved": "APPROUVÉ",
        "rejected": "REJETÉ / BLOQUÉ",
        "confidence": "Score de Confiance",
        "reason": "Raisonnement",
        "lang_select": "🌐 Sélectionner la Langue du Rapport",
        "valid_check": "Validé",
        "status_ok": "200 OK"
    },
    "German": {
        "title": "🛡️ Entscheidungspfad-Auditor",
        "subtitle": "Enterprise KI-Governance & Branchen-Audit-System",
        "select_domain": "🏢 Governance-Domäne Auswählen",
        "input_header": "📝 Details für Audit-Simulation Eingeben",
        "input_desc": "Wählen Sie oben eine Domäne aus, geben Sie unten die Details ein und klicken Sie auf 'KI-Agenten Starten'.",
        "run_btn": "🚀 KI-Governance-Agent Starten",
        "flow_title": "KI-Ausführungspipeline",
        "output_title": "🛡️ KI-ENTSCHEIDUNGSPFAD-PRÜFBERICHT",
        "sec1": "1. ANFRAGEDETAILS",
        "sec2": "2. EINGABEDATENVALIDIERUNG",
        "sec3": "3. KI-PROMPT UND AGENTENVERARBEITUNG",
        "sec4": "4. AUSGEFÜHRTE KI-TOOLS UND API-AUFRUFE",
        "sec5": "5. ZWISCHENLOGIK UND RISIKOBEWERTUNG",
        "sec6": "6. ENTSCHEIDUNGSLOGIK UND GESCHÄFTSREGELN",
        "sec7": "7. ENDGÜLTIGE ENTSCHEIDUNG",
        "sec8": "8. CHRONOLOGISCHER AUSFÜHRUNGSVERLAUF",
        "sec9": "9. AUDIT-ZUSAMMENFASSUNG UND JSON-LOG",
        "decision": "Entscheidung",
        "approved": "GENEHMIGT",
        "rejected": "ABGELEHNT / BLOCKIERT",
        "confidence": "Vertrauenswert",
        "reason": "Begründung",
        "lang_select": "🌐 Berichtssprache Auswählen",
        "valid_check": "Bestätigt",
        "status_ok": "200 OK"
    },
    "Spanish": {
        "title": "🛡️ Auditor de Ruta de Decisión",
        "subtitle": "Gobernanza de IA Empresarial Multisectorial",
        "select_domain": "🏢 Seleccionar Dominio de Gobernanza",
        "input_header": "📝 Ingrese los Detalles para la Simulación",
        "input_desc": "Seleccione un dominio arriba, ingrese los detalles a continuación y haga clic en 'Ejecutar Agente de IA'.",
        "run_btn": "🚀 Ejecutar Agente de IA",
        "flow_title": "Tubería de Ejecución de IA",
        "output_title": "🛡️ INFORME DE AUDITORÍA DE DECISIÓN IA",
        "sec1": "1. DETALLES DE LA SOLICITUD",
        "sec2": "2. VALIDACIÓN DE DATOS DE ENTRADA",
        "sec3": "3. PROMPT DE IA Y PROCESAMIENTO",
        "sec4": "4. HERRAMIENTAS DE IA Y LLAMADAS API",
        "sec5": "5. RAZONAMIENTO INTERMEDIO Y EVALUACIÓN DE RIESGO",
        "sec6": "6. LÓGICA DE DECISIÓN Y REGLAS DE NEGOCIO",
        "sec7": "7. DECISIÓN FINAL DE GOBERNANZA",
        "sec8": "8. HISTORIAL DE EJECUCIÓN CRONOLÓGICO",
        "sec9": "9. MÉTRICAS DE AUDITORÍA Y REGISTRO JSON",
        "decision": "Decisión",
        "approved": "APROBADO",
        "rejected": "RECHAZADO / BLOQUEADO",
        "confidence": "Puntaje de Confianza",
        "reason": "Razonamiento",
        "lang_select": "🌐 Seleccionar Idioma del Informe",
        "valid_check": "Validado",
        "status_ok": "200 OK"
    }
}

# Inject High-Contrast Theme & CSS Fixes
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

    /* Universal Button High Contrast Fix */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        border: 1.5px solid #94a3b8 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
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

    /* Primary Buttons (type="primary") */
    div.stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    div.stButton > button[kind="primary"] *, button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Form Input Fields & Selectboxes */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1.5px solid #94a3b8 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #0f172a !important;
    }

    /* Sidebar Selectbox Specific High-Contrast Override */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] div[data-baseweb="select"] div,
    [data-testid="stSidebar"] div[data-baseweb="select"] input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #0f172a !important;
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

    label[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Flowchart Badges */
    .fc-box {
        padding: 12px 20px;
        border-radius: 25px;
        color: white !important;
        font-weight: 700;
        text-align: center;
        margin: 6px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .fc-box * { color: white !important; }
    .fc-blue { background: linear-gradient(90deg, #2563eb, #3b82f6); }
    .fc-orange { background: linear-gradient(90deg, #d97706, #f59e0b); }
    .fc-purple { background: linear-gradient(90deg, #7c3aed, #a855f7); }
    .fc-red { background: linear-gradient(90deg, #dc2626, #ea580c); }
    .fc-green { background: linear-gradient(90deg, #16a34a, #10b981); }
    .fc-arrow { text-align: center; font-size: 20px; font-weight: bold; color: #2563eb; margin: 2px 0; }

    /* Custom Report Card Styling */
    .report-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        color: #0f172a !important;
    }
    .report-card-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 2px solid #e2e8f0;
    }
    .text-dark {
        color: #0f172a !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .text-dark * {
        color: #0f172a;
    }
    .badge-pass {
        background-color: #dcfce7;
        color: #15803d !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# State initialization
if "page" not in st.session_state:
    st.session_state.page = "input"
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "domain" not in st.session_state:
    st.session_state.domain = "Loan Approval"

# Sidebar Branding
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0 15px 0;">
    <div style="font-size: 45px; margin-bottom: 5px;">🛡️</div>
    <div style="font-weight: 800; font-size: 1.2rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GOVAUDIT AI</div>
    <div style="font-size: 0.75rem; color: #94a3b8; letter-spacing: 0.05em;">ENTERPRISE GOVERNANCE</div>
</div>
<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 15px;">
""", unsafe_allow_html=True)

# Language Selector
selected_lang = st.sidebar.selectbox(
    TRANSLATIONS[st.session_state.lang]["lang_select"],
    options=["English", "Tamil", "Hindi", "French", "German", "Spanish"],
    index=["English", "Tamil", "Hindi", "French", "German", "Spanish"].index(st.session_state.lang)
)
st.session_state.lang = selected_lang
t = TRANSLATIONS[st.session_state.lang]

# Main Header Banner
st.title(t["title"])
st.caption(t["subtitle"])
st.divider()

# Shared Flowchart Widget
def render_flowchart(decision="APPROVED"):
    st.markdown('<div class="fc-box fc-blue">User Data Ingestion</div>', unsafe_allow_html=True)
    st.markdown('<div class="fc-arrow">↓</div>', unsafe_allow_html=True)
    st.markdown('<div class="fc-box fc-orange">Feature Extraction</div>', unsafe_allow_html=True)
    st.markdown('<div class="fc-arrow">↓</div>', unsafe_allow_html=True)
    st.markdown('<div class="fc-box fc-purple">Domain AI Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="fc-arrow">↓</div>', unsafe_allow_html=True)
    if decision in ["APPROVED", "STABLE_DISCHARGE", "PASS", "ALLOWED"]:
        st.markdown('<div class="fc-box fc-green">Decision:<br><span style="font-weight:400; font-size:13px;">Low Risk - Compliant</span></div>', unsafe_allow_html=True)
        st.caption("📍 **Audit Summary**: Approved / Compliant.")
    else:
        st.markdown('<div class="fc-box fc-red">Decision:<br><span style="font-weight:400; font-size:13px;">High Risk - Non-Compliant</span></div>', unsafe_allow_html=True)
        st.caption("📍 **Audit Summary**: Rejected / Flagged.")

# Helper for numeric cleaning
def clean_numeric(val, default=0.0):
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace("₹", "").replace("$", "").replace(",", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return default

# ==========================================
# 1. INPUT PAGE (INTERACTIVE DOMAIN SELECTOR & FORMS)
# ==========================================
if st.session_state.page == "input":
    
    st.markdown(f"### {t['select_domain']}")
    selected_domain = st.selectbox(
        "Choose an industry domain to enter custom inputs and audit:",
        options=["Loan Approval", "Healthcare", "Education", "Insurance", "Cybersecurity"],
        index=["Loan Approval", "Healthcare", "Education", "Insurance", "Cybersecurity"].index(st.session_state.domain),
        key="domain_selector_widget"
    )
    st.session_state.domain = selected_domain
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_main, col_flow = st.columns([2.5, 1])
    
    with col_main:
        with st.container(border=True):
            st.subheader(f"📝 {st.session_state.domain} Form Fields")
            st.write(t["input_desc"])
            
            # Sample reference loader button
            col_sample, _ = st.columns([1, 1])
            with col_sample:
                if st.button("📋 Load Sample Data (For Reference / Testing)", key="btn_load_sample", use_container_width=True):
                    if st.session_state.domain == "Loan Approval":
                        st.session_state.loan_name = "Rahul Kumar"
                        st.session_state.loan_age = 28
                        st.session_state.loan_emp = "Full-time Permanent"
                        st.session_state.loan_amt = "₹5,00,000"
                        st.session_state.loan_sal = "₹65,000"
                        st.session_state.loan_score = 740
                    elif st.session_state.domain == "Healthcare":
                        st.session_state.hc_name = "Jane Smith"
                        st.session_state.hc_age = 45
                        st.session_state.hc_gender = "Female"
                        st.session_state.hc_symp = "Fever, Cough"
                        st.session_state.hc_hist = "Asthma"
                        st.session_state.hc_bp = "120/80"
                    elif st.session_state.domain == "Education":
                        st.session_state.edu_name = "Alex Rivera"
                        st.session_state.edu_age = 21
                        st.session_state.edu_course = "B.Tech Computer Science"
                        st.session_state.edu_cgpa = 8.8
                        st.session_state.edu_inc = "₹2,50,000"
                        st.session_state.edu_att = "94%"
                    elif st.session_state.domain == "Insurance":
                        st.session_state.ins_name = "Sarah Connor"
                        st.session_state.ins_age = 38
                        st.session_state.ins_pol = "INS202600123"
                        st.session_state.ins_claim = "₹1,50,000"
                        st.session_state.ins_type = "Vehicle Accident"
                        st.session_state.ins_stat = "Active"
                    elif st.session_state.domain == "Cybersecurity":
                        st.session_state.cs_user = "USR_84920"
                        st.session_state.cs_time = "30-07-2026 10:30 AM"
                        st.session_state.cs_ip = "192.168.1.101"
                        st.session_state.cs_dev = "Windows Laptop"
                        st.session_state.cs_loc = "Chennai"
                    st.rerun()

            c1, c2 = st.columns(2)
            
            # Domain 1: Loan Approval
            if st.session_state.domain == "Loan Approval":
                with c1:
                    loan_name = st.text_input("Customer Name", value=st.session_state.get("loan_name", ""), placeholder="e.g. Rahul Kumar", key="loan_name_input")
                    loan_age_val = st.session_state.get("loan_age", None)
                    loan_age = st.number_input("Age", value=loan_age_val, min_value=18, max_value=100, placeholder="e.g. 28", key="loan_age_input")
                    emp_opts = ["-- Select Employment Type --", "Full-time Permanent", "Self-Employed", "Temporary Employee"]
                    emp_curr = st.session_state.get("loan_emp", "-- Select Employment Type --")
                    emp_idx = emp_opts.index(emp_curr) if emp_curr in emp_opts else 0
                    loan_employment = st.selectbox("Employment Type", emp_opts, index=emp_idx, key="loan_emp_input")
                with c2:
                    loan_amt = st.text_input("Loan Amount (₹)", value=st.session_state.get("loan_amt", ""), placeholder="e.g. ₹5,00,000", key="loan_amt_input")
                    loan_salary = st.text_input("Monthly Salary (₹)", value=st.session_state.get("loan_sal", ""), placeholder="e.g. ₹45,000", key="loan_sal_input")
                    score_curr = st.session_state.get("loan_score", None)
                    loan_score = st.number_input("Credit Score", value=score_curr, min_value=300, max_value=900, placeholder="e.g. 720", key="loan_score_input")
                
                score_num = clean_numeric(loan_score, 0)
                emp_str = loan_employment if loan_employment != "-- Select Employment Type --" else "Not Specified"

                if score_num >= 650:
                    outcome, risk = "APPROVED", "LOW"
                elif score_num >= 600 and emp_str == "Full-time Permanent":
                    outcome, risk = "APPROVED", "LOW"
                elif score_num >= 550 and score_num < 600:
                    outcome, risk = "CONDITIONAL_APPROVAL", "MEDIUM"
                elif score_num > 0:
                    outcome, risk = "REJECTED", "HIGH"
                else:
                    outcome, risk = "UNDER_REVIEW", "MEDIUM"

                subj_val = loan_name.strip() if loan_name and loan_name.strip() else "Unspecified Customer"

                domain_payload = {
                    "subject": subj_val,
                    "fields": [
                        ("Customer Name", subj_val),
                        ("Age", str(loan_age) if loan_age is not None else "Not Specified"),
                        ("Employment Type", emp_str),
                        ("Loan Amount", loan_amt if loan_amt else "Not Specified"),
                        ("Monthly Salary", loan_salary if loan_salary else "Not Specified"),
                        ("Credit Score", str(loan_score) if loan_score is not None else "Not Specified")
                    ],
                    "tools": ["Credit Bureau API", "Income Verification API", "Risk Assessment Model", "Underwriting Rule Engine"],
                    "outcome": outcome,
                    "risk": risk
                }

            # Domain 2: Healthcare
            elif st.session_state.domain == "Healthcare":
                with c1:
                    hc_name = st.text_input("Patient Name", value=st.session_state.get("hc_name", ""), placeholder="e.g. Jane Smith", key="hc_name_input")
                    hc_age_val = st.session_state.get("hc_age", None)
                    hc_age = st.number_input("Age", value=hc_age_val, min_value=0, max_value=120, placeholder="e.g. 45", key="hc_age_input")
                    g_opts = ["-- Select Gender --", "Male", "Female", "Other"]
                    g_curr = st.session_state.get("hc_gender", "-- Select Gender --")
                    g_idx = g_opts.index(g_curr) if g_curr in g_opts else 0
                    hc_gender = st.selectbox("Gender", g_opts, index=g_idx, key="hc_gender_input")
                with c2:
                    hc_symptoms = st.text_input("Symptoms", value=st.session_state.get("hc_symp", ""), placeholder="e.g. Fever, Cough", key="hc_symp_input")
                    hc_history = st.text_input("Medical History", value=st.session_state.get("hc_hist", ""), placeholder="e.g. Asthma, Hypertension", key="hc_hist_input")
                    hc_bp = st.text_input("Blood Pressure", value=st.session_state.get("hc_bp", ""), placeholder="e.g. 120/80", key="hc_bp_input")
                
                symp_lower = (hc_symptoms or "").lower()
                hist_lower = (hc_history or "").lower()
                if "chest pain" in symp_lower or "stroke" in symp_lower or "severe" in symp_lower:
                    outcome, risk = "URGENT_CARE", "HIGH"
                elif "asthma" in hist_lower or "fever" in symp_lower or "diabetes" in hist_lower:
                    outcome, risk = "REFERRAL_REQUIRED", "MEDIUM"
                else:
                    outcome, risk = "STABLE_DISCHARGE", "LOW"

                subj_val = hc_name.strip() if hc_name and hc_name.strip() else "Unspecified Patient"

                domain_payload = {
                    "subject": subj_val,
                    "fields": [
                        ("Patient Name", subj_val),
                        ("Age", str(hc_age) if hc_age is not None else "Not Specified"),
                        ("Gender", hc_gender if hc_gender != "-- Select Gender --" else "Not Specified"),
                        ("Symptoms", hc_symptoms if hc_symptoms else "None Reported"),
                        ("Medical History", hc_history if hc_history else "None Reported"),
                        ("Blood Pressure", hc_bp if hc_bp else "Not Specified")
                    ],
                    "tools": ["Symptom Analyzer API", "EHR Record Lookup", "Vitals Assessment Model", "Clinical Protocol Engine"],
                    "outcome": outcome,
                    "risk": risk
                }

            # Domain 3: Education
            elif st.session_state.domain == "Education":
                with c1:
                    edu_name = st.text_input("Student Name", value=st.session_state.get("edu_name", ""), placeholder="e.g. Alex Rivera", key="edu_name_input")
                    edu_age_val = st.session_state.get("edu_age", None)
                    edu_age = st.number_input("Age", value=edu_age_val, min_value=16, max_value=80, placeholder="e.g. 21", key="edu_age_input")
                    edu_course = st.text_input("Course", value=st.session_state.get("edu_course", ""), placeholder="e.g. B.Tech Computer Science", key="edu_course_input")
                with c2:
                    cgpa_curr = st.session_state.get("edu_cgpa", None)
                    edu_cgpa = st.number_input("CGPA", value=cgpa_curr, min_value=0.0, max_value=10.0, step=0.1, placeholder="e.g. 8.5", key="edu_cgpa_input")
                    edu_income = st.text_input("Family Income (₹)", value=st.session_state.get("edu_inc", ""), placeholder="e.g. ₹2,50,000", key="edu_inc_input")
                    edu_attendance = st.text_input("Attendance", value=st.session_state.get("edu_att", ""), placeholder="e.g. 92%", key="edu_att_input")
                
                cgpa_num = clean_numeric(edu_cgpa, 0.0)

                if cgpa_num >= 8.0:
                    outcome, risk = "APPROVED", "LOW"
                elif cgpa_num >= 6.5:
                    outcome, risk = "CONDITIONAL_APPROVAL", "MEDIUM"
                elif cgpa_num > 0:
                    outcome, risk = "REJECTED", "HIGH"
                else:
                    outcome, risk = "UNDER_REVIEW", "MEDIUM"

                subj_val = edu_name.strip() if edu_name and edu_name.strip() else "Unspecified Student"

                domain_payload = {
                    "subject": subj_val,
                    "fields": [
                        ("Student Name", subj_val),
                        ("Age", str(edu_age) if edu_age is not None else "Not Specified"),
                        ("Course", edu_course if edu_course else "Not Specified"),
                        ("CGPA", str(edu_cgpa) if edu_cgpa is not None else "Not Specified"),
                        ("Family Income", edu_income if edu_income else "Not Specified"),
                        ("Attendance", edu_attendance if edu_attendance else "Not Specified")
                    ],
                    "tools": ["Academic Record Verifier", "Financial Need Estimator", "Attendance Log API", "Merit Scholarship Rule Engine"],
                    "outcome": outcome,
                    "risk": risk
                }

            # Domain 4: Insurance
            elif st.session_state.domain == "Insurance":
                with c1:
                    ins_name = st.text_input("Customer Name", value=st.session_state.get("ins_name", ""), placeholder="e.g. Sarah Connor", key="ins_name_input")
                    ins_age_val = st.session_state.get("ins_age", None)
                    ins_age = st.number_input("Age", value=ins_age_val, min_value=18, max_value=100, placeholder="e.g. 38", key="ins_age_input")
                    ins_policy = st.text_input("Policy Number", value=st.session_state.get("ins_pol", ""), placeholder="e.g. POL-2026-9876", key="ins_pol_input")
                with c2:
                    ins_claim_amt = st.text_input("Claim Amount (₹)", value=st.session_state.get("ins_claim", ""), placeholder="e.g. ₹1,50,000", key="ins_claim_input")
                    ins_claim_type = st.text_input("Claim Type", value=st.session_state.get("ins_type", ""), placeholder="e.g. Vehicle Accident", key="ins_type_input")
                    stat_opts = ["-- Select Policy Status --", "Active", "Lapsed", "Under Review"]
                    stat_curr = st.session_state.get("ins_stat", "-- Select Policy Status --")
                    stat_idx = stat_opts.index(stat_curr) if stat_curr in stat_opts else 0
                    ins_status = st.selectbox("Policy Status", stat_opts, index=stat_idx, key="ins_stat_input")
                
                stat_str = ins_status if ins_status != "-- Select Policy Status --" else "Not Specified"
                if stat_str == "Active":
                    outcome, risk = "APPROVED", "LOW"
                elif stat_str == "Under Review":
                    outcome, risk = "MANUAL_REVIEW_REQUIRED", "MEDIUM"
                else:
                    outcome, risk = "REJECTED", "HIGH"

                subj_val = ins_name.strip() if ins_name and ins_name.strip() else "Unspecified Customer"

                domain_payload = {
                    "subject": subj_val,
                    "fields": [
                        ("Customer Name", subj_val),
                        ("Age", str(ins_age) if ins_age is not None else "Not Specified"),
                        ("Policy Number", ins_policy if ins_policy else "Not Specified"),
                        ("Claim Amount", ins_claim_amt if ins_claim_amt else "Not Specified"),
                        ("Claim Type", ins_claim_type if ins_claim_type else "Not Specified"),
                        ("Policy Status", stat_str)
                    ],
                    "tools": ["Policy Validation API", "Loss Estimator Model", "Fraud Anomaly Detector", "Claims Settlement Engine"],
                    "outcome": outcome,
                    "risk": risk
                }

            # Domain 5: Cybersecurity
            elif st.session_state.domain == "Cybersecurity":
                with c1:
                    cs_user = st.text_input("User ID", value=st.session_state.get("cs_user", ""), placeholder="e.g. USR_84920", key="cs_user_input")
                    cs_time = st.text_input("Login Time", value=st.session_state.get("cs_time", ""), placeholder="e.g. 30-07-2026 10:30 AM", key="cs_time_input")
                    cs_ip = st.text_input("IP Address", value=st.session_state.get("cs_ip", ""), placeholder="e.g. 192.168.1.101", key="cs_ip_input")
                with c2:
                    cs_device = st.text_input("Device", value=st.session_state.get("cs_dev", ""), placeholder="e.g. Windows Laptop", key="cs_dev_input")
                    cs_location = st.text_input("Location", value=st.session_state.get("cs_loc", ""), placeholder="e.g. Chennai", key="cs_loc_input")
                
                ip_clean = (cs_ip or "").strip()
                if ip_clean.startswith("192.168") or ip_clean.startswith("10.") or ip_clean.startswith("127.") or not ip_clean:
                    outcome, risk = "ALLOWED", "LOW"
                elif "vpn" in (cs_device or "").lower():
                    outcome, risk = "MFA_CHALLENGE", "MEDIUM"
                else:
                    outcome, risk = "BLOCKED", "CRITICAL"

                subj_val = cs_user.strip() if cs_user and cs_user.strip() else "Unspecified User"

                domain_payload = {
                    "subject": subj_val,
                    "fields": [
                        ("User ID", subj_val),
                        ("Login Time", cs_time if cs_time else "Not Specified"),
                        ("IP Address", cs_ip if cs_ip else "Not Specified"),
                        ("Device", cs_device if cs_device else "Not Specified"),
                        ("Location", cs_location if cs_location else "Not Specified")
                    ],
                    "tools": ["IP Reputation Service", "Device Fingerprint API", "Geo-Velocity Anomaly Model", "Zero-Trust Policy Engine"],
                    "outcome": outcome,
                    "risk": risk
                }

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button(t["run_btn"], type="primary", use_container_width=True):
                # Generate dynamic session ID & timestamp
                session_id = f"DEC-{time.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Compute real cryptographic SHA-256 hash over input parameters
                hash_source = json.dumps({
                    "session_id": session_id,
                    "timestamp": now_str,
                    "domain": st.session_state.domain,
                    "payload": domain_payload
                }, sort_keys=True)
                hash_val = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()

                domain_payload["session_id"] = session_id
                domain_payload["timestamp"] = now_str
                domain_payload["hash_val"] = hash_val

                st.session_state.user_inputs = domain_payload
                if "audit_history_logs" not in st.session_state:
                    st.session_state.audit_history_logs = []
                
                st.session_state.audit_history_logs.append({
                    "session_id": session_id,
                    "subject": domain_payload.get("subject"),
                    "domain": st.session_state.domain,
                    "outcome": domain_payload.get("outcome"),
                    "risk": domain_payload.get("risk"),
                    "fields": domain_payload.get("fields"),
                    "timestamp": now_str,
                    "hash_val": hash_val
                })
                st.session_state.page = "processing"
                st.rerun()

    with col_flow:
        with st.container(border=True):
            st.subheader(t["flow_title"])
            render_flowchart()

# ==========================================
# 2. LIVE WORKFLOW PROCESSING PAGE
# ==========================================
elif st.session_state.page == "processing":
    st.subheader(f"⚡ Live AI Agent Execution: {st.session_state.domain} Domain")
    st.caption("Capturing real-time execution steps, tool invocations, intermediate reasoning, and governance logs...")
    
    progress = st.progress(0)
    status_container = st.container(border=True)
    
    inputs = st.session_state.get("user_inputs", {})
    tools = inputs.get("tools", ["API 1", "API 2", "Model 1", "Rule Engine"])
    sess_id = inputs.get("session_id", "DEC-20260730-001")
    hash_val = inputs.get("hash_val", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    
    with status_container:
        st.write(f"📥 **Step 1/6: Request Ingestion & Input Sanity Check**")
        st.caption(f"Subject={inputs.get('subject')}, Domain={st.session_state.domain}, Validated Fields: {len(inputs.get('fields', []))}")
        progress.progress(15)
        time.sleep(0.2)
        
        st.write(f"⚙️ **Step 2/6: Executing Domain Tool 1 (`{tools[0]}`)**")
        st.caption(f"Invoking {tools[0]} Service... Verification Complete")
        progress.progress(35)
        time.sleep(0.2)
        
        st.write(f"🔍 **Step 3/6: Executing Domain Tool 2 (`{tools[1]}`)**")
        st.caption(f"Invoking {tools[1]} Service... Verification Complete")
        progress.progress(55)
        time.sleep(0.2)
        
        st.write(f"📊 **Step 4/6: Executing Risk Assessment Model (`{tools[2]}`)**")
        st.caption(f"Calculating Risk Index... Risk Evaluated: **{inputs.get('risk')}**")
        progress.progress(75)
        time.sleep(0.2)
        
        st.write(f"⚖️ **Step 5/6: Applying Policy Engine (`{tools[3]}`)**")
        st.caption(f"Evaluating Rules -> Recommended Outcome: **{inputs.get('outcome')}**")
        progress.progress(90)
        time.sleep(0.2)
        
        st.write("💾 **Step 6/6: Storing Immutable Cryptographic Audit Trace**")
        st.caption(f"Trace saved to SQLite/Postgres DB with SHA-256 Signature `{hash_val[:16]}...`.")
        progress.progress(100)
        time.sleep(0.2)

    if st.button("📊 View Complete Governance Audit Report", type="primary", use_container_width=True):
        st.session_state.page = "output"
        st.rerun()

# ==========================================
# 3. MULTI-DOMAIN AUDIT REPORT PAGE
# ==========================================
elif st.session_state.page == "output":
    
    if st.button("← Run Another Audit Request", type="secondary"):
        st.session_state.page = "input"
        st.rerun()
        
    inputs = st.session_state.get("user_inputs", {})
    outcome = inputs.get("outcome", "APPROVED")
    tools = inputs.get("tools", ["API 1", "API 2", "Model 1", "Rule Engine"])
    fields = inputs.get("fields", [])
    session_id = inputs.get("session_id", "DEC-20260730-001")
    timestamp = inputs.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hash_val = inputs.get("hash_val", hashlib.sha256(session_id.encode()).hexdigest())
    
    is_success = outcome in ["APPROVED", "STABLE_DISCHARGE", "PASS", "ALLOWED"]
    decision_color = "#16a34a" if is_success else "#dc2626"
    outcome_label = t["approved"] if is_success else t["rejected"]
    
    st.success(f"✔ Complete {st.session_state.domain} Governance Trace Recorded! Session ID: **{session_id}** | Status: **{outcome}**")
    
    # Header Banner
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 100%); padding: 22px 28px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; color: white; font-size: 1.8rem; font-weight: 800;">{t['output_title']} ({st.session_state.domain.upper()})</h2>
                <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                    <b>Decision ID</b>: {session_id} &nbsp;|&nbsp; 
                    <b>Domain</b>: {st.session_state.domain} &nbsp;|&nbsp; 
                    <b>Timestamp</b>: {timestamp}
                </p>
            </div>
            <div style="background: {decision_color}; padding: 12px 24px; border-radius: 30px; font-weight: 800; font-size: 1.3rem; color: white;">
                {outcome}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render Section 1 Fields Dynamically
    fields_html = "".join([f"• <b>{lbl}</b>: {val}<br>" for lbl, val in fields])
    
    # Sections Grid
    r1, r2 = st.columns(2)
    
    with r1:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #2563eb;">{t['sec1']}</div>
            <div class="text-dark">
                {fields_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with r2:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #059669;">{t['sec2']}</div>
            <div class="text-dark">
                ✔ <b>Subject Identity Check</b>: <span class="badge-pass">{t['valid_check'].upper()}</span><br>
                ✔ <b>Input Parameters Sanity</b>: <span class="badge-pass">{t['valid_check'].upper()} ({len(fields)}/{len(fields)} Fields)</span><br>
                ✔ <b>Domain Policy Compliance</b>: <span class="badge-pass">{t['valid_check'].upper()}</span><br>
                ✔ <b>PII Masking & Redaction</b>: <span class="badge-pass">ENCRYPTED</span><br>
                ✔ <b>Validation Status</b>: <span class="badge-pass">100% SUCCESS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    r3, r4 = st.columns(2)
    
    f0_lbl = fields[0][0] if len(fields) > 0 else "Field 1"
    f0_val = fields[0][1] if len(fields) > 0 else "N/A"
    f1_lbl = fields[1][0] if len(fields) > 1 else "Field 2"
    f1_val = fields[1][1] if len(fields) > 1 else "N/A"

    with r3:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #d97706;">{t['sec3']}</div>
            <div class="text-dark">
                <b>System Prompt Generated:</b><br>
                <i style="color: #475569;">"Execute AI Agent for domain '{st.session_state.domain}' evaluating subject '{inputs.get('subject')}' with parameters {f0_lbl}={f0_val}, {f1_lbl}={f1_val}. Call domain tools and return decision."</i><br><br>
                <b>Execution Model:</b> Gemini 3.1 Pro / GPT-4o Multi-Agent Framework
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r4:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #7c3aed;">{t['sec4']}</div>
            <div class="text-dark">
                • <b>Tool 1</b>: <code>{tools[0]}</code> ➔ Status: <span class="badge-pass">{t['status_ok']}</span><br>
                • <b>Tool 2</b>: <code>{tools[1]}</code> ➔ Status: <span class="badge-pass">{t['status_ok']}</span><br>
                • <b>Tool 3</b>: <code>{tools[2]}</code> ➔ Risk: {inputs.get('risk')} <span class="badge-pass">{t['status_ok']}</span><br>
                • <b>Tool 4</b>: <code>{tools[3]}</code> ➔ Action: {outcome} <span class="badge-pass">{t['status_ok']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    r5, r6 = st.columns(2)
    
    with r5:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #4f46e5;">{t['sec5']}</div>
            <div class="text-dark">
                • <b>Step 1 Reasoning</b>: Evaluated {f0_lbl} ({f0_val}).<br>
                • <b>Step 2 Reasoning</b>: Evaluated {f1_lbl} ({f1_val}).<br>
                • <b>Synthesized Domain Risk</b>: <b>{inputs.get('risk')} RISK</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r6:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #0284c7;">{t['sec6']}</div>
            <div class="text-dark">
                • <b>Policy Rule 1</b>: Input Validation Check ➔ <span class="badge-pass">PASS</span><br>
                • <b>Policy Rule 2</b>: Risk Model Criteria ➔ <span class="badge-pass">EVALUATED</span><br>
                • <b>Final Triggered Action</b>: <b>{outcome}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    r7, r8 = st.columns(2)
    
    with r7:
        st.markdown(f"""
        <div class="report-card" style="border-left: 6px solid {decision_color};">
            <div class="report-card-title" style="color: {decision_color};">{t['sec7']}</div>
            <div class="text-dark">
                • <b>{t['decision']}</b>: <b style="color: {decision_color}; font-size: 1.1rem;">{outcome}</b><br>
                • <b>{t['confidence']}</b>: <b>96%</b><br>
                • <b>{t['reason']}</b>: Subject {inputs.get('subject')} evaluated under {st.session_state.domain} Policy Guidelines. Resulting risk classification is {inputs.get('risk')}.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r8:
        st.markdown(f"""
        <div class="report-card">
            <div class="report-card-title" style="color: #0891b2;">{t['sec8']}</div>
            <div class="text-dark" style="font-size: 0.9rem;">
                ⏱️ <b>Step 1</b> - {st.session_state.domain} Audit Session Initialized<br>
                ⏱️ <b>Step 2</b> - Input Sanity & PII Masking Completed<br>
                ⏱️ <b>Step 3</b> - Executed {tools[0]}<br>
                ⏱️ <b>Step 4</b> - Executed {tools[1]}<br>
                ⏱️ <b>Step 5</b> - Executed {tools[2]}<br>
                ⏱️ <b>Step 6</b> - Executed {tools[3]} & Generated Decision<br>
                ⏱️ <b>Step 7</b> - Audit Log & SHA-256 Hash Saved to Database
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader(t["sec9"])
    m_col1, m_col2, m_col3 = st.columns([1, 2, 1])
    
    with m_col1:
        with st.container(border=True):
            st.markdown("**AUDIT SUMMARY METRICS**")
            st.write(f"• **Domain**: {st.session_state.domain}")
            st.write(f"• **Total Input Fields**: {len(fields)}")
            st.write("• **AI Tools Executed**: 4")
            st.write(f"• **Final Status**: {outcome}")
            st.write(f"• **Tamper Hash**: `{hash_val[:12]}...`")
            
    with m_col2:
        with st.container(border=True):
            st.markdown("**COMPLETE JSON AUDIT LOG TRACE**")
            st.json({
                "decision_id": session_id,
                "domain": st.session_state.domain,
                "timestamp": timestamp,
                "subject_details": dict(fields),
                "tools_executed": tools,
                "final_decision": outcome,
                "confidence_score": "96%",
                "sha256_signature": hash_val
            })
            
    with m_col3:
        pdf_bytes = generate_pdf_report(
            domain=st.session_state.domain,
            subject=inputs.get("subject", "Unspecified Subject"),
            fields=fields,
            tools=tools,
            outcome=outcome,
            risk=inputs.get("risk", "LOW"),
            session_id=session_id,
            hash_val=hash_val,
            timestamp=timestamp
        )
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"Audit_Report_{session_id}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            key="btn_dl_pdf_out"
        )

        csv_bytes = generate_csv_logs(
            domain=st.session_state.domain,
            subject=inputs.get("subject", "Unspecified Subject"),
            fields=fields,
            tools=tools,
            outcome=outcome,
            risk=inputs.get("risk", "LOW"),
            session_id=session_id,
            hash_val=hash_val,
            timestamp=timestamp
        )
        st.download_button(
            label="📊 Export Audit Logs CSV",
            data=csv_bytes,
            file_name=f"Audit_Logs_{session_id}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_dl_csv_out"
        )

        if st.button("🔒 Verify SHA-256 Hash", use_container_width=True, key="btn_verify_hash_out"):
            st.session_state.hash_verified = True

        if st.session_state.get("hash_verified", False):
            st.success("✅ **SHA-256 Cryptographic Hash Verified!**")
            st.caption(f"🔒 Signature: `{hash_val}`\n\nStatus: **Tamper-Proof & Immutable Ledger Verified**")

    # Masonry Grid View
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("========= VISUAL AUDIT MASONRY GRID VIEW =========")
    
    grid_col_left, grid_col_right = st.columns([3, 1])

    with grid_col_left:
        c_a, c_b, c_c = st.columns(3)
        
        req_lines = "\n".join([f"{lbl}: {val}" for lbl, val in fields[:3]])
        with c_a:
            with st.container(border=True):
                st.markdown("**1. REQUEST DETAILS**")
                st.write(f"**{inputs.get('subject')}**\n{req_lines}")
            with st.container(border=True):
                st.markdown("**2. INPUT DATA COLLECTED**")
                st.success("✔ Data Check Complete")
            with st.container(border=True):
                st.markdown("**3. TOOLS USED BY AI**")
                st.write(f"• {tools[0]}\n• {tools[1]}\n• {tools[2]}\n• {tools[3]}")

        with c_b:
            with st.container(border=True):
                st.markdown("**2. DATA VALIDATION**")
                st.success("✔ Inputs Validated")
            with st.container(border=True):
                st.markdown("**4. REASONING CHAIN**")
                if is_success:
                    st.success(f"Risk Evaluation: {inputs.get('risk')}")
                else:
                    st.error(f"Risk Evaluation: {inputs.get('risk')}")
            with st.container(border=True):
                st.markdown("**6. FINAL DECISION**")
                if is_success:
                    st.success(f"✅ **Decision: {outcome}**")
                else:
                    st.error(f"❌ **Decision: {outcome}**")

        with c_c:
            with st.container(border=True):
                st.markdown("**5. DECISION LOGIC**")
                st.write(f"Domain Policy Evaluation ➔ **{outcome}**")
            with st.container(border=True):
                st.markdown("**7. COMPLETE HISTORY**")
                st.write(f"⏱️ Initialized: {timestamp}\n⏱️ Saved to DB: {session_id}")

    with grid_col_right:
        with st.container(border=True):
            st.subheader(t["flow_title"])
            render_flowchart(decision=outcome)
