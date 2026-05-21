"""AI Chatbot page — conversational farming assistant."""

import streamlit as st
from frontend.api_client import api_post, API_BASE
import httpx


def show():
    st.markdown("### 💬 AI Farming Chatbot")
    st.markdown("Ask any farming question and get an instant AI-powered answer.")

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI farming assistant. Ask me anything about crops, soil, market prices, or farming techniques! 🌾"}
        ]

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about crops, soil, weather, market tips..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    r = httpx.post(
                        f"{API_BASE}/chat/send",
                        json={"message": prompt, "session_id": "main"},
                        timeout=45.0
                    )
                    if r.status_code == 200:
                        reply = r.json()["reply"]
                    else:
                        reply = "Sorry, I couldn't process that. Please try again."
                except Exception:
                    reply = "Connection error. Make sure the backend is running."

            st.write(reply)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    # Clear chat button
    if len(st.session_state.chat_messages) > 1:
        if st.button("🗑️ Clear Chat", use_container_width=False):
            try:
                httpx.post(f"{API_BASE}/chat/clear", params={"session_id": "main"}, timeout=5.0)
            except Exception:
                pass
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Chat cleared! How can I help you? 🌾"}
            ]
            st.rerun()
