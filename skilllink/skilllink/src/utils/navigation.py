import streamlit as st

NAV_ITEMS = [
    ("home", "🏠", "Home"),
    ("bookings", "📅", "Bookings"),
    ("chat", "💬", "Chat"),
    ("profile", "👤", "Profile"),
]


def navigate_to(page_name: str):
    """Updates the active view and resets open subpages/modals."""
    st.session_state.current_page = page_name
    st.session_state.profile_subpage = None
    st.session_state.negotiating_with = None
    st.session_state.booking_in_progress = None
    st.rerun()


def render_bottom_nav():
    """Renders the sleek, mobile-friendly bottom navigation bar with crisp text."""
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("<div id='nav-marker'></div>", unsafe_allow_html=True)

    current = st.session_state.current_page
    cols = st.columns(4)

    for col, (page_key, icon, label) in zip(cols, NAV_ITEMS):
        with col:
            is_active = current == page_key
            btn_type = "primary" if is_active else "secondary"

            # Clean emoji + label with zero text clipping
            if st.button(
                f"{icon}\n{label}",
                key=f"nav_{page_key}",
                type=btn_type,
                use_container_width=True,
            ):
                if page_key != current or st.session_state.profile_subpage is not None:
                    navigate_to(page_key)
