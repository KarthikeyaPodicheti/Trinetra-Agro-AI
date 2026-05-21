"""Market Intelligence page."""

import streamlit as st
import plotly.graph_objects as go
from frontend.api_client import api_post


def show():
    st.markdown("### 📈 Market Price Intelligence")
    st.markdown("Forecast future crop prices and get AI-driven buy/sell recommendations.")

    with st.form("market_form"):
        crops = ["rice", "wheat", "cotton", "tomato", "potato", "onion", "maize", "sugarcane", "soybean", "groundnut"]
        c1, c2 = st.columns(2)
        crop = c1.selectbox("Select Crop", [c.title() for c in crops])
        days = c2.slider("Forecast Horizon (Days)", 7, 30, 14)
        submitted = st.form_submit_button("📊 Predict Prices", use_container_width=True, type="primary")

    if submitted:
        with st.spinner("Analyzing market trends..."):
            r = api_post("/ai/market", {"crop": crop, "days": days})
            
        if r.get("success"):
            st.markdown("---")
            rec = r["recommendation"]
            color = {"Buy": "green", "Sell": "red", "Hold": "orange", "Monitor": "blue"}
            st.markdown(f"#### Recommendation: :{color.get(rec['action'], 'blue')}[**{rec['action']}**] — {rec['message']}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Price", f"₹{r['current_price']:,}/q")
            preds = r["predictions"]["prices"]
            avg = sum(preds) / len(preds)
            delta = avg - r["current_price"]
            c2.metric(f"Avg Expected ({days}d)", f"₹{avg:,.0f}", f"{delta:+,.0f}")
            c3.metric("Overall Trend", r["trend"].title())

            st.markdown("#### 📉 Price Forecast")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=r["predictions"]["dates"], y=preds, mode="lines+markers", name="Price", line=dict(color="#2E7D32")))
            fig.add_trace(go.Scatter(x=r["predictions"]["dates"], y=r["predictions"]["moving_avg"], mode="lines", name="7-day MA", line=dict(dash="dash", color="#81C784")))
            fig.update_layout(title=f"{crop} Price Forecast", template="plotly_white", height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

            if r.get("market_tips"):
                st.markdown("#### 💡 Market Tips")
                for tip in r["market_tips"]:
                    st.write(f"- {tip}")
        else:
            st.error(r.get("error", "Analysis failed. Please try again."))
