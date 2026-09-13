import streamlit as st
from database import save_chat_message, get_chat_messages
from src.utils.navigation import navigate_to, render_bottom_nav

QUICK_REPLIES = [
    "I am waiting at the pickup gate 🚪",
    "How many minutes left? ⏳",
    "Please call me 📞",
    "Okay, sounds good! 👍",
]


def render_chat():
    provider_name = st.session_state.get("active_chat_provider", "Ahmed Khan")
    current_user = st.session_state.get("user_name", "Abeer Ahmed")

    # ---- Chat Top Header ----
    col_back, col_info, col_call = st.columns([0.8, 3.8, 0.8])
    with col_back:
        if st.button("←", key="back_from_chat", type="secondary", use_container_width=True):
            navigate_to("home")
    with col_info:
        st.markdown(
            f"""
            <div style='line-height:1.25;padding-left:6px;'>
                <b style='font-size:15px;color:#f8fafc;'>{provider_name}</b><br>
                <span style='color:#34d399;font-size:11px;font-weight:700;'>
                    <span class='pulse-dot'></span> Active & Online
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_call:
        if st.button("📞", key="chat_call_btn", type="secondary", use_container_width=True):
            st.toast(f"Connecting encrypted call to {provider_name}...")

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ---- Fetch & Render Messages ----
    db_messages = get_chat_messages(current_user, provider_name)

    if not db_messages:
        # Seed initial greeting if fresh
        save_chat_message(provider_name, current_user, "Assalam-o-Alaikum! I am your SkillLink specialist for today. How can I help?")
        db_messages = get_chat_messages(current_user, provider_name)

    # Messages Container Box
    st.markdown("<div style='min-height:220px;max-height:360px;overflow-y:auto;padding:6px 0;'>", unsafe_allow_html=True)
    for msg in db_messages:
        is_me = (msg["sender_name"] == current_user)
        time_str = msg.get("timestamp", "Now")
        
        if is_me:
            # Client outgoing message (Right aligned, Blue gradient)
            st.markdown(
                f"""
                <div style='display:flex;justify-content:flex-end;margin-bottom:10px;'>
                    <div style='background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);color:#ffffff;padding:10px 14px;border-radius:18px 18px 4px 18px;max-width:82%;box-shadow:0 4px 12px rgba(37,99,235,0.25);'>
                        <div style='font-size:13px;line-height:1.4;'>{msg['text']}</div>
                        <div style='text-align:right;font-size:9.5px;color:rgba(255,255,255,0.7);margin-top:4px;'>{time_str} · Delivered ✓</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Provider incoming message (Left aligned, Dark Slate)
            st.markdown(
                f"""
                <div style='display:flex;justify-content:flex-start;margin-bottom:10px;'>
                    <div style='background:#1e293b;border:1px solid rgba(255,255,255,0.08);color:#f8fafc;padding:10px 14px;border-radius:18px 18px 18px 4px;max-width:82%;box-shadow:0 4px 12px rgba(0,0,0,0.3);'>
                        <div style='font-size:10.5px;font-weight:700;color:#60a5fa;margin-bottom:2px;'>{provider_name}</div>
                        <div style='font-size:13px;line-height:1.4;'>{msg['text']}</div>
                        <div style='text-align:right;font-size:9.5px;color:#94a3b8;margin-top:4px;'>{time_str}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Quick Suggestions Chips ----
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    st.caption("Quick suggestions:")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button(QUICK_REPLIES[0], key="qr_1", type="secondary", use_container_width=True):
            send_db_message(current_user, provider_name, QUICK_REPLIES[0])
        if st.button(QUICK_REPLIES[2], key="qr_3", type="secondary", use_container_width=True):
            send_db_message(current_user, provider_name, QUICK_REPLIES[2])
    with col_q2:
        if st.button(QUICK_REPLIES[1], key="qr_2", type="secondary", use_container_width=True):
            send_db_message(current_user, provider_name, QUICK_REPLIES[1])
        if st.button(QUICK_REPLIES[3], key="qr_4", type="secondary", use_container_width=True):
            send_db_message(current_user, provider_name, QUICK_REPLIES[3])

    # ---- In-Frame Message Input Form ----
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    with st.form(key="chat_msg_form", clear_on_submit=True):
        col_in, col_btn = st.columns([3.8, 1.2])
        with col_in:
            typed_msg = st.text_input(
                "Type message",
                placeholder="Type a message to provider...",
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("Send ➔", type="primary", use_container_width=True)

        if submitted and typed_msg and typed_msg.strip():
            send_db_message(current_user, provider_name, typed_msg.strip())

    render_bottom_nav()


def send_db_message(sender: str, recipient: str, text: str):
    save_chat_message(sender, recipient, text)

    # Automated realistic reply simulation
    replies = [
        "Understood, I am on my way!",
        "Got it, arriving at your location shortly.",
        "Sure, no problem at all!",
        "Thanks for confirming, see you in 2 minutes.",
    ]
    simulated_reply = replies[len(text) % len(replies)]
    save_chat_message(recipient, sender, simulated_reply)
    st.rerun()

