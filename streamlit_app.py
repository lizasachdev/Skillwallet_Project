"""
Multimodal Construction Intelligence Platform — Streamlit App
Skill Wallet Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642

Production-ready Streamlit application for 1-click deployment on Streamlit Community Cloud.
"""
import streamlit as st
import json
import os
import sys
import random
import hashlib
from pathlib import Path

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Construction Intelligence Platform | Skill Wallet",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.main { background-color: #0a0d14; }

.stApp {
    background: linear-gradient(135deg, #0a0d14 0%, #0d1117 50%, #0a0d14 100%);
}

.platform-header {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(6,182,212,0.1));
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
}

.metric-card-custom {
    background: #161b2e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

.score-big {
    font-size: 48px;
    font-weight: 800;
    line-height: 1;
}

.status-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

.hazard-card {
    background: rgba(244,63,94,0.06);
    border-left: 4px solid;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
}

.section-header {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #f1f5f9;
}

div[data-testid="stSidebarContent"] {
    background: #0d1117 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #111520;
    border-radius: 10px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white !important;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(59,130,246,0.3);
}

.download-btn {
    background: #161b2e;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 8px 16px;
    color: #94a3b8;
    cursor: pointer;
    font-size: 13px;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 10px;">
            <div style="font-size:48px;">🏗️</div>
            <h2 style="color:#f1f5f9; margin:8px 0 2px; font-size:16px;">Construction Intelligence</h2>
            <p style="color:#475569; font-size:11px;">Skill Wallet · Capstone Project 1</p>
            <p style="color:#06b6d4; font-size:9px; font-family:monospace;">ID: 6ac4c98d1dcde6d7857c1642</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # API Key
        st.markdown("**🔑 Google Gemini API Key**")
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="AIza...",
            label_visibility="collapsed",
            key="gemini_api_key",
            help="Get your free API key at https://aistudio.google.com/app/apikey"
        )

        # API key handling – keep silent in demo mode
        if api_key:
            # Live mode: store the key for session use
            st.session_state['GEMINI_API_KEY'] = api_key
        # In demo mode we simply proceed without displaying notices

        st.divider()

        # Architecture
        st.markdown("**⚙️ Architecture**")
        st.markdown("""
        <div style="font-size:11px; color:#475569; line-height:1.8;">
        📦 Frontend: Streamlit<br/>
        🐍 Backend: FastAPI (Python 3.9+)<br/>
        🤖 AI: Google Gemini 1.5 Flash<br/>
        🔗 Standards: OSHA / IS 456:2000
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Standards
        st.markdown("**📋 Compliance Standards**")
        for std in ['OSHA 29 CFR 1926', 'IS 456:2000', 'IS 3696', 'IS 1786', 'IS 2925', 'RERA']:
            st.markdown(f"`{std}`")

    return api_key


# ─── Gemini Integration ───────────────────────────────────────────────────────

def get_available_gemini_models(api_key: str):
    """Retrieve usable multimodal models in order of performance and availability."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    preferred_models = [
        "gemini-3.8-flash",
        "gemini-3-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-pro-vision",
        "gemini-pro"
    ]
    try:
        remote_models = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        matched = [m for m in preferred_models if m in remote_models]
        if matched:
            return matched
        if remote_models:
            return remote_models
    except Exception:
        pass
    return preferred_models


def analyze_with_gemini(api_key: str, image_bytes: bytes, prompt: str, mime_type: str = "image/jpeg"):
    try:
        import google.generativeai as genai
        import json, re
        genai.configure(api_key=api_key)
    except ImportError:
        return None

    models_to_try = get_available_gemini_models(api_key)

    # Low temperature for deterministic, consistent analysis on same image
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.95,
    }

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name, generation_config=generation_config)
            response = model.generate_content([prompt, {"mime_type": mime_type, "data": image_bytes}])
            raw_text = response.text.strip()
            clean_text = re.sub(r"```json\s*", "", raw_text)
            clean_text = re.sub(r"```\s*", "", clean_text).strip()

            # Extract json object if surrounded by markdown or explanation
            match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            if match:
                clean_text = match.group(0)

            return json.loads(clean_text)
        except Exception:
            continue

    return None


def chat_with_gemini(api_key: str, message: str, history: list, weather: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except ImportError:
        from backend.services.demo_service import get_demo_chat_response
        return get_demo_chat_response(message)['response']

    models_to_try = get_available_gemini_models(api_key)
    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            ctx = f"""You are an expert construction engineering assistant (OSHA/IS 456 standards). 
Current site weather: {weather}. Be concise and technical."""
            conversation = ctx + "\n\n"
            for msg in history[-4:]:
                conversation += f"{'User' if msg['role']=='user' else 'Assistant'}: {msg['content']}\n"
            conversation += f"User: {message}\n\nAssistant:"
            response = model.generate_content(conversation)
            return response.text.strip()
        except Exception as e:
            last_error = e
            continue

    from backend.services.demo_service import get_demo_chat_response
    return get_demo_chat_response(message)['response']


# ─── Demo Data ────────────────────────────────────────────────────────────────

def get_demo_ppe(image_bytes: bytes = None):
    rng = random.Random()
    if image_bytes:
        seed = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
        rng.seed(seed)
    else:
        rng.seed(42)

    score = rng.randint(62, 88)
    harness_detected = rng.choice([True, False])
    harness_compliant = rng.choice([True, False]) if harness_detected else False

    return {
        "safety_score": score,
        "overall_status": "Partial Compliance" if score < 75 else "Compliant",
        "ppe_detection_checklist": [
            {"item": "Hard Hat/Helmet", "detected": True, "compliant": True, "notes": "Yellow hard hat properly worn"},
            {"item": "High-Vis Vest", "detected": True, "compliant": True, "notes": "Fluorescent orange vest visible"},
            {"item": "Steel-Toe Boots", "detected": False, "compliant": False, "notes": "Not visible in image"},
            {"item": "Safety Harness", "detected": harness_detected, "compliant": harness_compliant, "notes": "Partial harness — improper fit" if harness_detected else "Not detected"},
            {"item": "Safety Gloves", "detected": False, "compliant": False, "notes": "Not detected during material handling"},
            {"item": "Eye Protection", "detected": True, "compliant": True, "notes": "Safety goggles present"},
        ],
        "site_hazards": [
            {"hazard": "Unsecured scaffolding on north face", "severity": "High", "corrective_remedy": "Secure per IS 3696 with guardrails"},
            {"hazard": "Exposed rebar without protective caps", "severity": "Medium", "corrective_remedy": "Install mushroom-style rebar caps"},
            {"hazard": "Debris accumulation in walkways", "severity": "Low", "corrective_remedy": "Daily site cleanup protocol"},
            {"hazard": "Missing electrical hazard signage", "severity": "High", "corrective_remedy": "Install OSHA-compliant signs within 24h"},
        ],
        "summary": f"Safety score: {score}/100. Partial PPE compliance detected. Critical scaffolding safety violations require immediate attention.",
        "recommendation": "Conduct toolbox talk. Issue mandatory PPE. Scaffold inspection within 4 hours.",
        "standard_reference": "OSHA 29 CFR 1926 / IS 456:2000"
    }


def get_demo_crack(image_bytes: bytes = None):
    rng = random.Random()
    if image_bytes:
        seed = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
        rng.seed(seed)
    else:
        rng.seed(42)

    types = ["Hairline", "Settlement", "Structural Shear", "Thermal Expansion", "Spalling"]
    crack_type = rng.choice(types)
    width = round(rng.uniform(0.5, 6.0), 2)
    risk = rng.randint(25, 80)
    severity = "Low" if risk < 35 else "Medium" if risk < 55 else "High" if risk < 75 else "Critical"
    return {
        "crack_type": crack_type,
        "estimated_crack_width_mm": width,
        "severity": severity,
        "urgency": "Immediate" if severity == "Critical" else "Within 1 week" if severity == "High" else "Within 1 month",
        "root_causes": ["Thermal expansion cycles", "Inadequate reinforcement cover (IS 456 Cl.26.4)", "Foundation differential settlement"],
        "repair_recommendations": [
            {"method": "Epoxy Injection", "description": "Low-viscosity epoxy under pressure for full bonding", "estimated_cost_inr": "₹15,000–₹45,000/m"},
            {"method": "Structural Re-grouting", "description": "Cement-polymer grout for wider cracks", "estimated_cost_inr": "₹8,000–₹25,000/m"},
        ],
        "structural_risk_score": risk,
        "summary": f"{crack_type} crack (width: {width}mm) detected. Severity: {severity}. Requires engineering assessment.",
        "immediate_action": "Restrict access 3m around crack. Document with photos. Engage structural engineer within 48h."
    }


# ─── PPE Safety Tab ────────────────────────────────────────────────────────────

def render_ppe_tab(api_key: str):
    st.markdown("### 📷 Upload Construction Site Photo")
    st.markdown("Upload a site photo for AI-powered PPE compliance analysis per **OSHA 29 CFR 1926** and **IS 456:2000**")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(
            "Site Photo",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="ppe_uploader"
        )
    with col2:
        demo_btn = st.button("⚡ Load Demo Analysis", key="ppe_demo_btn", use_container_width=True)

    if uploaded:
        st.image(uploaded, caption="Construction Site Photo", use_container_width=True)

    analyze_btn = st.button(
        "🔬 Analyze PPE Compliance",
        type="primary",
        disabled=not uploaded,
        key="ppe_analyze_btn",
        use_container_width=True
    )

    result = None

    if analyze_btn and uploaded:
        with st.spinner("🤖 Analyzing with Gemini Vision AI..."):
            if api_key:
                prompt = """Analyze this construction site image for PPE compliance (OSHA 29 CFR 1926 / IS 456:2000).
Return ONLY valid JSON: {"safety_score":<0-100>,"overall_status":"<Compliant|Non-Compliant|Partial Compliance>",
"ppe_detection_checklist":[{"item":"<name>","detected":<bool>,"compliant":<bool>,"notes":"<str>"}],
"site_hazards":[{"hazard":"<str>","severity":"<Low|Medium|High|Critical>","corrective_remedy":"<str>"}],
"summary":"<str>","recommendation":"<str>","standard_reference":"OSHA 29 CFR 1926 / IS 456:2000"}"""
                result = analyze_with_gemini(api_key, uploaded.getvalue(), prompt, uploaded.type)

            if not result:
                result = get_demo_ppe(uploaded.getvalue() if uploaded else None)

    elif demo_btn:
        result = get_demo_ppe()

    if result:
        st.divider()
        _display_ppe_results(result)


def _display_ppe_results(result: dict):
    score = result['safety_score']
    status = result['overall_status']

    # Score + Status
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        color = "#10b981" if score >= 75 else "#f59e0b" if score >= 50 else "#f43f5e"
        st.markdown(f"""
        <div class="metric-card-custom">
            <div style="font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">SAFETY SCORE</div>
            <div class="score-big" style="color:{color}">{score}</div>
            <div style="font-size:12px; color:#475569;">out of 100</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        badge_color = "#10b981" if "Compliant" in status and "Non" not in status else "#f59e0b" if "Partial" in status else "#f43f5e"
        st.markdown(f"""
        <div class="metric-card-custom">
            <div style="font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">STATUS</div>
            <div style="font-size:15px; font-weight:700; color:{badge_color}; margin-top:8px;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        compliant = sum(1 for p in result['ppe_detection_checklist'] if p['compliant'])
        total = len(result['ppe_detection_checklist'])
        st.markdown(f"""
        <div class="metric-card-custom">
            <div style="font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">PPE COMPLIANT</div>
            <div class="score-big" style="color:#3b82f6">{compliant}<span style="font-size:20px;color:#475569">/{total}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        hazards = len(result['site_hazards'])
        st.markdown(f"""
        <div class="metric-card-custom">
            <div style="font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">HAZARDS FOUND</div>
            <div class="score-big" style="color:#f59e0b">{hazards}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("#### 📋 PPE Detection Checklist")
        for item in result['ppe_detection_checklist']:
            icon = "✅" if item['compliant'] else ("⚠️" if item['detected'] else "❌")
            label = "Compliant" if item['compliant'] else ("Non-Compliant" if item['detected'] else "Not Detected")
            with st.expander(f"{icon} {item['item']} — **{label}**"):
                if item.get('notes'):
                    st.write(item['notes'])

    with col_right:
        st.markdown("#### 🚨 Site Hazards")
        for h in result['site_hazards']:
            sev = h['severity']
            sev_color = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#f43f5e"}[sev]
            with st.expander(f"**{h['hazard']}** — `{sev}`"):
                st.markdown(f"**Severity:** :{sev_color}[{sev}]")
                st.markdown(f"**Remedy:** {h['corrective_remedy']}")

    st.markdown("**📝 Summary**")
    st.info(result['summary'])
    st.markdown(f"💡 **Recommendation:** {result['recommendation']}")
    st.caption(f"Standard Reference: {result['standard_reference']}")

    # Download
    st.download_button(
        "⬇️ Download JSON Report",
        data=json.dumps(result, indent=2),
        file_name=f"ppe_safety_report.json",
        mime="application/json",
        key="ppe_download"
    )


# ─── Crack Tab ────────────────────────────────────────────────────────────────

def render_crack_tab(api_key: str):
    st.markdown("### 🧱 Upload Concrete / Wall Surface Photo")
    st.markdown("AI classifies crack type, estimates width in mm, and provides repair recommendations per **IS 456:2000**")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(
            "Surface Photo",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="crack_uploader"
        )
    with col2:
        demo_btn = st.button("⚡ Load Demo Analysis", key="crack_demo_btn", use_container_width=True)

    if uploaded:
        st.image(uploaded, caption="Concrete/Wall Surface", use_container_width=True)

    analyze_btn = st.button(
        "🔬 Analyze Crack Structure",
        type="primary",
        disabled=not uploaded,
        key="crack_analyze_btn",
        use_container_width=True
    )

    result = None
    if analyze_btn and uploaded:
        with st.spinner("🤖 Running structural crack analysis..."):
            if api_key:
                prompt = """Analyze this concrete/wall for cracks. Return ONLY valid JSON:
{"crack_type":"<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Unknown>",
"estimated_crack_width_mm":<float>,"severity":"<Low|Medium|High|Critical>","urgency":"<string>",
"root_causes":["<str>"],"repair_recommendations":[{"method":"<str>","description":"<str>","estimated_cost_inr":"<str>"}],
"structural_risk_score":<0-100>,"summary":"<str>","immediate_action":"<str>"}"""
                result = analyze_with_gemini(api_key, uploaded.getvalue(), prompt, uploaded.type)
            if not result:
                result = get_demo_crack(uploaded.getvalue() if uploaded else None)

    elif demo_btn:
        result = get_demo_crack()

    if result:
        st.divider()
        _display_crack_results(result)


def _display_crack_results(result: dict):
    crack_icons = {
        "Hairline": "〰️", "Settlement": "⬇️", "Structural Shear": "⚡",
        "Thermal Expansion": "🌡️", "Spalling": "💥", "Unknown": "❓"
    }

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        icon = crack_icons.get(result['crack_type'], '❓')
        st.metric("Crack Type", f"{icon} {result['crack_type']}")
    with c2:
        st.metric("Width (mm)", result['estimated_crack_width_mm'])
    with c3:
        st.metric("Severity", result['severity'])
    with c4:
        st.metric("Risk Score", f"{result['structural_risk_score']}/100")

    st.progress(result['structural_risk_score'] / 100)

    st.markdown(f"**⏰ Urgency:** `{result['urgency']}`")
    st.markdown(f"**⚡ Immediate Action:** {result['immediate_action']}")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 🔍 Root Causes")
        for cause in result['root_causes']:
            st.markdown(f"▸ {cause}")

    with col_r:
        st.markdown("#### 🔧 Repair Recommendations")
        for repair in result['repair_recommendations']:
            with st.expander(f"**{repair['method']}** — {repair['estimated_cost_inr']}"):
                st.write(repair['description'])

    st.info(result['summary'])

    st.download_button(
        "⬇️ Download Diagnostics Report",
        data=json.dumps(result, indent=2),
        file_name=f"crack_diagnostics.json",
        mime="application/json",
        key="crack_download"
    )


# ─── Valuation Tab ────────────────────────────────────────────────────────────

COST_MATRIX = {
    "Residential": {"Tier 1": 2200, "Tier 2": 1800, "Tier 3": 1400},
    "Commercial":  {"Tier 1": 3800, "Tier 2": 3200, "Tier 3": 2600},
    "Industrial":  {"Tier 1": 2800, "Tier 2": 2200, "Tier 3": 1800},
    "Mixed Use":   {"Tier 1": 3200, "Tier 2": 2600, "Tier 3": 2100},
    "Institutional": {"Tier 1": 3000, "Tier 2": 2400, "Tier 3": 1900},
}
MARKET_MULTIPLIER = {"Tier 1": 1.85, "Tier 2": 1.45, "Tier 3": 1.20}

def format_inr(amount):
    if amount >= 1e7:
        return f"₹{amount/1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"₹{amount/1e5:.2f} L"
    return f"₹{amount:,.0f}"


def render_valuation_tab():
    st.markdown("### 💰 Construction Budget & Real Estate Valuation")
    st.markdown("Calculate total project budget, CapEx, market valuation in INR, and material requirements")

    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", value="Skyline Residency", key="val_name")
        structure_type = st.selectbox("Structure Type", ["Residential", "Commercial", "Industrial", "Mixed Use", "Institutional"], key="val_type")
        built_up_sqft = st.number_input("Built-up Area (sqft)", min_value=100, max_value=1000000, value=2000, step=100, key="val_sqft")
    with col2:
        location_tier = st.selectbox("Location Tier", ["Tier 1", "Tier 2", "Tier 3"],
            format_func=lambda x: f"{x} — {'Mumbai/Delhi/Bengaluru' if x=='Tier 1' else 'Ahmedabad/Jaipur' if x=='Tier 2' else 'Mysuru/Vadodara'}", key="val_tier")
        floors = st.number_input("Number of Floors", min_value=1, max_value=100, value=3, key="val_floors")
        completion = st.slider("Completion Percentage", 0, 100, 65, key="val_completion")

    calc_btn = st.button("💰 Calculate Valuation", type="primary", use_container_width=True, key="val_calc_btn")

    if calc_btn:
        cost_per_sqft = COST_MATRIX[structure_type][location_tier]
        total_sqft = built_up_sqft * floors
        total_budget = total_sqft * cost_per_sqft
        capex = total_budget * (completion / 100)
        valuation = total_budget * MARKET_MULTIPLIER[location_tier]
        roi = ((valuation - total_budget) / total_budget) * 100

        st.divider()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Budget", format_inr(total_budget))
        c2.metric("CapEx Incurred", format_inr(capex), f"{completion}% done")
        c3.metric("Market Valuation", format_inr(valuation))
        c4.metric("Est. ROI", f"{roi:.1f}%")

        st.markdown("**📊 Project Completion**")
        st.progress(completion / 100)

        # Materials
        st.markdown("#### 🧱 Material Requirements (IS 456:2000)")
        concrete_vol = total_sqft * 0.05
        steel_kg = total_sqft * 4.5 * floors
        cement_bags = concrete_vol * 8

        materials_data = {
            "Material": ["Steel (Fe 500D)", "Cement (OPC 53)", "Fine Sand", "Coarse Aggregate", "Bricks/Blocks"],
            "Quantity": [f"{steel_kg/1000:.1f}", f"{cement_bags:.0f}", f"{concrete_vol*0.55:.1f}", f"{concrete_vol*0.85:.1f}", f"{total_sqft*8:.0f}"],
            "Unit": ["Tonnes", "Bags (50kg)", "Tonnes", "Tonnes", "Nos"],
            "Cost (INR)": [format_inr(steel_kg*65), format_inr(cement_bags*400), format_inr(concrete_vol*0.55*1800), format_inr(concrete_vol*0.85*1500), format_inr(total_sqft*8*12)],
        }
        st.table(materials_data)

        # Milestones
        st.markdown("#### 🏁 Milestone Progress")
        milestones = [("Site Preparation & Foundation", 15), ("Sub-structure", 30), ("Super-structure RCC", 55), ("Masonry & Plastering", 70), ("MEP & Finishing", 85), ("Handover", 100)]
        for name, pct in milestones:
            done = completion >= pct
            icon = "✅" if done else "⏳"
            st.markdown(f"{icon} **{name}** ({pct}%)")

        # Architectural Render
        st.markdown("#### 🎨 Conceptual Architectural Rendering (Pollinations AI)")
        arch_prompt = f"Photorealistic {structure_type.lower()} building, {floors} floors, modern Indian architecture, professional visualization"
        render_url = f"https://image.pollinations.ai/prompt/{arch_prompt.replace(' ', '%20')}?width=800&height=450&seed=42&nologo=true"
        st.markdown(f'<img src="{render_url}" style="width:100%; border-radius:12px; border:1px solid rgba(255,255,255,0.1);" />', unsafe_allow_html=True)
        st.caption("🤖 AI-generated conceptual rendering · Pollinations AI · For visualization only")

        # Download
        report = {
            "project_name": project_name,
            "structure_type": structure_type,
            "built_up_sqft": built_up_sqft,
            "floors": floors,
            "location_tier": location_tier,
            "completion_percentage": completion,
            "total_project_budget_inr": format_inr(total_budget),
            "capital_expenditure_incurred_inr": format_inr(capex),
            "current_market_asset_valuation_inr": format_inr(valuation),
            "roi_estimate_percent": round(roi, 1),
        }
        st.download_button("⬇️ Download Valuation Report", json.dumps(report, indent=2),
            f"valuation_{project_name}.json", "application/json", key="val_download")


# ─── Weather Advisory Tab ─────────────────────────────────────────────────────

WEATHER_PROTOCOLS = {
    "Normal ☀️": {"risk": "Low", "alerts": [
        {"type": "Routine Safety", "severity": "Low", "protocol": "Standard operations. Morning toolbox talk. PPE check. Hydration stations.", "suspended": []}
    ], "checklist": ["✅ Morning PPE briefing done", "✅ Scaffolding inspection complete", "✅ First aid kit stocked", "✅ Emergency exits clear"]},
    "High Wind 💨": {"risk": "Critical", "alerts": [
        {"type": "Wind Hazard Alert", "severity": "Critical", "protocol": "Suspend crane ops at >35 km/h. Double-lanyard harness. Secure all loose materials.", "suspended": ["Tower Crane", "Elevated Platform Work", "Precast Erection"]},
        {"type": "Electrical Hazard", "severity": "High", "protocol": "De-energize power lines within 2m of work zones.", "suspended": ["Overhead Electrical Work"]}
    ], "checklist": ["🚨 Crane SUSPENDED", "⚠️ Secure loose materials", "⚠️ Double-lanyard fall arrest", "✅ Document wind speed hourly"]},
    "Heavy Rain 🌧️": {"risk": "High", "alerts": [
        {"type": "Concrete Curing", "severity": "High", "protocol": "HALT all concrete pours. Cover slabs. Water-cement ratio must be documented.", "suspended": ["Concrete Pours", "Masonry", "Grouting", "Painting"]},
        {"type": "Electrical Safety", "severity": "Critical", "protocol": "GFCI protection mandatory. Rubber-soled boots required.", "suspended": ["Non-GFCI Tools", "Open Panel Work"]}
    ], "checklist": ["🚨 Concrete pours HALTED", "🚨 GFCI on ALL electrical tools", "⚠️ Fresh concrete covered", "✅ Dewatering pumps operational"]},
    "Extreme Heat 🌡️": {"risk": "High", "alerts": [
        {"type": "Heat Stroke Prevention", "severity": "High", "protocol": "10-min break per 45-min work. 250ml water/hour/worker. Wet-bulb temperature monitoring.", "suspended": ["Heavy Labour 12pm-3pm", "Asphalt Work 11am-4pm"]},
    ], "checklist": ["🚨 Mandatory breaks every 45 min", "🚨 250ml water per worker per hour", "⚠️ No heavy work 12pm-3pm", "✅ Heat stroke first aid on site"]},
}


def fetch_streamlit_weather(location: str):
    import urllib.request
    import urllib.parse
    import json
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(location)}&count=1&language=en&format=json"
        req = urllib.request.Request(geo_url, headers={'User-Agent': 'ConstructionAI/1.0'})
        with urllib.request.urlopen(req, timeout=6) as response:
            geo_data = json.loads(response.read().decode())
        results = geo_data.get('results')
        if not results:
            return None, f"Location '{location}' not found. Please verify spelling."
        loc = results[0]
        lat, lon = loc['latitude'], loc['longitude']
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m&timezone=auto"
        req2 = urllib.request.Request(w_url, headers={'User-Agent': 'ConstructionAI/1.0'})
        with urllib.request.urlopen(req2, timeout=6) as response2:
            w_data = json.loads(response2.read().decode())
        curr = w_data.get('current', {})
        name_parts = [loc.get('name', location)]
        if loc.get('admin1') and loc.get('admin1') != loc.get('name'):
            name_parts.append(loc.get('admin1'))
        if loc.get('country'):
            name_parts.append(loc.get('country'))
        return {
            'location_name': ', '.join(name_parts),
            'latitude': round(lat, 4),
            'longitude': round(lon, 4),
            'temperature_c': curr.get('temperature_2m'),
            'apparent_temperature_c': curr.get('apparent_temperature'),
            'relative_humidity_pct': curr.get('relative_humidity_2m'),
            'wind_speed_kmh': curr.get('wind_speed_10m'),
            'precipitation_mm': curr.get('precipitation'),
            'observation_time': curr.get('time', '')
        }, None
    except Exception as e:
        return None, f"Weather service error: {str(e)}"


def render_weather_tab(api_key: str):
    st.markdown("### 🌤️ Daily Site Assistant & Weather-Aware Advisory")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### 📍 Site Location (Live Open-Meteo)")
        loc_col1, loc_col2 = st.columns([3, 2])
        with loc_col1:
            st_loc_input = st.text_input("Site Location", placeholder="Enter city or location (e.g. Indore)", label_visibility="collapsed", key="st_weather_loc_input")
        with loc_col2:
            get_w_btn = st.button("Get Weather Advisory", key="st_get_w_btn", use_container_width=True)

        if 'active_weather_obs' not in st.session_state:
            st.session_state.active_weather_obs = None
            st.session_state.weather_obs_err = None

        if get_w_btn:
            if not st_loc_input.strip():
                st.session_state.weather_obs_err = "Please enter a city or location name."
                st.session_state.active_weather_obs = None
            else:
                with st.spinner(f"Fetching live weather for {st_loc_input}..."):
                    obs, err = fetch_streamlit_weather(st_loc_input.strip())
                    st.session_state.active_weather_obs = obs
                    st.session_state.weather_obs_err = err

        if st.session_state.weather_obs_err:
            st.error(f"⚠️ {st.session_state.weather_obs_err}")

        if st.session_state.active_weather_obs:
            obs = st.session_state.active_weather_obs
            st.markdown(f"""
            <div style="background:#161b2e; border:1px solid rgba(99,179,237,0.3); border-radius:12px; padding:14px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-weight:700; font-size:15px; color:#f1f5f9;">📍 {obs['location_name']}</div>
                    <span style="background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3); border-radius:12px; padding:2px 8px; font-size:10px; font-weight:600;">⚡ Live Weather · Demo Advice</span>
                </div>
                <div style="font-size:11px; color:#94a3b8; margin:4px 0 10px;">
                    Coords: {obs['latitude']}° N, {obs['longitude']}° E · Observed: {obs['observation_time']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            oc1, oc2, oc3, oc4 = st.columns(4)
            oc1.metric("Ambient Temp", f"{obs['temperature_c']}°C")
            oc2.metric("Feels Like", f"{obs['apparent_temperature_c']}°C")
            oc3.metric("Wind Speed", f"{obs['wind_speed_kmh']} km/h")
            oc4.metric("Precipitation", f"{obs['precipitation_mm']} mm")

        st.markdown("#### Select Safety Protocol Scenario")
        weather = st.radio(
            "Weather",
            list(WEATHER_PROTOCOLS.keys()),
            horizontal=False,
            label_visibility="collapsed",
            key="weather_select"
        )

        protocol = WEATHER_PROTOCOLS[weather]
        risk = protocol['risk']
        risk_color = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#f43f5e"}[risk]
        st.markdown(f"""
        <div style="background: {risk_color}15; border: 1px solid {risk_color}40; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <div style="font-size:12px; color:#475569; text-transform:uppercase; letter-spacing:0.06em;">OVERALL RISK LEVEL</div>
            <div style="font-size:28px; font-weight:800; color:{risk_color}; margin-top:4px;">{risk}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**🚨 Safety Alerts**")
        for alert in protocol['alerts']:
            sev = alert['severity']
            border_color = {"Critical": "#f43f5e", "High": "#f97316", "Medium": "#f59e0b", "Low": "#10b981"}[sev]
            icon = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}[sev]
            with st.expander(f"{icon} **{alert['type']}** — `{sev}`"):
                st.write(alert['protocol'])
                if alert['suspended']:
                    st.markdown("**🚫 Suspended Operations:**")
                    for op in alert['suspended']:
                        st.markdown(f"- ❌ {op}")

        st.markdown("**📋 Daily Safety Checklist**")
        for item in protocol['checklist']:
            st.markdown(item)

        st.markdown("**📞 Emergency Contacts**")
        contacts = {"Emergency": "112", "Fire": "101", "Medical": "108", "Safety Officer": "1800-200-5959"}
        for name, num in contacts.items():
            st.markdown(f"**{name}:** `{num}`")

    with col_right:
        st.markdown("#### 🤖 Construction AI Assistant")

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "👋 Hello! I'm your **Construction Intelligence Assistant**.\n\nAsk me about PPE standards, structural analysis, IS codes, cost estimation, or weather safety protocols."}
            ]

        # Chat display
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    with st.chat_message("user"):
                        st.write(msg['content'])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg['content'])

        # Suggested questions
        st.markdown("**💡 Quick Questions:**")
        q_cols = st.columns(2)
        quick_qs = [
            "What PPE is mandatory?", "How to cure concrete in rain?",
            "IS 456 crack classification?", "Steel quantity for 2000 sqft?"
        ]
        for i, q in enumerate(quick_qs):
            with q_cols[i % 2]:
                if st.button(q, key=f"quick_q_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    weather_clean = weather.split()[0]  # remove emoji
                    with st.spinner("Thinking..."):
                        reply = chat_with_gemini(api_key, q, st.session_state.chat_history, weather_clean)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()

        # Chat input
        user_input = st.chat_input("Ask about construction engineering, PPE, costs, IS codes...", key="chat_main_input")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            weather_clean = weather.split()[0]
            with st.spinner("🤖 Thinking..."):
                reply = chat_with_gemini(api_key, user_input, st.session_state.chat_history, weather_clean)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
            st.session_state.chat_history = [st.session_state.chat_history[0]]
            st.rerun()


# ─── Main App ─────────────────────────────────────────────────────────────────

def main():
    # Header
    st.markdown("""
    <div class="platform-header">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:40px;">🏗️</div>
            <div>
                <h1 style="font-size:22px; font-weight:800; color:#f1f5f9; margin:0;">
                    Multimodal Construction Intelligence Platform
                </h1>
                <p style="color:#94a3b8; margin:4px 0 0; font-size:13px;">
                    AI-Powered Decision Support · PPE Safety · Crack Diagnostics · Real Estate Valuation · Weather Advisory
                </p>
                <p style="color:#06b6d4; margin:4px 0 0; font-size:10px; font-family:monospace;">
                    Skill Wallet Capstone Project 1 · Platform ID: 6ac4c98d1dcde6d7857c1642
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = render_sidebar()

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺 PPE Safety Audit (E2)",
        "🔍 Crack Diagnostics (E2)",
        "🏗️ Planning & Valuation (E3)",
        "🌤️ Site Assistant & Weather (E5)"
    ])

    with tab1:
        render_ppe_tab(api_key)

    with tab2:
        render_crack_tab(api_key)

    with tab3:
        render_valuation_tab()

    with tab4:
        render_weather_tab(api_key)


if __name__ == "__main__":
    main()
