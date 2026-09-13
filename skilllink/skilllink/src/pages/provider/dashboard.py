import streamlit as st
from src.utils.navigation import navigate_to


def render_provider_dashboard():
    # ---- Provider Header & Profile ----
    col_p_info, col_mode_btn = st.columns([3, 2])
    with col_p_info:
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;gap:10px;'>
                <div class='avatar-circle' style='width:44px;height:44px;min-width:44px;font-size:15px;'>AK</div>
                <div>
                    <b style='font-size:15px;'>{st.session_state.provider_name}</b><br>
                    <span style='color:#fbbf24;font-size:11px;'>★ 4.9 · Top Provider</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_mode_btn:
        if st.button("Client Mode 🔄", type="secondary", use_container_width=True):
            st.session_state.app_mode = "Client"
            st.session_state.current_page = "home"
            st.rerun()

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ---- Online / Offline Availability Toggle ----
    is_online = st.session_state.get("provider_online", True)
    col_status_lbl, col_toggle_btn = st.columns([2.5, 1.5])
    with col_status_lbl:
        if is_online:
            st.markdown(
                "<span class='badge-completed' style='font-size:12px;padding:6px 12px;'><span class='pulse-dot'></span> ONLINE & READY</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<span class='badge-pending' style='font-size:12px;padding:6px 12px;'>⚫ OFFLINE</span>",
                unsafe_allow_html=True,
            )
    with col_toggle_btn:
        btn_text = "Go Offline" if is_online else "Go Online"
        btn_type = "secondary" if is_online else "primary"
        if st.button(btn_text, key="provider_online_toggle", type=btn_type, use_container_width=True):
            st.session_state.provider_online = not is_online
            st.toast(f"Status changed to: {'Online' if not is_online else 'Offline'}")
            st.rerun()

    # ---- Today's Performance Metrics ----
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Today's Earnings", f"Rs. {st.session_state.provider_today_earnings:,}")
    with m2:
        st.metric("Trips / Jobs", st.session_state.provider_today_jobs)
    with m3:
        st.metric("Acceptance", "98%")

    # ==================== ACTIVE JOB IN PROGRESS ====================
    active_job = st.session_state.get("provider_active_job")
    if active_job:
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='highlight-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <span class='badge-active'><span class='pulse-dot'></span> Active Job Execution</span>
                        <h4 style='margin:4px 0 2px 0;'>{active_job['service']}</h4>
                        <span style='color:#9ca3af;font-size:12px;'>Client: <b>{active_job['client_name']}</b></span>
                    </div>
                    <div style='text-align:right;'>
                        <b style='color:#60a5fa;font-size:16px;'>Rs. {active_job['offered_fare']}</b><br>
                        <span style='font-size:11px;color:#34d399;'>Payment: Cash</span>
                    </div>
                </div>
                <hr style='border-color:rgba(255,255,255,0.1);margin:10px 0;'>
                <div style='font-size:12px;'>
                    📍 <b>Pickup:</b> {active_job['pickup']}<br>
                    🎯 <b>Destination:</b> {active_job['dropoff']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_call_client, col_finish_job = st.columns(2)
        with col_call_client:
            if st.button("📞 Call Client", type="secondary", use_container_width=True):
                st.toast(f"Connecting to {active_job['client_name']}...")
        with col_finish_job:
            if st.button("Complete Job & Collect ✅", type="primary", use_container_width=True):
                fare_earned = active_job["offered_fare"]
                st.session_state.provider_today_earnings += fare_earned
                st.session_state.provider_today_jobs += 1
                st.session_state.provider_active_job = None
                st.toast(f"🎉 Job completed! Rs. {fare_earned} added to your earnings.")
                st.rerun()

    # ==================== INCOMING REQUESTS QUEUE ====================
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown("##### ⚡ Live Dispatch Queue")

    if not is_online:
        st.markdown(
            """
            <div class='startup-card' style='text-align:center;padding:24px;'>
                <p style='color:#9ca3af;font-size:13px;margin:0;'>
                    You are currently <b>Offline</b>.<br>
                    Switch your status to <b>ONLINE</b> above to receive new incoming job leads and ride requests.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif not st.session_state.incoming_requests:
        st.markdown(
            """
            <div class='startup-card' style='text-align:center;padding:24px;'>
                <span class='pulse-dot'></span>
                <b style='font-size:13px;'>Listening for nearby requests in Islamabad...</b>
                <p style='color:#9ca3af;font-size:11px;margin:6px 0 0 0;'>New requests within 5km will appear here automatically.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for idx, req in enumerate(st.session_state.incoming_requests):
            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                        <div>
                            <span class='badge-pending'>Incoming Request · {req['time']}</span>
                            <h4 style='margin:6px 0 2px 0;font-size:15px;'>{req['service']}</h4>
                            <span style='color:#9ca3af;font-size:12px;'>Client: <b>{req['client_name']}</b> ({req['distance']})</span>
                        </div>
                        <div style='text-align:right;'>
                            <b style='color:#60a5fa;font-size:16px;'>Rs. {req['offered_fare']}</b><br>
                            <span style='color:#34d399;font-size:11px;font-weight:600;'>Offered Fare</span>
                        </div>
                    </div>
                    <div style='margin-top:8px;font-size:11px;color:#9ca3af;background:#0b0f19;padding:8px;border-radius:8px;'>
                        📍 {req['pickup']} ➔ 🎯 {req['dropoff']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_acc, col_dec = st.columns([1.5, 1])
            with col_acc:
                if st.button(f"Accept (Rs. {req['offered_fare']}) ➔", key=f"acc_req_{req['id']}", type="primary", use_container_width=True):
                    st.session_state.provider_active_job = req
                    st.session_state.incoming_requests.pop(idx)
                    st.toast(f"Job accepted from {req['client_name']}!")
                    st.rerun()
            with col_dec:
                if st.button("Decline", key=f"dec_req_{req['id']}", type="secondary", use_container_width=True):
                    st.session_state.incoming_requests.pop(idx)
                    st.toast("Request declined.")
                    st.rerun()

    # ---- Provider Services Offered ----
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("##### 🚗 Services & Vehicle")
    st.markdown(
        """
        <div class='startup-card'>
            <div style='display:flex;justify-content:space-between;'>
                <span>Registered Vehicle</span><b>Toyota Corolla (ABC-123)</b>
            </div>
            <div style='display:flex;justify-content:space-between;margin-top:6px;'>
                <span>Active City</span><b>Islamabad & Rawalpindi</b>
            </div>
            <div style='display:flex;justify-content:space-between;margin-top:6px;'>
                <span>Documents & CNIC</span><b style='color:#34d399;'>Verified ✓</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
