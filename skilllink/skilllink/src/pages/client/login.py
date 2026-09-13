import streamlit as st
from src.utils.navigation import navigate_to


def render_login():
    st.markdown(
        """
        <div style='text-align:center;margin-bottom:20px;padding-top:10px;'>
            <div style='display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;border-radius:20px;background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);box-shadow:0 8px 24px rgba(37,99,235,0.4);font-size:28px;margin-bottom:12px;'>
                🔗
            </div>
            <h2 style='margin:0;font-size:24px;font-weight:800;letter-spacing:-0.5px;'>SkillLink</h2>
            <p style='margin:4px 0 0 0;color:#9ca3af;font-size:13px;'>On-Demand Services & Instant Mobility</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stage = st.session_state.get("otp_stage", "phone")

    if stage == "phone":
        st.markdown("##### Sign In / Register")
        st.caption("Enter your mobile number to receive a secure one-time passcode.")

        phone = st.text_input(
            "Mobile Number",
            value=st.session_state.user_phone,
            placeholder="+92 300 1234567",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        col_send, col_demo = st.columns([1.2, 1])
        with col_send:
            if st.button("Send Code 📲", type="primary", use_container_width=True):
                if len(phone.strip()) >= 10:
                    st.session_state.user_phone = phone
                    st.session_state.otp_stage = "otp"
                    st.toast("OTP Sent! Use demo code: 1234")
                    st.rerun()
                else:
                    st.error("Please enter a valid phone number.")

        with col_demo:
            if st.button("⚡ Quick Demo", type="secondary", use_container_width=True):
                st.session_state.user_phone = "+92 300 1234567"
                st.session_state.is_authenticated = True
                st.toast("Logged in as Abeer Ahmed!")
                navigate_to("home")

    elif stage == "otp":
        st.markdown("##### Enter Verification Code")
        st.caption(f"We sent a 4-digit code to **{st.session_state.user_phone}**")

        st.info("💡 **Hackathon Demo Code:** `1234`")

        otp_val = st.text_input(
            "OTP Code",
            max_chars=4,
            placeholder="• • • •",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        if st.button("Verify & Continue ➔", type="primary", use_container_width=True):
            if otp_val.strip() == "1234" or len(otp_val.strip()) == 4:
                st.session_state.is_authenticated = True
                st.session_state.otp_stage = "phone"
                st.toast("Verification successful! Welcome to SkillLink.")
                navigate_to("home")
            else:
                st.error("Invalid OTP. Try entering '1234'.")

        col_resend, col_back = st.columns(2)
        with col_resend:
            if st.button("Resend Code", type="secondary", use_container_width=True):
                st.toast("New OTP sent: 1234")
        with col_back:
            if st.button("Change Phone", type="secondary", use_container_width=True):
                st.session_state.otp_stage = "phone"
                st.rerun()
