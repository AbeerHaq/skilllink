import streamlit as st
from database import get_client_bookings, update_booking_step, cancel_booking, submit_booking_rating
from src.utils.navigation import navigate_to, render_bottom_nav

STEPS = ["Assigned", "En Route", "Arrived", "Completed"]


def render_bookings():
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("←", key="back_from_bookings", type="secondary"):
            navigate_to("home")
    with col_title:
        st.markdown("#### My Bookings & Orders")

    if "bookings_tab" not in st.session_state:
        st.session_state.bookings_tab = "active"

    is_active_tab = (st.session_state.bookings_tab == "active")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        btn_t = "primary" if is_active_tab else "secondary"
        if st.button("🚀 Active Order", key="tab_btn_active", type=btn_t, use_container_width=True):
            st.session_state.bookings_tab = "active"
            st.rerun()
    with col_b2:
        btn_t = "secondary" if is_active_tab else "primary"
        if st.button("📜 Past History", key="tab_btn_history", type=btn_t, use_container_width=True):
            st.session_state.bookings_tab = "history"
            st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # Query from SQLite Database
    bookings_list = get_client_bookings(st.session_state.get("user_phone", "+92 300 1234567"))

    if is_active_tab:
        active_bookings = [b for b in bookings_list if b["status"] in ("In Progress", "Scheduled")]

        if not active_bookings:
            st.markdown(
                """
                <div class='startup-card' style='text-align:center;padding:30px 16px;'>
                    <div style='font-size:36px;margin-bottom:10px;'>🚗</div>
                    <b style='font-size:15px;'>No Active Orders</b>
                    <p style='color:#9ca3af;font-size:12px;margin:6px 0 14px 0;'>You don't have any ongoing rides or service requests right now.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Browse Available Services ➔", type="primary", use_container_width=True):
                navigate_to("home")
        else:
            job = active_bookings[0]
            booking_type = job.get("booking_type", "instant")
            step_idx = int(job.get("step", 0))
            step_idx = max(0, min(step_idx, 3))
            step_name = STEPS[step_idx]

            status_header = (
                "<span class='badge-active'><span class='pulse-dot'></span> 📅 Scheduled Booking</span>"
                if booking_type == "scheduled"
                else f"<span class='badge-active'><span class='pulse-dot'></span> Status: {step_name}</span>"
            )
            scheduled_info = (
                f"<div style='color:#fbbf24;font-size:12px;margin-top:4px;'>📅 Scheduled: {job.get('scheduled_datetime', '')}</div>"
                if booking_type == "scheduled"
                else ""
            )

            progress_html = (
                f"""
                <div style='margin-top:14px;background:#1f2937;border-radius:10px;height:8px;overflow:hidden;'>
                    <div style='background:linear-gradient(90deg, #2563eb, #10b981);height:100%;width:{(step_idx + 1) * 25}%;transition:all 0.3s;'></div>
                </div>
                <div style='display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-top:4px;'>
                    <span style='color:{"#60a5fa" if step_idx >= 0 else "#6b7280"};'>Assigned</span>
                    <span style='color:{"#60a5fa" if step_idx >= 1 else "#6b7280"};'>En Route</span>
                    <span style='color:{"#60a5fa" if step_idx >= 2 else "#6b7280"};'>Arrived</span>
                    <span style='color:{"#34d399" if step_idx >= 3 else "#6b7280"};'>Done</span>
                </div>
                """
                if booking_type != "scheduled"
                else
                """
                <div style='margin-top:12px;padding:10px;background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.25);border-radius:10px;text-align:center;color:#fbbf24;font-size:12px;'>
                    ⏰ Your specialist will be dispatched at the scheduled time.
                </div>
                """
            )

            st.markdown(
                f"""<div class='highlight-card'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<div>
{status_header}
<h3 style='margin:6px 0 2px 0;font-size:18px;'>{job['service_name']}</h3>
{scheduled_info}
<span style='color:#9ca3af;font-size:12px;'>Order ID: {job['booking_code']}</span>
</div>
<div style='text-align:right;'>
<span style='font-size:10px;color:#94a3af;'>DRIVER PIN</span><br>
<span style='background:#10b981;color:white;padding:3px 8px;border-radius:8px;font-weight:700;font-size:13px;'>
{job['otp_pin']}
</span>
</div>
</div>
{progress_html}
</div>""",
                unsafe_allow_html=True,
            )

            # Details card
            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div>
                            <b style='font-size:14px;'>{job['provider_name']}</b><br>
                            <span style='color:#9ca3af;font-size:12px;'>📞 {job.get('provider_phone', '+92 300 0000000')}</span>
                        </div>
                        <div style='text-align:right;'>
                            <b style='color:#60a5fa;font-size:15px;'>Rs. {int(job['fare'])}</b><br>
                            <span style='font-size:11px;color:#9ca3af;'>{job.get('payment_method', 'Cash')}</span>
                        </div>
                    </div>
                    <hr style='border-color:rgba(255,255,255,0.08);margin:10px 0;'>
                    <div style='font-size:12px;color:#d1d5db;'>
                        📍 <b>Pickup:</b> {job['pickup']}<br>
                        🎯 <b>Dropoff:</b> {job['dropoff']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Actions row
            col_chat, col_call, col_cancel = st.columns([1.2, 1, 1])
            with col_chat:
                if st.button("💬 Chat", key="order_chat_btn", type="primary", use_container_width=True):
                    st.session_state.active_chat_provider = job["provider_name"]
                    navigate_to("chat")
            with col_call:
                if st.button("📞 Call", key="order_call_btn", type="secondary", use_container_width=True):
                    st.toast(f"Dialing {job['provider_name']} ({job.get('provider_phone', '')})...")
            with col_cancel:
                if st.button("❌ Cancel", key="order_cancel_btn", type="secondary", use_container_width=True):
                    cancel_booking(job["id"])
                    st.toast("Order cancelled.")
                    st.rerun()

            # Advance state simulation button for Demo
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if step_idx < 3:
                if st.button(f"⚡ Demo: Advance to '{STEPS[step_idx + 1]}' Stage ➔", type="secondary", use_container_width=True):
                    update_booking_step(job["id"], step_idx + 1)
                    if step_idx + 1 == 3:
                        st.balloons()
                        st.session_state.bookings_tab = "history"
                        st.toast("🎉 Job completed! Rate your specialist below.")
                    st.rerun()
    else:
        past_bookings = [b for b in bookings_list if b["status"] != "In Progress"]
        if not past_bookings:
            st.caption("No past bookings recorded yet.")

        for b in past_bookings:
            status_badge = (
                "<span class='badge-completed'>✓ Completed</span>"
                if b["status"] == "Completed"
                else "<span class='badge-pending'>Cancelled</span>"
            )
            has_rated = bool(b.get("rating_stars") and int(b["rating_stars"]) > 0)

            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <b style='font-size:14px;'>{b['service_name']}</b>
                        {status_badge}
                    </div>
                    <span style='color:#9ca3af;font-size:12px;'>Provider: {b['provider_name']} · {b.get('date_str', 'Past')}</span>
                    <div style='display:flex;justify-content:space-between;margin-top:8px;'>
                        <span style='color:#9ca3af;font-size:12px;'>Final Paid Fare</span>
                        <b style='color:#60a5fa;'>Rs. {int(b['fare'])}</b>
                    </div>
                    {f"<div style='margin-top:6px;font-size:12px;color:#fbbf24;'>⭐ Rated: {int(b['rating_stars'])}/5 · <i style='color:#cbd5e1;'>{b.get('review_text', '')}</i></div>" if has_rated else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Interactive Rating & Review if Completed and not yet rated
            if b["status"] == "Completed" and not has_rated:
                with st.expander(f"⭐ Leave Rating & Review for {b['provider_name']}", expanded=True):
                    stars = st.selectbox(
                        "Rating Score",
                        [5, 4, 3, 2, 1],
                        format_func=lambda x: f"{'⭐' * x} ({x} Stars - {'Outstanding' if x==5 else 'Good' if x==4 else 'Average' if x==3 else 'Poor'})",
                        key=f"star_sel_{b['id']}",
                    )
                    
                    st.markdown("<span style='font-size:11px;color:#94a3b8;'>Quick Compliment Tags:</span>", unsafe_allow_html=True)
                    cp1, cp2 = st.columns(2)
                    with cp1:
                        if st.button("⚡ Punctual & Fast", key=f"cmp1_{b['id']}", type="secondary", use_container_width=True):
                            st.session_state[f"rev_val_{b['id']}"] = "Arrived very fast and punctual!"
                            st.rerun()
                        if st.button("🛠️ Expert Quality", key=f"cmp2_{b['id']}", type="secondary", use_container_width=True):
                            st.session_state[f"rev_val_{b['id']}"] = "Outstanding quality of work and very professional!"
                            st.rerun()
                    with cp2:
                        if st.button("💬 Polite & Friendly", key=f"cmp3_{b['id']}", type="secondary", use_container_width=True):
                            st.session_state[f"rev_val_{b['id']}"] = "Extremely courteous and polite behavior."
                            st.rerun()
                        if st.button("🤝 Fair & Honest", key=f"cmp4_{b['id']}", type="secondary", use_container_width=True):
                            st.session_state[f"rev_val_{b['id']}"] = "Honest pricing and transparent service."
                            st.rerun()

                    cur_text = st.session_state.get(f"rev_val_{b['id']}", "Professional, punctual, and clean service.")
                    review_in = st.text_input("Review Details", value=cur_text, key=f"rev_txt_{b['id']}")
                    if st.button("Submit Rating & Review ⭐", key=f"btn_rate_{b['id']}", type="primary", use_container_width=True):
                        submit_booking_rating(b["id"], stars, review_in)
                        st.balloons()
                        st.toast(f"Thank you! Your {stars}★ review for {b['provider_name']} has been recorded.")
                        st.rerun()

            if st.button(f"🧾 View Receipt ({b['booking_code']})", key=f"rec_{b['id']}", type="secondary"):
                st.toast(f"Receipt for {b['booking_code']} verified from database.")

    render_bottom_nav()

