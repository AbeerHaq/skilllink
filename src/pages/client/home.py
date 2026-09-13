import streamlit as st
from database import get_user_notifications, mark_notifications_read, get_client_bookings
from src.components.map_ui import render_live_map
from src.utils.navigation import navigate_to, render_bottom_nav
from src.data.mock_data import SERVICES, OFFERS


def render_home():
    user_phone = st.session_state.get("user_phone", "+92 300 1234567")

    # Fetch notifications from SQLite
    db_notifs = get_user_notifications(user_phone)
    unread_notifs = sum(1 for n in db_notifs if not n.get("is_read", 0))
    bell_badge = f"🔔 {unread_notifs}" if unread_notifs > 0 else "🔔"

    col_loc, col_bell, col_user = st.columns([3.4, 0.8, 0.8])
    with col_loc:
        st.markdown(
            f"""
            <div style='line-height:1.2;padding-top:2px;'>
                <span style='color:#94a3b8;font-size:10px;font-weight:700;letter-spacing:0.5px;'>LOCATION</span><br>
                <b style='font-size:14px;color:#f8fafc;'>📍 {st.session_state.current_location}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_bell:
        if st.button(bell_badge, key="h_bell", type="secondary", use_container_width=True):
            st.session_state.show_notifications = not st.session_state.show_notifications
            st.rerun()
    with col_user:
        if st.button("👤", key="h_user", type="secondary", use_container_width=True):
            navigate_to("profile")

    # ---- Notification Drawer ----
    if st.session_state.get("show_notifications", False):
        st.markdown(
            """
            <div class='modal-card' style='margin-bottom:12px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <b style='font-size:14px;color:#60a5fa;'>🔔 Live Notifications</b>
                    <span style='font-size:11px;color:#94a3b8;'>Database Connected</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for notif in db_notifs[:4]:
            st.markdown(
                f"""
                <div style='background:#1e293b;padding:10px 12px;border-radius:14px;margin-bottom:8px;border-left:3px solid #3b82f6;'>
                    <div style='display:flex;justify-content:space-between;'>
                        <b style='font-size:12px;color:#f8fafc;'>{notif['title']}</b>
                        <span style='color:#94a3b8;font-size:10px;'>{notif.get('time', 'Recent')}</span>
                    </div>
                    <span style='color:#cbd5e1;font-size:11px;'>{notif['text']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        col_nr1, col_nr2 = st.columns(2)
        with col_nr1:
            if st.button("Mark Read", key="m_read", type="secondary"):
                mark_notifications_read(user_phone)
                st.session_state.show_notifications = False
                st.rerun()
        with col_nr2:
            if st.button("Close", key="c_notif", type="secondary"):
                st.session_state.show_notifications = False
                st.rerun()

    # ---- Active Order Banner (From SQLite) ----
    db_bookings = get_client_bookings(user_phone)
    active_jobs = [b for b in db_bookings if b["status"] == "In Progress"]
    if active_jobs:
        job = active_jobs[0]
        st.markdown(
            f"""
            <div class='highlight-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <span class='badge-active'><span class='pulse-dot'></span> Active Booking</span>
                        <h4 style='margin:6px 0 2px 0;font-size:16px;color:#ffffff;'>{job['service_name']}</h4>
                        <span style='color:#cbd5e1;font-size:12px;'>Provider: <b>{job['provider_name']}</b></span>
                    </div>
                    <div style='text-align:right;'>
                        <span style='font-size:10px;color:#94a3b8;'>DRIVER PIN</span><br>
                        <span style='background:#10b981;color:#ffffff;font-size:13px;font-weight:800;padding:2px 8px;border-radius:8px;'>
                            {job['otp_pin']}
                        </span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Track Order Progress ➔", key="btn_track_active", type="primary", use_container_width=True):
            navigate_to("bookings")

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    render_live_map()

    # ---- Smart Problem Matcher & Search Bar ----
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    # NLP / Keyword issue matcher
    issue_desc = st.text_input(
        "Describe your problem or need",
        placeholder="💡 Describe issue: e.g. 'pipe leaking under sink', 'AC not cooling', 'ride to F-7'...",
        key="home_issue_input",
    )

    if issue_desc:
        desc_lower = issue_desc.lower()
        matched_cat = None
        
        issue_keywords = {
            "Plumber": ["pipe", "leak", "tap", "sink", "drain", "water", "toilet", "flush", "plumb", "geyser", "valve"],
            "Electrician": ["wire", "spark", "fuse", "switch", "socket", "short", "power", "light", "fan", "breaker", "current", "electric"],
            "AC Repair": ["ac", "air condition", "cooling", "filter", "compressor", "gas", "chilling", "split"],
            "Ride": ["ride", "cab", "taxi", "car", "drive", "pickup", "drop", "airport", "station", "travel"],
            "Delivery": ["parcel", "package", "deliver", "courier", "food", "box", "send"],
            "Cleaning": ["clean", "dust", "maid", "sweep", "mop", "wash", "sofa", "carpet", "deep clean"],
            "Tutor": ["tutor", "teach", "math", "physics", "english", "study", "exam", "lesson", "homework", "grade"],
            "Carpenter": ["carpenter", "wood", "table", "chair", "door", "bed", "furniture", "cabinet", "shelf", "lock"],
        }
        
        for cat, kws in issue_keywords.items():
            if any(kw in desc_lower for kw in kws):
                matched_cat = cat
                break

        if matched_cat:
            st.markdown(
                f"""
                <div style='background:rgba(37,99,235,0.18);border:1px solid #3b82f6;padding:10px 14px;border-radius:14px;margin-top:6px;display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <span style='color:#93c5fd;font-size:11px;font-weight:700;'>🎯 AUTO-MATCHED SPECIALIST:</span><br>
                        <b style='color:#ffffff;font-size:14px;'>{matched_cat} Services</b>
                    </div>
                    <span class='badge-active'>Ready to Dispatch</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Find Nearest {matched_cat}s ➔", type="primary", use_container_width=True, key="btn_match_cat"):
                st.session_state.selected_service = matched_cat
                st.session_state.search_query = ""
                navigate_to("providers")
        else:
            if st.button(f"Search Providers for '{issue_desc}' ➔", type="primary", use_container_width=True, key="btn_match_custom"):
                st.session_state.selected_service = None
                st.session_state.search_query = issue_desc
                navigate_to("providers")

    search = st.text_input(
        "Search Services",
        value=st.session_state.get("search_query", ""),
        placeholder="🔍  Or search all services by name...",
        label_visibility="collapsed",
        key="home_search_bar",
    )
    if search and search != st.session_state.get("search_query", ""):
        st.session_state.search_query = search
        st.session_state.selected_service = None
        navigate_to("providers")

    # ---- Categories Grid ----
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
            <b style='font-size:15px;color:#f8fafc;'>On-Demand Services</b>
            <span style='font-size:12px;color:#60a5fa;font-weight:700;'>View All</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols1 = st.columns(3)
    for i, srv in enumerate(SERVICES[:3]):
        with cols1[i]:
            if st.button(
                f"{srv['icon']} {srv['label']}",
                key=f"h_srv_{srv['code']}",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.selected_service = srv["label"]
                st.session_state.search_query = ""
                navigate_to("providers")

    cols2 = st.columns(3)
    for i, srv in enumerate(SERVICES[3:]):
        with cols2[i]:
            if st.button(
                f"{srv['icon']} {srv['label']}",
                key=f"h_srv_{srv['code']}",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.selected_service = srv["label"]
                st.session_state.search_query = ""
                navigate_to("providers")

    # ---- Why SkillLink Stats & Trust Grid ----
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='highlight-card' style='padding:14px 16px;margin-bottom:14px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                <b style='font-size:13.5px;color:#ffffff;'>⚡ Why SkillLink?</b>
                <span style='font-size:10.5px;color:#34d399;font-weight:700;'>LIVE METRICS</span>
            </div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
                <div style='background:rgba(15,23,42,0.6);padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);'>
                    <div style='font-size:17px;font-weight:800;color:#60a5fa;'>&lt; 8 min</div>
                    <div style='font-size:10.5px;color:#94a3b8;'>Avg. Specialist Arrival</div>
                </div>
                <div style='background:rgba(15,23,42,0.6);padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);'>
                    <div style='font-size:17px;font-weight:800;color:#fbbf24;'>4.85 ★</div>
                    <div style='font-size:10.5px;color:#94a3b8;'>1,200+ Verified Jobs</div>
                </div>
                <div style='background:rgba(15,23,42,0.6);padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);'>
                    <div style='font-size:17px;font-weight:800;color:#34d399;'>20% Lower</div>
                    <div style='font-size:10.5px;color:#94a3b8;'>Direct Counter-Bidding</div>
                </div>
                <div style='background:rgba(15,23,42,0.6);padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);'>
                    <div style='font-size:17px;font-weight:800;color:#a78bfa;'>100% Insured</div>
                    <div style='font-size:10.5px;color:#94a3b8;'>NADRA & Police Checked</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Special Offers Section ----
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    st.markdown("<b style='font-size:15px;color:#f8fafc;'>🎁 Special Promotions</b>", unsafe_allow_html=True)

    for offer in OFFERS:
        is_applied = st.session_state.get("applied_promo") == offer["code"]
        st.markdown(
            f"""
            <div class='startup-card' style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <b style='font-size:14px;color:#ffffff;'>{offer['title']}</b><br>
                    <span style='color:#94a3b8;font-size:11px;'>{offer['subtitle']}</span>
                </div>
                <span class='badge-tag'>{offer['code']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_ap, col_sp = st.columns([1.5, 2])
        with col_ap:
            if is_applied:
                st.caption("✅ Promo Applied")
            else:
                if st.button(f"Claim {offer['code']}", key=f"promo_{offer['code']}", type="secondary"):
                    st.session_state.applied_promo = offer["code"]
                    st.session_state.discount_amount = offer["discount"]
                    st.toast(f"Promo {offer['code']} applied! Rs. {offer['discount']} discount ready.")
                    st.rerun()

    render_bottom_nav()
