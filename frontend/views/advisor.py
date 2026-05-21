"""AI Advisor page."""

import streamlit as st
from frontend.api_client import api_post


def show():
    st.markdown("### 🌱 AI Farming Advisor")
    st.markdown("Get personalized crop recommendations based on your specific farm conditions.")

    with st.form("advisor_form"):
        st.markdown("#### Farm Parameters")
        c1, c2, c3 = st.columns(3)
        soil = c1.selectbox("Soil Type", ["loamy", "black cotton", "alluvial", "sandy", "clay", "red soil"])
        acres = c2.number_input("Land Size (acres)", 0.5, 500.0, 5.0, 0.5)
        season = c3.selectbox("Season", ["kharif", "rabi", "zaid"])
        
        st.markdown("#### Financial Constraints")
        budget = st.number_input("Budget (₹)", 5000, 10000000, 50000, 5000)
        
        submitted = st.form_submit_button("🌱 Get Crop Recommendations", use_container_width=True, type="primary")

    if submitted:
        with st.spinner("AI analyzing your farm data..."):
            r = api_post("/ai/advisor", {"soil_type": soil, "land_acres": acres, "budget": budget, "season": season})
        
        if r.get("success"):
            st.markdown("---")
            st.success(f"Top recommendations for {season.title()} season")
            
            for i, crop in enumerate(r["primary_recommendations"], 1):
                with st.expander(f"**{i}. {crop['name']}** — Match Score: {crop['score']:.0%}", expanded=(i==1)):
                    st.write(f"**Season:** {crop['season']}")
                    st.write(f"**Duration:** {crop['duration']}")
                    st.write(f"**Water Req:** {crop['water_requirement']}")
                    st.write(f"**Profit Range:** ₹{crop['profit_range']}")
                    if crop.get("diseases"):
                        st.write(f"**Watch for:** {', '.join(crop['diseases'])}")

            st.markdown("#### 💰 Expected ROI")
            returns = r["expected_returns"]
            c1, c2, c3 = st.columns(3)
            c1.metric("Conservative", f"₹{returns['conservative']:,}")
            c2.metric("Moderate", f"₹{returns['moderate']:,}", "Expected")
            c3.metric("Optimistic", f"₹{returns['optimistic']:,}")
        else:
            st.error(r.get("error", "Analysis failed. Please try again."))
