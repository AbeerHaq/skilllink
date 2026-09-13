import streamlit as st
from src.utils.navigation import navigate_to, render_bottom_nav


def render_profile():
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("←", key="back_from_profile", type="secondary"):
            st.session_state.profile_subpage = None
            navigate_to("home")
    with col_title:
        st.markdown("#### My Profile")

    subpage = st.session_state.get("profile_subpage")

    # ==================== SUBPAGES ====================
    if subpage == "locations":
        st.markdown("##### 📍 Saved Locations")
        st.caption("Quickly select your frequent pickup and delivery spots.")

        for loc in st.session_state.saved_locations:
            st.markdown(
                f"""
                <div class='startup-card' style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <b>{loc['icon']} {loc['label']}</b><br>
                        <span style='color:#9ca3af;font-size:12px;'>{loc['address']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        new_label = st.text_input("Location Name (e.g., Gym, Parents House)")
        new_addr = st.text_input("Full Address")
        if st.button("Add New Location +", type="primary", use_container_width=True):
            if new_label and new_addr:
                st.session_state.saved_locations.append({
                    "label": new_label,
                    "address": new_addr,
                    "icon": "📌",
                })
                st.toast(f"Saved location '{new_label}' successfully!")
                st.rerun()

        if st.button("← Back to Profile", type="secondary"):
            st.session_state.profile_subpage = None
            st.rerun()

    elif subpage == "wallet":
        st.markdown("##### 💳 SkillLink Wallet")
        st.markdown(
            f"""
            <div class='highlight-card' style='text-align:center;padding:24px;'>
                <span style='color:#9ca3af;font-size:12px;font-weight:600;'>AVAILABLE WALLET BALANCE</span>
                <h1 style='margin:8px 0;color:#60a5fa;font-size:32px;'>Rs. {st.session_state.wallet_balance:,}</h1>
                <span class='badge-completed'>Active & Verified</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<b>Quick Top-Up:</b>", unsafe_allow_html=True)
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("+ Rs. 500", type="secondary", use_container_width=True):
                st.session_state.wallet_balance += 500
                st.toast("Top-up successful: + Rs. 500")
                st.rerun()
        with col_t2:
            if st.button("+ Rs. 1,000", type="secondary", use_container_width=True):
                st.session_state.wallet_balance += 1000
                st.toast("Top-up successful: + Rs. 1,000")
                st.rerun()
        with col_t3:
            if st.button("+ Rs. 2,500", type="secondary", use_container_width=True):
                st.session_state.wallet_balance += 2500
                st.toast("Top-up successful: + Rs. 2,500")
                st.rerun()

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<b>Linked Payment Accounts:</b>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='startup-card' style='display:flex;justify-content:space-between;align-items:center;'>
                <span>📱 <b>JazzCash</b> (0300-1234567)</span><span class='badge-completed'>Linked</span>
            </div>
            <div class='startup-card' style='display:flex;justify-content:space-between;align-items:center;'>
                <span>💳 <b>Debit Card</b> (Visa •••• 4092)</span><span class='badge-completed'>Linked</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("← Back to Profile", type="secondary"):
            st.session_state.profile_subpage = None
            st.rerun()

    elif subpage == "settings":
        st.markdown("##### ⚙️ Account Settings")
        new_name = st.text_input("Full Name", value=st.session_state.user_name)
        new_email = st.text_input("Email Address", value=st.session_state.user_email)
        new_city = st.selectbox("Preferred City", ["Islamabad / Rawalpindi", "Lahore", "Karachi", "Peshawar"])

        if st.button("Save Profile Changes", type="primary", use_container_width=True):
            st.session_state.user_name = new_name
            st.session_state.user_email = new_email
            st.toast("Profile settings updated successfully!")
            st.session_state.profile_subpage = None
            st.rerun()

        if st.button("← Back to Profile", type="secondary"):
            st.session_state.profile_subpage = None
            st.rerun()

    elif subpage == "help":
        st.markdown("##### ❓ Help & 24/7 Support")
        st.markdown(
            """
            <div class='startup-card'>
                <b>🚨 Emergency Helpline</b><br>
                <span style='color:#ef4444;font-weight:700;'>Police: 15 | Rescue: 1122</span>
            </div>
            <div class='startup-card'>
                <b>💬 SkillLink Live Support</b><br>
                <span style='color:#9ca3af;font-size:12px;'>Average response time: &lt; 2 minutes</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Contact Support Team", type="primary", use_container_width=True):
            st.toast("Connecting to SkillLink agent...")

        if st.button("← Back to Profile", type="secondary"):
            st.session_state.profile_subpage = None
            st.rerun()

    else:
        # ==================== MAIN PROFILE VIEW ====================
        name_parts = st.session_state.user_name.split()
        initials = "".join(w[0] for w in name_parts[:2]).upper() or "U"

        st.markdown(
            f"""
            <div class='startup-card' style='display:flex;align-items:center;gap:14px;'>
                <div class='avatar-circle'>{initials}</div>
                <div>
                    <b style='font-size:16px;color:#f3f4f6;'>{st.session_state.user_name}</b><br>
                    <span style='color:#9ca3af;font-size:12px;'>{st.session_state.user_phone}</span><br>
                    <span style='color:#fbbf24;font-size:12px;font-weight:600;'>★ 4.95 Rating · Verified Client</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Profile Menus
        if st.button("📍  Saved Locations", key="menu_locations", type="secondary", use_container_width=True):
            st.session_state.profile_subpage = "locations"
            st.rerun()

        if st.button(f"💳  SkillLink Wallet (Rs. {st.session_state.wallet_balance:,})", key="menu_wallet", type="secondary", use_container_width=True):
            st.session_state.profile_subpage = "wallet"
            st.rerun()

        if st.button("⚙️  Account Settings", key="menu_settings", type="secondary", use_container_width=True):
            st.session_state.profile_subpage = "settings"
            st.rerun()

        if st.button("❓  Help & Safety Helpline", key="menu_help", type="secondary", use_container_width=True):
            st.session_state.profile_subpage = "help"
            st.rerun()

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        # Logout Marker
        st.markdown("<div id='logout-marker'></div>", unsafe_allow_html=True)
        if st.button("↪  Log Out", key="logout_btn", use_container_width=True):
            st.session_state.is_authenticated = False
            st.session_state.otp_stage = "phone"
            st.toast("Logged out successfully.")
            navigate_to("login")

    render_bottom_nav()
