import streamlit as st
import sys
import os

# Add parent directory to sys.path if not present
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

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
        "status_ok": "200 OK",
        "dash_title": "📊 Enterprise Governance Dashboard",
        "dash_sub": "Global overview of AI decision metrics, compliance ratios, and execution volume",
        "timeline_title": "⏱️ Decision Timeline Reconstructor",
        "timeline_sub": "Step-by-step cryptographic audit reconstruction for any AI session ID",
        "login_title": "🔒 Enterprise Auditor Login",
        "login_sub": "Sign in to access AI governance logs & audit metrics"
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
        "status_ok": "200 சரியானது",
        "dash_title": "📊 நிறுவன ஆளுகை கட்டுப்பாட்டுப் பலகை",
        "dash_sub": "செயற்கை நுண்ணறிவு முடிவுகள் மற்றும் இணக்க அளவீடுகளின் மேலோட்டம்",
        "timeline_title": "⏱️ முடிவு காலவரிசை மறுஉருவாக்கம்",
        "timeline_sub": "எந்தவொரு AI அமர்வு ஐடிக்கும் படிபடியான தணிக்கை மறுஉருவாக்கம்",
        "login_title": "🔒 நிறுவன தணிக்கையாளர் உள்நுழைவு",
        "login_sub": "AI ஆளுகைப் பதிவுகளை அணுக உள்நுழையவும்"
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
        "status_ok": "200 सही",
        "dash_title": "📊 एंटरप्राइज गवर्नेंस डैशबोर्ड",
        "dash_sub": "एआई निर्णय मेट्रिक्स और अनुपालन का अवलोकन",
        "timeline_title": "⏱️ निर्णय समयरेखा पुनर्निर्माण",
        "timeline_sub": "किसी भी एआई सत्र आईडी के लिए चरण-दर-चरण ऑडिट पुनर्निर्माण",
        "login_title": "🔒 एंटरप्राइज ऑडिटर लॉगिन",
        "login_sub": "एआई गवर्नेंस लॉग एक्सेस करने के लिए साइन इन करें"
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
        "status_ok": "200 OK",
        "dash_title": "📊 Tableau de Bord de Gouvernance",
        "dash_sub": "Aperçu global des métriques de décision IA",
        "timeline_title": "⏱️ Reconstructeur de Chronologie",
        "timeline_sub": "Reconstruction d'audit étape par étape",
        "login_title": "🔒 Connexion Auditeur",
        "login_sub": "Connectez-vous pour accéder aux journaux de gouvernance"
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
        "status_ok": "200 OK",
        "dash_title": "📊 Governance-Dashboard",
        "dash_sub": "Gesamtübersicht über KI-Entscheidungskennzahlen",
        "timeline_title": "⏱️ Zeitleisten-Rekonstruktor",
        "timeline_sub": "Schritt-für-Schritt-Prüfung beliebiger Sitzungs-IDs",
        "login_title": "🔒 Auditor-Anmeldung",
        "login_sub": "Melden Sie sich an, um auf Governance-Logs zuzugreifen"
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
        "status_ok": "200 OK",
        "dash_title": "📊 Panel de Gobernanza Empresarial",
        "dash_sub": "Visión general global de métricas de decisión de IA",
        "timeline_title": "⏱️ Reconstructor de Cronología",
        "timeline_sub": "Reconstrucción paso a paso de auditoría para cualquier sesión",
        "login_title": "🔒 Inicio de Sesión de Auditor",
        "login_sub": "Inicie sesión para acceder a los registros de gobernanza"
    }
}

def render_sidebar_translator():
    """Renders the Translator (Language Selector) option in the Streamlit left sidebar consistently across all pages."""
    if "lang" not in st.session_state:
        st.session_state.lang = "English"
    
    current_lang = st.session_state.lang
    lang_opts = ["English", "Tamil", "Hindi", "French", "German", "Spanish"]
    curr_idx = lang_opts.index(current_lang) if current_lang in lang_opts else 0
    
    label = TRANSLATIONS.get(current_lang, TRANSLATIONS["English"]).get("lang_select", "🌐 Select Report Language / Translator")
    
    selected_lang = st.sidebar.selectbox(
        label,
        options=lang_opts,
        index=curr_idx,
        key="global_translator_selectbox"
    )
    
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
        
    if "token" in st.session_state:
        st.sidebar.markdown("---")
        if st.sidebar.button("🔒 Logout", type="primary", use_container_width=True):
            del st.session_state["token"]
            st.rerun()
            
    return TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["English"])
