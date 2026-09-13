import streamlit as st
from database import create_user, authenticate_user
from src.utils.navigation import navigate_to


def render_login():
    st.markdown(
        """
        <div style='text-align:center;margin-bottom:18px;padding-top:6px;'>
            <div style='display:inline-flex;align-items:center;justify-content:center;width:60px;height:60px;border-radius:20px;background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);box-shadow:0 8px 24px rgba(37,99,235,0.45);font-size:26px;margin-bottom:10px;'>
                🔗
            </div>
            <h2 style='margin:0;font-size:22px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;'>SkillLink</h2>
            <p style='margin:4px 0 0 0;color:#94a3b8;font-size:12px;'>Connected Mobility & On-Demand Services</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Create Account"])

    # ==================== TAB 1: SIGN IN ====================
    with tab_signin:
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.caption("Sign in with your registered mobile phone and security PIN.")

        phone_in = st.text_input(
            "Phone Number",
            value=st.session_state.get("user_phone", "+92 300 1234567"),
            placeholder="+92 300 1234567",
            key="signin_phone",
        )

        password_in = st.text_input(
            "Password / PIN (or Demo Code: 1234)",
            type="password",
            value="1234",
            placeholder="••••",
            key="signin_password",
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        col_login, col_demo = st.columns([1.2, 1])
        with col_login:
            if st.button("Sign In ➔", type="primary", use_container_width=True):
                success, msg, user_data = authenticate_user(phone_in, password_in)
                if success:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = user_data["name"]
                    st.session_state.user_phone = user_data["phone"]
                    st.session_state.user_email = user_data["email"]
                    st.session_state.app_mode = user_data["role"]
                    st.session_state.wallet_balance = user_data.get("wallet_balance", 1850.0)
                    st.toast(msg)
                    navigate_to("home")
                else:
                    st.error(msg)

        with col_demo:
            if st.button("⚡ 1-Click Demo", type="secondary", use_container_width=True):
                success, msg, user_data = authenticate_user("+92 300 1234567", "1234")
                if success:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = user_data["name"]
                    st.session_state.user_phone = user_data["phone"]
                    st.session_state.user_email = user_data["email"]
                    st.session_state.app_mode = "Client"
                    st.session_state.wallet_balance = user_data.get("wallet_balance", 1850.0)
                    st.toast("Signed in as Abeer Ahmed!")
                    navigate_to("home")

    # ==================== TAB 2: CREATE ACCOUNT (SIGN UP) ====================
    with tab_signup:
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='background:rgba(37,99,235,0.14);border:1px solid rgba(59,130,246,0.3);padding:10px 12px;border-radius:14px;margin-bottom:12px;'>
                <b style='color:#93c5fd;font-size:12px;'>🎁 Welcome Promotion:</b>
                <span style='color:#e2e8f0;font-size:11px;'> New accounts receive <b>Rs. 1,000</b> wallet bonus instantly.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        reg_name = st.text_input("Full Name", placeholder="e.g. Fatima Ali", key="signup_name")
        reg_phone = st.text_input("Mobile Number", placeholder="+92 300 9876543", key="signup_phone")
        reg_email = st.text_input("Email Address", placeholder="fatima@example.com", key="signup_email")
        reg_pass = st.text_input("Create Password / 4-Digit PIN", type="password", placeholder="••••", key="signup_pass")

        reg_role_choice = st.radio(
            "Account Type",
            ["Client (Book rides & home services)", "Partner (Provide services & earn)"],
            index=0,
            horizontal=False,
            key="signup_role",
        )
        selected_role = "Client" if "Client" in reg_role_choice else "Provider"

        # Partner-specific onboarding fields
        p_trade = "Ride"
        p_exp = 3
        p_bio = "Experienced professional ready to serve."
        p_rate = 800.0
        p_radius = 15.0
        p_avail = "Full-time (24/7)"

        if selected_role == "Provider":
            st.markdown(
                """
                <div style='background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);padding:10px 12px;border-radius:14px;margin:8px 0 12px 0;'>
                    <b style='color:#34d399;font-size:12px;'>🛠️ Partner Profile Setup:</b>
                    <span style='color:#cbd5e1;font-size:11px;'> Configure your trade, skills, and rates to start receiving jobs.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_trade = st.selectbox(
                    "Trade Category",
                    ["Ride", "Plumber", "Electrician", "AC Repair", "Delivery", "Cleaning", "Tutor", "Carpenter"],
                    key="p_trade_sel",
                )
                p_rate = st.number_input("Standard Base Rate (Rs.)", min_value=100, max_value=15000, value=800, step=50, key="p_rate_num")
                p_radius = st.number_input("Service Radius (km)", min_value=1, max_value=60, value=15, step=1, key="p_rad_num")
            with col_p2:
                p_exp = st.number_input("Years of Experience", min_value=1, max_value=40, value=4, key="p_exp_num")
                p_avail = st.selectbox(
                    "Availability",
                    ["Full-time (24/7)", "Daily 9AM - 6PM", "Evening Shifts", "Weekends Only"],
                    key="p_avail_sel",
                )
            p_bio = st.text_area(
                "Skills Summary & Experience",
                placeholder="e.g. Certified master technician with 4+ years of field experience across Islamabad...",
                value=f"Certified {p_trade} specialist with {p_exp} years of field experience.",
                key="p_bio_txt",
            )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        if st.button("Create Account & Claim Bonus 🚀", type="primary", use_container_width=True):
            if not reg_name or not reg_phone or not reg_email or not reg_pass:
                st.error("Please fill in all registration fields.")
            elif len(reg_phone) < 10:
                st.error("Please enter a valid mobile number (e.g. +92 300 1234567).")
            elif "@" not in reg_email or "." not in reg_email:
                st.error("Please enter a valid email address.")
            else:
                success, msg, user_data = create_user(
                    name=reg_name,
                    phone=reg_phone,
                    email=reg_email,
                    password=reg_pass,
                    role=selected_role,
                    trade_category=p_trade if selected_role == "Provider" else "Ride",
                    experience_years=p_exp if selected_role == "Provider" else 0,
                    bio=p_bio if selected_role == "Provider" else "",
                    base_rate=float(p_rate) if selected_role == "Provider" else 500.0,
                    service_radius_km=float(p_radius) if selected_role == "Provider" else 15.0,
                    availability_status=p_avail if selected_role == "Provider" else "Available",
                )
                if success:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = user_data["name"]
                    st.session_state.user_phone = user_data["phone"]
                    st.session_state.user_email = user_data["email"]
                    st.session_state.app_mode = user_data["role"]
                    if user_data["role"] == "Provider":
                        st.session_state.provider_name = user_data["name"]
                        st.session_state.provider_phone = user_data["phone"]
                    st.session_state.wallet_balance = user_data.get("wallet_balance", 1000.0)
                    st.toast(msg)
                    navigate_to("home")
                else:
                    st.error(msg)
