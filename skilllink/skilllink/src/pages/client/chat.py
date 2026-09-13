import streamlit as st
import datetime
from src.utils.navigation import navigate_to, render_bottom_nav

QUICK_REPLIES = [
    "I'm waiting at the gate 🚪",
    "How many minutes left? ⏳",
    "Please call me 📞",
    "Okay, sounds good! 👍",
]


def render_chat():
    provider_name = st.session_state.get("active_chat_provider", "Ahmed Khan")

    col_back, col_info, col_call = st.columns([1, 4, 1])
    with col_back:
        if st.button("←", key="back_from_chat", type="secondary"):
            navigate_to("home")
    with col_info:
        st.markdown(
            f"""
            <div style='line-height:1.2;'>
                <b style='font-size:15px;color:#f3f4f6;'>{provider_name}</b><br>
                <span style='color:#34d399;font-size:11px;font-weight:600;'>
                    <span class='pulse-dot'></span> Active & Online
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_call:
        if st.button("📞", key="chat_call_btn", type="secondary"):
            st.toast(f"Starting encrypted audio call with {provider_name}...")

    # Ensure provider has conversation history
    if provider_name not in st.session_state.chat_history:
        st.session_state.chat_history[provider_name] = [
            {"role": "them", "text": f"Assalam-o-Alaikum! I am your SkillLink provider for today. How can I help?", "time": "Just now"}
        ]

    # Render message bubbles
    history = st.session_state.chat_history[provider_name]
    for msg in history:
        role = "assistant" if msg["role"] == "them" else "user"
        time_str = msg.get("time", "")
        with st.chat_message(role):
            st.markdown(f"{msg['text']} <span style='float:right;color:#6b7280;font-size:10px;margin-left:8px;'>{time_str}</span>", unsafe_allow_html=True)

    # Quick reply chips
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    st.caption("Quick suggestions:")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button(QUICK_REPLIES[0], key="qr_1", type="secondary", use_container_width=True):
            send_message(provider_name, QUICK_REPLIES[0])
        if st.button(QUICK_REPLIES[2], key="qr_3", type="secondary", use_container_width=True):
            send_message(provider_name, QUICK_REPLIES[2])
    with col_q2:
        if st.button(QUICK_REPLIES[1], key="qr_2", type="secondary", use_container_width=True):
            send_message(provider_name, QUICK_REPLIES[1])
        if st.button(QUICK_REPLIES[3], key="qr_4", type="secondary", use_container_width=True):
            send_message(provider_name, QUICK_REPLIES[3])

    # Message Input
    user_input = st.chat_input("Type your message to provider...")
    if user_input:
        send_message(provider_name, user_input)

    render_bottom_nav()


def send_message(provider_name: str, text: str):
    now_str = datetime.datetime.now().strftime("%I:%M %p")
    # Add user message
    st.session_state.chat_history[provider_name].append({
        "role": "me",
        "text": text,
        "time": now_str,
    })

    # Generate simulated reply
    replies = [
        "Understood, I am on my way!",
        "Got it, arriving at your location shortly.",
        "Sure, no problem at all!",
        "Thanks for confirming, see you in 2 minutes.",
    ]
    simulated_reply = replies[len(st.session_state.chat_history[provider_name]) % len(replies)]
    st.session_state.chat_history[provider_name].append({
        "role": "them",
        "text": simulated_reply,
        "time": now_str,
    })
    st.rerun()
