"""Disease Scanner page."""

import io

import httpx
import streamlit as st


def show():
    st.markdown("### 🔬 AI Disease Scanner")
    st.markdown("Upload a leaf image for AI-powered disease detection and treatment recommendations.")

    API_BASE = "http://localhost:8000"

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("#### 1. Upload Image")
        uploaded = st.file_uploader("Upload leaf/crop image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        crops = ["rice", "tomato", "cotton", "potato", "wheat"]
        crop_type = st.selectbox("Select Crop Type", [c.title() for c in crops])
        
        analyze_btn = False
        if uploaded:
            st.image(uploaded, caption="Preview", use_container_width=True)
            analyze_btn = st.button("🔍 Analyze for Disease", use_container_width=True, type="primary")

    with col2:
        st.markdown("#### 2. AI Diagnosis")
        if not uploaded:
            st.info("👈 Upload an image of a leaf on the left to see the AI diagnosis here.")
        elif not analyze_btn:
            st.info("👆 Click 'Analyze for Disease' to start the scan.")
        elif analyze_btn:
            with st.spinner("AI analyzing your crop image..."):
                files = {"image": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                data = {"crop_type": crop_type.lower()}
                token = st.session_state.get("access_token", "")
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                try:
                    r = httpx.post(f"{API_BASE}/ai/disease", data=data, files=files, headers=headers, timeout=30.0)
                    result = r.json()
                except Exception as e:
                    result = {"error": str(e)}

            if result.get("success"):
                disease = result["disease"]
                conf = result["confidence"]
                severity = result.get("severity", "Unknown")

                if disease.lower() == "healthy":
                    st.success(f"✅ **Healthy** — Confidence: {conf*100:.1f}%")
                else:
                    st.error(f"⚠️ **Disease: {disease}**")
                    c1, c2 = st.columns(2)
                    c1.metric("Confidence", f"{conf*100:.1f}%")
                    c2.metric("Severity", severity)

                    st.markdown("#### 💡 Treatment")
                    st.write(result.get("recommendation", "Consult a local plant pathologist."))

                    st.markdown("#### 🛡️ Prevention")
                    for tip in result.get("prevention_tips", []):
                        st.write(f"- {tip}")

                    if result.get("note"):
                        st.info(result["note"])
            else:
                st.error(result.get("error", "Analysis failed."))
