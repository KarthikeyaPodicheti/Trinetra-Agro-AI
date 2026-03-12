"""
Trinetra Agro AI - Main Application
Vision Beyond the Fields 🔱
"""

import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

# ---- path setup ----
app_dir = Path(__file__).parent
project_root = app_dir.parent
sys.path.insert(0, str(app_dir))

from chatbot.core_bot import TrinetraBot
from utils.config import load_config
from utils.helpers import setup_logging
from utils.translator import translate as _t

# AI modules
from ai_modules.disease_detection import DiseaseDetector
from ai_modules.market_prediction import MarketPredictor
from ai_modules.crop_advisor import CropAdvisor
from ai_modules import risk_assessment, yield_prediction, irrigation_ai, profit_predictor

# Database
from database import (save_farmer, save_conversation, save_disease_detection,
                       save_market_query, save_crop_recommendation)

# ---- page config ----
st.set_page_config(
    page_title="Trinetra Agro AI",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- CSS ----
st.markdown("""
<style>
/* ===== GLOBAL ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Soften the main background */
section.main > div {max-width: 1100px; margin: auto;}

/* ===== HEADER ===== */
.hero {
    background: linear-gradient(135deg, #E8F5E9 0%, #ffffff 50%, #F1F8E9 100%);
    border-radius: 18px;
    padding: 2.2rem 1.5rem 1.4rem;
    margin-bottom: 1.8rem;
    text-align: center;
    border: 1px solid #C8E6C9;
    box-shadow: 0 2px 16px rgba(67,160,71,.08);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #2E7D32;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1.05rem;
    color: #66BB6A;
    margin-top: .35rem;
    font-weight: 500;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FAFFFE 0%, #E8F5E9 100%) !important;
    border-right: 1px solid #C8E6C9;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #2E7D32 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #C8E6C9;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label {
    color: #37474F !important;
    font-weight: 500;
}

/* ===== CARDS / CONTAINERS ===== */
.card {
    background: #ffffff;
    border: 1px solid #E0E0E0;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 8px rgba(0,0,0,.04);
    transition: box-shadow .2s ease;
}
.card:hover {box-shadow: 0 4px 20px rgba(67,160,71,.10);}

.card-green {
    background: linear-gradient(135deg, #ffffff 60%, #F1F8E9);
    border-left: 4px solid #66BB6A;
}

/* ===== METRICS ===== */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #E8F5E9;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 1px 6px rgba(67,160,71,.06);
}
div[data-testid="stMetric"] label {color: #558B2F !important; font-weight: 600;}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {color: #2E7D32 !important; font-weight: 700;}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #43A047, #66BB6A) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .55rem 1.6rem !important;
    font-weight: 600 !important;
    font-size: .92rem !important;
    letter-spacing: .3px;
    box-shadow: 0 2px 8px rgba(67,160,71,.18);
    transition: all .2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #388E3C, #43A047) !important;
    box-shadow: 0 4px 14px rgba(56,142,60,.25);
    transform: translateY(-1px);
}
.stButton > button:active {transform: translateY(0);}

/* ===== CHAT ===== */
div[data-testid="stChatMessage"] {
    border-radius: 14px;
    border: 1px solid #E8F5E9;
    box-shadow: 0 1px 4px rgba(0,0,0,.03);
}

/* ===== EXPANDERS ===== */
details {
    border: 1px solid #E0E0E0 !important;
    border-radius: 12px !important;
    background: #FAFFFE !important;
}
details summary {font-weight: 600; color: #2E7D32;}

/* ===== TABS / FILE UPLOADER ===== */
.stFileUploader {
    border: 2px dashed #A5D6A7 !important;
    border-radius: 14px !important;
    background: #FAFFFE !important;
}
.stFileUploader:hover {border-color: #66BB6A !important;}

/* ===== SELECTBOX & INPUTS ===== */
div[data-testid="stSelectbox"] > div > div,
.stNumberInput input,
.stTextInput input {
    border-radius: 10px !important;
    border: 1px solid #C8E6C9 !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within,
.stNumberInput input:focus,
.stTextInput input:focus {
    border-color: #43A047 !important;
    box-shadow: 0 0 0 2px rgba(67,160,71,.15) !important;
}

/* ===== SLIDER ===== */
.stSlider [data-testid="stThumbValue"] {color: #2E7D32;}

/* ===== ALERTS ===== */
.stAlert {border-radius: 12px !important;}

/* ===== DATAFRAME ===== */
.stDataFrame {border-radius: 12px; overflow: hidden;}

/* ===== STAT WIDGET (right column) ===== */
.stat-box {
    background: #ffffff;
    border: 1px solid #E8F5E9;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: .8rem;
    box-shadow: 0 1px 6px rgba(67,160,71,.06);
}
.stat-box h4 {color: #2E7D32; margin-top:0;}

/* ===== PAGE SECTION ===== */
.page-section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #2E7D32;
    margin-bottom: .6rem;
    padding-bottom: .4rem;
    border-bottom: 2px solid #C8E6C9;
}
</style>
""", unsafe_allow_html=True)


# ===========================================================================
#  Singleton helpers cached in session_state
# ===========================================================================
def _bot() -> TrinetraBot:
    if "bot" not in st.session_state:
        st.session_state.bot = TrinetraBot(
            language=st.session_state.get("language", "English"),
            farmer_profile=_profile(),
        )
    return st.session_state.bot


def _disease() -> DiseaseDetector:
    if "disease_det" not in st.session_state:
        st.session_state.disease_det = DiseaseDetector()
    return st.session_state.disease_det


def _market() -> MarketPredictor:
    if "market_pred" not in st.session_state:
        st.session_state.market_pred = MarketPredictor()
    return st.session_state.market_pred


def _advisor() -> CropAdvisor:
    if "crop_adv" not in st.session_state:
        st.session_state.crop_adv = CropAdvisor()
    return st.session_state.crop_adv


def _profile() -> dict:
    return {
        "land_size": st.session_state.get("land_size", 5.0),
        "soil_type": st.session_state.get("soil_type", "Black Cotton"),
        "budget": st.session_state.get("budget", 50000),
    }


# ===========================================================================
#  MAIN
# ===========================================================================
def main():
    setup_logging()
    load_config()

    # ---- hero header ----
    st.markdown("""
    <div class="hero">
        <p class="hero-title">🔱 Trinetra Agro AI</p>
        <p class="hero-sub">Vision Beyond the Fields — Intelligent Farming at Your Fingertips</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- sidebar ----
    with st.sidebar:
        st.markdown("### 🌿 Navigation")
        feature = st.selectbox("Choose AI Feature:", key="feature_select", options=[
            "💬 Smart Chat",
            "🔬 Disease Detection",
            "📈 Market Prediction",
            "👨‍🌾 Farming Advisor",
            "⚠️ Risk Assessment",
            "🌾 Yield Prediction",
            "🗣️ Voice AI",
            "💧 Irrigation AI",
            "💰 Profit Predictor",
        ])
        st.markdown("---")

        language = st.selectbox("🌍 Language / భాష:", ["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"], key="language")
        st.markdown("---")

        st.markdown("### 👨‍🌾 Your Farm")
        st.number_input("Land Size (acres)", min_value=0.1, value=5.0, key="land_size")
        st.selectbox("Soil Type", ["Black Cotton", "Red Soil", "Alluvial", "Sandy", "Clay", "Loamy"], key="soil_type")
        st.number_input("Budget (₹)", min_value=1000, value=50000, step=5000, key="budget")

        st.markdown("---")
        # Inline API status in sidebar
        status = _bot().get_api_status()
        if status["openrouter_connected"]:
            st.success("🧠 AI-Powered Mode", icon="✅")
        else:
            st.info("🤖 Rule-Based Mode", icon="ℹ️")
            with st.expander("Enable AI Chat"):
                st.markdown("1. Get a key at [openrouter.ai](https://openrouter.ai/)\n"
                            "2. Add `OPENROUTER_API_KEY=...` to `.env`\n"
                            "3. Restart the app")

    # Keep bot profile in sync
    _bot().update_farmer_profile(_profile())
    _bot().language = language

    # ---- main area (full‑width, no side column) ----
    if feature == "💬 Smart Chat":
        page_chat()
    elif feature == "🔬 Disease Detection":
        page_disease()
    elif feature == "📈 Market Prediction":
        page_market()
    elif feature == "👨‍🌾 Farming Advisor":
        page_advisor()
    elif feature == "⚠️ Risk Assessment":
        page_risk()
    elif feature == "🌾 Yield Prediction":
        page_yield()
    elif feature == "🗣️ Voice AI":
        page_voice()
    elif feature == "💧 Irrigation AI":
        page_irrigation()
    elif feature == "💰 Profit Predictor":
        page_profit()


# ===========================================================================
#  PAGE: Smart Chat
# ===========================================================================
def page_chat():
    st.markdown('<p class="page-section-title">💬 ' + _t('Intelligent Farming Chat') + '</p>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": _t("🙏 Namaste! I'm **Trinetra**, your AI farming advisor. Ask me anything about crops, diseases, markets, irrigation, or farming!")}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(_t("Ask your farming question…")):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(_t("Thinking…")):
                reply = _bot().get_response(prompt)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        save_conversation(0, "user", prompt)
        save_conversation(0, "bot", reply)


# ===========================================================================
#  PAGE: Disease Detection
# ===========================================================================
def page_disease():
    st.markdown('<p class="page-section-title">🔬 ' + _t('AI-Powered Crop Disease Detection') + '</p>', unsafe_allow_html=True)

    col_input, col_spacer = st.columns([2, 1])
    with col_input:
        crop_type = st.selectbox("Crop type:", list(DiseaseDetector.DISEASE_CLASSES.keys()), index=0, key="disease_crop")
    uploaded = st.file_uploader(_t("Upload leaf / crop image"), type=["jpg", "jpeg", "png"])

    if uploaded is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded, caption="Uploaded Image", use_container_width=True)

        with col2:
            if st.button(_t("🔍 Analyse Disease")):
                with st.spinner(_t("AI is analysing your crop…")):
                    result = _disease().detect_disease_bytes(uploaded.getvalue(), crop_type)

                if result.get("success"):
                    disease = result["disease"]
                    conf = result["confidence"]
                    if disease == "Healthy":
                        st.success(_t(f"✅ **{disease}** — Confidence: {conf*100:.1f}%"))
                    else:
                        st.error(_t(f"⚠️ **Disease Detected: {disease}**"))
                        mc1, mc2 = st.columns(2)
                        mc1.metric(_t("Confidence"), f"{conf*100:.1f}%")
                        mc2.metric(_t("Severity"), result['severity'])

                    st.markdown(_t("### 💡 Treatment"))
                    st.markdown(_t(result["recommendation"]))

                    st.markdown(_t("### 🛡️ Prevention Tips"))
                    for tip in result["prevention_tips"]:
                        st.markdown(f"• {_t(tip)}")

                    with st.expander("🔎 " + _t("Detailed Analysis")):
                        st.json(result.get("analysis", {}))

                    save_disease_detection(0, crop_type, disease, conf, result["severity"])
                else:
                    st.error(_t(result.get("error", "Analysis failed.")))


# ===========================================================================
#  PAGE: Market Prediction
# ===========================================================================
def page_market():
    st.markdown('<p class="page-section-title">📈 ' + _t('Smart Market Price Prediction') + '</p>', unsafe_allow_html=True)
    import plotly.graph_objects as go

    crops = list(MarketPredictor.BASE_PRICES.keys())
    c1, c2, c3 = st.columns(3)
    with c1:
        crop = st.selectbox("Select Crop:", [c.title() for c in crops], key="market_crop")
    with c2:
        days = st.slider("Prediction Days:", 7, 30, 14)
    with c3:
        location = st.selectbox("Nearest Market:", ["Hyderabad", "Mumbai", "Delhi", "Chennai", "Bangalore"], key="market_location")

    if st.button(_t("📊 Predict Prices")):
        with st.spinner(_t("Analysing market trends…")):
            res = _market().predict_prices(crop, days, location)

        if res.get("success"):
            preds = res["predictions"]

            # Metrics row
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric(_t("Current Price"), f"₹{res['current_price']:,.0f}")
            avg_pred = sum(preds["prices"]) / len(preds["prices"])
            delta = avg_pred - res["current_price"]
            mc2.metric(_t(f"Avg Predicted ({days}d)"), f"₹{avg_pred:,.0f}", f"{delta:+,.0f}")
            mc3.metric(_t("Trend"), _t(res["trend"].title()))

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=preds["dates"], y=preds["prices"],
                                     mode="lines+markers", name="Ensemble"))
            fig.add_trace(go.Scatter(x=preds["dates"], y=preds["moving_avg"],
                                     mode="lines", name="Moving Avg", line=dict(dash="dash")))
            fig.add_trace(go.Scatter(x=preds["dates"], y=preds["trend"],
                                     mode="lines", name="Trend", line=dict(dash="dot")))
            fig.update_layout(
                title=f"{crop.title()} Price Forecast ({days} days)",
                xaxis_title="Date", yaxis_title="₹ per Quintal",
                template="plotly_white", height=380,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#1B3A1D"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Recommendation
            rec = res["recommendation"]
            urgency_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            st.markdown(_t(f"### Recommendation: **{rec['action']}** {urgency_colors.get(rec['urgency'], '')}"))
            st.markdown(_t(f"{rec['message']} — _{rec['reason']}_"))

            st.markdown(_t("### 💡 Market Tips"))
            for tip in res.get("market_tips", []):
                st.markdown(f"• {_t(tip)}")

            save_market_query(0, crop, res["current_price"], res["trend"], rec["action"])
        else:
            st.error(res.get("error"))

    # Overview
    with st.expander("📋 Market Overview — All Crops"):
        overview = _market().get_market_overview()
        import pandas as pd
        rows = []
        for c, d in overview.items():
            rows.append({
                "Crop": c.title(),
                "Current (₹)": f"{d['current_price']:,.0f}",
                "Week Δ%": f"{d['week_change']:+.1f}%",
                "Trend": d["trend"].title(),
                "Volatility": d["volatility"].title(),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ===========================================================================
#  PAGE: Farming Advisor
# ===========================================================================
def page_advisor():
    st.markdown('<p class="page-section-title">👨‍🌾 ' + _t('Personalised Farming Advisor') + '</p>', unsafe_allow_html=True)

    prof = _profile()
    season = st.selectbox("Current Season:", ["Kharif", "Rabi", "Zaid"], key="advisor_season")

    if st.button(_t("🌱 Get Crop Recommendations")):
        with st.spinner(_t("Generating recommendations…")):
            advisor = _advisor()
            profile_data = {
                "soil_type": prof["soil_type"].lower().replace(" ", "_"),
                "land_size": prof["land_size"],
                "budget": prof["budget"],
                "irrigation_available": True,
                "location": "",
            }
            recs = advisor.get_recommendations(profile=profile_data)

        if recs.get("success"):
            st.markdown(_t("### 🌱 Primary Recommendations"))
            for i, crop in enumerate(recs.get("primary_recommendations", [])[:3], 1):
                name = crop.get("name", crop.get("crop_id", ""))
                with st.expander(f"**{i}. {_t(name)}**"):
                    st.markdown(_t(f"• **Season:** {crop.get('season', 'N/A')}"))
                    st.markdown(_t(f"• **Duration:** {crop.get('duration', 'N/A')}"))
                    st.markdown(_t(f"• **Water:** {crop.get('water_requirement', 'N/A')}"))
                    st.markdown(_t(f"• **Expected Yield:** {crop.get('expected_yield', 'N/A')}"))
                    st.markdown(_t(f"• **Profit Range:** ₹{crop.get('profit_range', 'N/A')}"))
                    if crop.get("diseases"):
                        st.markdown(_t(f"• **Common Diseases:** {', '.join(crop['diseases'])}"))

            st.markdown(_t("### 📅 Seasonal Plan"))
            plan = recs.get("seasonal_plan", {})
            for key in sorted(plan.get("months", {}).keys()):
                month = plan["months"][key]
                st.markdown(f"**{_t(month['name'])}**")
                for act in month.get("activities", []):
                    st.markdown(f"  - {_t(act)}")

            risk = recs.get("risk_assessment", {})
            if risk:
                st.markdown(_t(f"### ⚠️ Risk Level: **{risk.get('risk_level', 'N/A')}** (score {risk.get('risk_score', '')})"))

            ret = recs.get("expected_returns", {})
            if ret:
                st.markdown(_t("### 💰 Expected Returns"))
                rc, rm, ro = st.columns(3)
                rc.metric(_t("Conservative"), f"₹{ret.get('conservative', 0):,.0f}")
                rm.metric(_t("Moderate"), f"₹{ret.get('moderate', 0):,.0f}")
                ro.metric(_t("Optimistic"), f"₹{ret.get('optimistic', 0):,.0f}")

            crop_names = ", ".join(c.get("name", "") for c in recs.get("primary_recommendations", [])[:3])
            save_crop_recommendation(0, crop_names, risk.get("risk_level", ""))
        else:
            st.error(_t(recs.get("error", "Could not generate recommendations")))


# ===========================================================================
#  PAGE: Risk Assessment
# ===========================================================================
def page_risk():
    st.markdown('<p class="page-section-title">⚠️ ' + _t('Farm Risk Assessment') + '</p>', unsafe_allow_html=True)

    crops = ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Onion", "Maize", "Sugarcane", "Soybean", "Groundnut"]
    c1, c2 = st.columns([2, 1])
    with c1:
        crop = st.selectbox("Select Crop:", crops, key="risk_crop")
    with c2:
        irrig = st.checkbox("Irrigation available?", value=True, key="risk_irrig")

    if st.button(_t("🔍 Assess Risk")):
        prof = _profile()
        res = risk_assessment.assess_risk(
            crop, soil_type=prof["soil_type"], land_size=prof["land_size"],
            budget=prof["budget"], irrigation=irrig,
        )
        level = res["risk_level"]
        colour = {"Low": "success", "Medium": "warning", "High": "error"}
        getattr(st, colour.get(level, "info"))(_t(f"**Risk Level: {level}** — Score {res['risk_score']}/100"))

        bd = res["breakdown"]
        c1, c2, c3 = st.columns(3)
        c1.metric(_t("Disease Risk"), f"{bd['disease_risk']}/30")
        c2.metric(_t("Market Risk"), f"{bd['market_risk']}/25")
        c3.metric(_t("Water Risk"), f"{bd['water_risk']}/25")

        if res["factors"]:
            st.markdown(_t("### Risk Factors"))
            for f in res["factors"]:
                st.markdown(f"• {_t(f)}")

        if res["mitigations"]:
            st.markdown(_t("### 🛡️ Mitigations"))
            for m in res["mitigations"]:
                st.markdown(f"• {_t(m)}")


# ===========================================================================
#  PAGE: Yield Prediction
# ===========================================================================
def page_yield():
    st.markdown('<p class="page-section-title">🌾 ' + _t('Crop Yield Prediction') + '</p>', unsafe_allow_html=True)

    crops = list(yield_prediction._YIELD_DATA.keys())
    c1, c2 = st.columns([2, 1])
    with c1:
        crop = st.selectbox("Crop:", [c.title() for c in crops], key="yield_crop")
    with c2:
        irrig = st.checkbox("Irrigation available?", value=True, key="yield_irrig")

    if st.button(_t("📊 Predict Yield")):
        prof = _profile()
        res = yield_prediction.predict_yield(crop, prof["land_size"], prof["soil_type"], irrig)
        if res.get("success"):
            e = res["estimates"]
            c1, c2, c3 = st.columns(3)
            c1.metric(_t("Conservative"), f"{e['conservative']:.1f} {res['unit']}")
            c2.metric(_t("Moderate"), f"{e['moderate']:.1f} {res['unit']}")
            c3.metric(_t("Optimistic"), f"{e['optimistic']:.1f} {res['unit']}")

            m = res["multipliers"]
            st.markdown(_t(f"**Soil factor:** {m['soil']:.2f} | "
                        f"**Season factor:** {m['season']:.2f} | "
                        f"**Irrigation factor:** {m['irrigation']:.2f}"))
            st.info(_t(f"Season: {res['current_season']} — {res['notes'][0]}"))
        else:
            st.error(_t(res.get("error")))


# ===========================================================================
#  PAGE: Irrigation AI
# ===========================================================================
def page_irrigation():
    st.markdown('<p class="page-section-title">💧 ' + _t('Smart Irrigation Planner') + '</p>', unsafe_allow_html=True)

    crops = list(irrigation_ai._WATER_DATA.keys())
    c1, c2 = st.columns(2)
    with c1:
        crop = st.selectbox("Crop:", [c.title() for c in crops], key="irrig_crop")
    with c2:
        stage = st.selectbox("Growth Stage:", list(irrigation_ai._STAGE_MULT.keys()), key="irrig_stage")

    if st.button(_t("💧 Get Irrigation Plan")):
        prof = _profile()
        res = irrigation_ai.irrigation_plan(crop, prof["land_size"], stage)
        if res.get("success"):
            w = res["water_needs"]
            c1, c2, c3 = st.columns(3)
            c1.metric(_t("Daily"), f"{w['daily_litres']:,.0f} L")
            c2.metric(_t("Weekly"), f"{w['weekly_litres']:,.0f} L")
            c3.metric(_t("Season Total"), f"{w['season_total_cm']} cm")

            st.markdown(_t(f"**Method:** {res['recommended_method']}"))

            s = res["schedule"]
            st.markdown(_t("### 📅 Schedule"))
            st.markdown(_t(f"• **Frequency:** {s['frequency']}"))
            st.markdown(_t(f"• **Duration:** {s['duration']}"))
            st.markdown(_t(f"• **Best time:** {s['best_time']}"))
            st.markdown(f"• _{_t(s['note'])}_")

            st.markdown(_t("### 💡 Water-Saving Tips"))
            for t in res["tips"]:
                st.markdown(f"• {_t(t)}")
        else:
            st.error(_t(res.get("error")))


# ===========================================================================
#  PAGE: Profit Predictor
# ===========================================================================
def page_profit():
    st.markdown('<p class="page-section-title">💰 ' + _t('Profit Predictor') + '</p>', unsafe_allow_html=True)

    crops = list(profit_predictor._INPUT_COSTS.keys())
    c1, c2 = st.columns([2, 1])
    with c1:
        crop = st.selectbox("Crop:", [c.title() for c in crops], key="profit_crop")
    with c2:
        irrig = st.checkbox("Irrigation available?", value=True, key="profit_irrig")

    if st.button(_t("💰 Predict Profit")):
        prof = _profile()
        res = profit_predictor.predict_profit(
            crop, prof["land_size"], soil_type=prof["soil_type"], irrigation=irrig,
        )
        if res.get("success"):
            # Costs
            st.markdown(_t("### Input Costs"))
            ic = res["input_costs"]
            st.markdown(_t(f"**Total:** ₹{ic['total']:,.0f} ({prof['land_size']} acres × ₹{ic['per_acre']:,.0f}/acre)"))
            bd = ic["breakdown"]
            cols = st.columns(len(bd))
            for col, (k, v) in zip(cols, bd.items()):
                col.metric(_t(k.title()), f"₹{v:,.0f}")

            # Revenue & Profit
            st.markdown(_t("### 📊 Projections"))
            rc, rm, ro = st.columns(3)
            p = res["profit"]
            roi = res["roi_percent"]
            rc.metric(_t("Conservative"), f"₹{p['conservative']:,.0f}", f"ROI {roi['conservative']}%")
            rm.metric(_t("Moderate"), f"₹{p['moderate']:,.0f}", f"ROI {roi['moderate']}%")
            ro.metric(_t("Optimistic"), f"₹{p['optimistic']:,.0f}", f"ROI {roi['optimistic']}%")

            # Chart
            import plotly.graph_objects as go
            scenarios = ["Conservative", "Moderate", "Optimistic"]
            rev = res["revenue"]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Revenue", x=scenarios,
                                 y=[rev["conservative"], rev["moderate"], rev["optimistic"]],
                                 marker_color="#4CAF50"))
            fig.add_trace(go.Bar(name="Cost", x=scenarios,
                                 y=[ic["total"]] * 3, marker_color="#F44336"))
            fig.update_layout(barmode="group", title="Revenue vs Cost", template="plotly_white", height=350,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(family="Inter", color="#1B3A1D"))
            st.plotly_chart(fig, use_container_width=True)

            # Verdict
            if p["moderate"] > 0:
                st.success(_t(f"✅ {res['recommendation']}"))
            else:
                st.error(_t(f"⚠️ {res['recommendation']}"))
        else:
            st.error(_t(res.get("error")))


# ===========================================================================
#  PAGE: Voice AI
# ===========================================================================
def page_voice():
    st.markdown('<p class="page-section-title">🗣️ ' + _t('Voice AI — Text-to-Speech') + '</p>', unsafe_allow_html=True)
    st.markdown(_t("Type a farming question below and hear the answer spoken aloud."))

    try:
        from gtts import gTTS
        tts_ok = True
    except ImportError:
        tts_ok = False

    lang_map = {
        "English": "en", "Telugu (తెలుగు)": "te", "Hindi (हिंदी)": "hi",
    }
    tts_lang = lang_map.get(st.session_state.get("language", "English"), "en")

    question = st.text_input("Your question:", placeholder="e.g. What crops should I plant this Rabi season?")

    if st.button(_t("🔊 Get Spoken Answer")) and question:
        with st.spinner(_t("Generating answer…")):
            reply = _bot().get_response(question)
        st.markdown(reply)

        if tts_ok:
            tts = gTTS(text=reply, lang=tts_lang, slow=False)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp.name)
            st.audio(tmp.name, format="audio/mp3")
        else:
            st.warning(_t("gTTS not installed — install with `pip install gTTS` for audio playback."))


# ===========================================================================
if __name__ == "__main__":
    main()