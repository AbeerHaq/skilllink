import streamlit as st
from database import (
    get_incoming_requests,
    get_provider_metrics,
    get_provider_earnings_ledger,
    update_booking_step,
    create_negotiation,
    calculate_commission,
)
from src.utils.navigation import navigate_to


def render_provider_dashboard():
    provider_name = st.session_state.get("provider_name", "Ahmed Khan")

    # Fetch live performance metrics & earnings ledger
    ledger = get_provider_earnings_ledger(provider_name)
    earnings, job_count = get_provider_metrics(provider_name)
    st.session_state.provider_today_earnings = ledger["gross_revenue"]
    st.session_state.provider_today_jobs = ledger["completed_trips"]

    # ---- Provider Header & Profile ----
    col_p_info, col_mode_btn = st.columns([3.2, 1.8])
    with col_p_info:
        initials = "".join([part[0] for part in provider_name.split()[:2]]).upper() if provider_name else "PR"
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;gap:12px;padding:2px 0;'>
                <div class='avatar-circle' style='width:46px;height:46px;min-width:46px;font-size:16px;'>{initials}</div>
                <div style='line-height:1.3;'>
                    <b style='font-size:15.5px;color:#f8fafc;'>{provider_name}</b><br>
                    <span style='color:#fbbf24;font-size:11.5px;font-weight:700;'>★ 4.9 · Verified Partner</span>
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

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

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

    # ---- Partner Financial Ledger (25% Commission Split) ----
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
            <b style='font-size:14px;color:#f8fafc;'>💼 Financial Earnings Ledger</b>
            <span style='font-size:10px;color:#93c5fd;background:rgba(37,99,235,0.2);padding:2px 6px;border-radius:6px;'>25% Platform Fee</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Gross Revenue", f"Rs. {int(ledger['gross_revenue']):,}")
    with m2:
        st.metric("Net Take-Home", f"Rs. {int(ledger['net_take_home']):,}")
    with m3:
        st.metric("Completed", ledger["completed_trips"])

    st.markdown(
        f"""
        <div style='background:#1e293b;border-radius:12px;padding:8px 12px;font-size:11px;color:#94a3b8;margin-bottom:12px;'>
            Platform Commission Deducted (25%): <b style='color:#f87171;'>- Rs. {int(ledger['platform_commission']):,}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==================== ACTIVE JOB IN PROGRESS ====================
    active_job = st.session_state.get("provider_active_job")
    if active_job:
        split_active = calculate_commission(float(active_job["fare"]))
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='highlight-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <span class='badge-active'><span class='pulse-dot'></span> Active Job Execution</span>
                        <h4 style='margin:4px 0 2px 0;'>{active_job['service_name']}</h4>
                        <span style='color:#9ca3af;font-size:12px;'>Client: <b>{active_job['client_name']}</b></span>
                    </div>
                    <div style='text-align:right;'>
                        <b style='color:#60a5fa;font-size:16px;'>Rs. {int(active_job['fare'])}</b><br>
                        <span style='font-size:11px;color:#34d399;'>Take-Home: Rs. {int(split_active['provider_payout'])}</span>
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
                st.toast(f"Connecting to {active_job['client_name']} ({active_job.get('client_phone', '')})...")
        with col_finish_job:
            if st.button("Complete Job & Collect ✅", type="primary", use_container_width=True):
                update_booking_step(active_job["id"], 3)
                st.session_state.provider_active_job = None
                st.balloons()
                st.toast(f"🎉 Job completed! Rs. {int(split_active['provider_payout'])} added to your net payout.")
                st.rerun()

    # ==================== INCOMING REQUESTS QUEUE (From Database) ====================
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown("##### ⚡ Live Dispatch Queue")

    incoming_db_requests = get_incoming_requests()

    if not is_online:
        st.markdown(
            """
            <div class='startup-card' style='text-align:center;padding:20px 14px;'>
                <p style='color:#9ca3af;font-size:12.5px;margin:0;line-height:1.4;'>
                    You are currently <b>Offline</b>.<br>
                    Switch your status to <b>ONLINE</b> above to receive new incoming booking requests.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif not incoming_db_requests:
        st.markdown(
            """
            <div class='startup-card' style='text-align:center;padding:20px 14px;'>
                <div style='display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:6px;'>
                    <span class='pulse-dot'></span>
                    <b style='font-size:13px;color:#f8fafc;'>Listening for nearby requests in Islamabad...</b>
                </div>
                <p style='color:#9ca3af;font-size:11.5px;margin:0;line-height:1.4;'>New customer orders from the database will appear here automatically.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("⚡ Demo: Simulate Incoming Customer Request", type="secondary", use_container_width=True):
            from database import create_booking
            create_booking(
                client_name="Sarah Malik",
                client_phone="+92 321 5554321",
                provider_name=provider_name,
                provider_phone=st.session_state.get("provider_phone", "+92 300 1112233"),
                service_name="Plumbing & Pipe Repair",
                pickup="F-7/2 Street 14, Islamabad",
                dropoff="Kitchen Sink Leakage Service",
                fare=1200.0,
                payment_method="Cash on Delivery",
            )
            st.toast("⚡ Demo incoming customer booking added to dispatch queue!")
            st.rerun()
    else:
        for idx, req in enumerate(incoming_db_requests):
            split_req = calculate_commission(float(req["fare"]))
            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                        <div>
                            <span class='badge-pending'>Incoming Order · {req.get('date_str', 'Just now')}</span>
                            <h4 style='margin:6px 0 2px 0;font-size:15px;'>{req['service_name']}</h4>
                            <span style='color:#9ca3af;font-size:12px;'>Client: <b>{req['client_name']}</b></span>
                        </div>
                        <div style='text-align:right;'>
                            <b style='color:#60a5fa;font-size:16px;'>Rs. {int(req['fare'])}</b><br>
                            <span style='color:#34d399;font-size:11px;font-weight:600;'>Net Take-Home: Rs. {int(split_req['provider_payout'])}</span>
                        </div>
                    </div>
                    <div style='margin-top:8px;font-size:11px;color:#9ca3af;background:#0b0f19;padding:8px;border-radius:8px;'>
                        📍 {req['pickup']} ➔ 🎯 {req['dropoff']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_acc, col_cnt, col_dec = st.columns([1.2, 1, 1])
            with col_acc:
                if st.button(f"Accept ➔", key=f"acc_req_{req['id']}", type="primary", use_container_width=True):
                    update_booking_step(req["id"], 1)  # Move to En Route
                    st.session_state.provider_active_job = req
                    st.toast(f"Job accepted from {req['client_name']}!")
                    st.rerun()
            with col_cnt:
                if st.button("Counter 🤝", key=f"cnt_req_{req['id']}", type="secondary", use_container_width=True):
                    st.session_state[f"counter_mode_{req['id']}"] = not st.session_state.get(f"counter_mode_{req['id']}", False)
                    st.rerun()
            with col_dec:
                if st.button("Decline", key=f"dec_req_{req['id']}", type="secondary", use_container_width=True):
                    st.toast("Request declined.")
                    st.rerun()

            # Optional counter input
            if st.session_state.get(f"counter_mode_{req['id']}", False):
                with st.expander(f"🤝 Propose Counter Offer for Order {req.get('booking_code', '')}", expanded=True):
                    counter_val = st.number_input(
                        "Your Counter Price (Rs.)",
                        min_value=100,
                        max_value=15000,
                        value=int(req["fare"] * 1.15),
                        step=50,
                        key=f"p_cnt_val_{req['id']}",
                    )
                    if st.button("Send Counter-Offer to Client ➔", key=f"p_send_cnt_{req['id']}", type="primary"):
                        create_negotiation(
                            client_name=req["client_name"],
                            client_phone=req.get("client_phone", ""),
                            provider_name=provider_name,
                            provider_phone=st.session_state.get("provider_phone", "+92 300 1112233"),
                            service_name=req["service_name"],
                            proposed_by="Provider",
                            offer_amount=float(req["fare"]),
                            counter_amount=float(counter_val),
                        )
                        st.session_state[f"counter_mode_{req['id']}"] = False
                        st.toast(f"Counter offer of Rs. {counter_val} sent to {req['client_name']}!")
                        st.rerun()

    # ---- Provider Services & Verification Info ----
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown("##### 🚗 Partner Credentials & Verification")
    st.markdown(
        """
        <div class='startup-card' style='padding:16px 18px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.08);'>
                <span style='color:#94a3b8;font-size:12px;font-weight:600;'>Registered Trade</span>
                <b style='color:#f8fafc;font-size:12.5px;text-align:right;'>Mobility & Trades Partner</b>
            </div>
            <div style='display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);'>
                <span style='color:#94a3b8;font-size:12px;font-weight:600;'>Operating Radius</span>
                <span style='color:#60a5fa;font-size:12px;font-weight:700;text-align:right;'>📍 15 km (Islamabad & RWP)</span>
            </div>
            <div style='display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);'>
                <span style='color:#94a3b8;font-size:12px;font-weight:600;'>CNIC & Police Check</span>
                <span class='badge-completed' style='font-size:11px;padding:3px 8px;'>Verified ✓</span>
            </div>
            <div style='display:flex;justify-content:space-between;align-items:center;padding-top:10px;'>
                <span style='color:#94a3b8;font-size:12px;font-weight:600;'>Safety & Insurance</span>
                <span style='color:#34d399;font-size:12px;font-weight:700;text-align:right;'>Active Policy 🛡️</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


