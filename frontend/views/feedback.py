"""Feedback page."""

import streamlit as st


def show():
    st.markdown("### 💬 Send Feedback")
    st.markdown("Help us improve Trinetra Agro AI for farmers everywhere.")

    with st.form("feedback_form"):
        feature = st.selectbox("Which feature are you reviewing?", ["AI Advisor", "Disease Scanner", "Market Intelligence", "Risk Monitor", "Yield Prediction", "Profit Calculator", "Voice AI"])
        st.markdown("#### How was your experience?")
        rating = st.slider("Rating (1 = Poor, 5 = Excellent)", 1, 5, 4)
        comment = st.text_area("Your thoughts", placeholder="What worked well? What can we improve?")

        submitted = st.form_submit_button("Submit Feedback", use_container_width=True, type="primary")

    if submitted:
        if comment.strip():
            st.toast("Feedback submitted! Thank you.")
            st.success("✅ **Thank you!** Your feedback helps us improve Trinetra.")
        else:
            st.warning("⚠️ Please add a comment before submitting.")
