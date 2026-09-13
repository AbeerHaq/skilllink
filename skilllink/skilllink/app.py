import streamlit as st

from src.styles.theme import apply_theme
from src.state.app_state import init_session_state
from src.utils.navigation import navigate_to

from src.pages.client.login import render_login
from src.pages.client.home import render_home
from src.pages.client.providers import render_providers
from src.pages.client.bookings import render_bookings
from src.pages.client.chat import render_chat
from src.pages.client.profile import render_profile
from src.pages.provider.dashboard import render_provider_dashboard

st.set_page_config(
    page_title="SkillLink • On-Demand Mobility & Services",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Apply styling and state initialization
apply_theme()
init_session_state()

# ---------- iOS Status Bar Mockup ----------
st.markdown(
    """
    <div style='display:flex;justify-content:space-between;align-items:center;padding:0 6px 12px 6px;color:#94a3b8;font-size:12px;font-weight:700;'>
        <span>09:41</span>
        <div style='width:70px;height:14px;background:#000;border-radius:12px;'></div>
        <div style='display:flex;align-items:center;gap:6px;font-size:11px;'>
            <span>5G</span>
            <span>􀙇</span>
            <span>􀛨 100%</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Brand Header & Segmented Mode Switch ----------
col_brand, col_mode = st.columns([1.5, 1.5])
with col_brand:
    st.markdown(
        """
        <div style='display:flex;align-items:center;gap:8px;padding-top:2px;'>
            <div style='width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg, #2563eb, #1d4ed8);display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 4px 12px rgba(37,99,235,0.4);'>
                🔗
            </div>
            <div>
                <span style='font-size:17px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;'>SkillLink</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_mode:
    if st.session_state.is_authenticated:
        # Sleek segmented pill switch
        is_client = st.session_state.app_mode == "Client"
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            btn_t = "primary" if is_client else "secondary"
            if st.button("Client", key="mode_btn_client", type=btn_t, use_container_width=True):
                if not is_client:
                    st.session_state.app_mode = "Client"
                    navigate_to("home")
        with col_m2:
            btn_t = "secondary" if is_client else "primary"
            if st.button("Partner", key="mode_btn_provider", type=btn_t, use_container_width=True):
                if is_client:
                    st.session_state.app_mode = "Provider"
                    st.rerun()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ---------- Dynamic Screen Router ----------
page = st.session_state.current_page

if not st.session_state.is_authenticated:
    render_login()
elif st.session_state.app_mode == "Provider":
    render_provider_dashboard()
elif page == "home":
    render_home()
elif page == "providers":
    render_providers()
elif page == "bookings":
    render_bookings()
elif page == "chat":
    render_chat()
elif page == "profile":
    render_profile()
else:
    render_home()
