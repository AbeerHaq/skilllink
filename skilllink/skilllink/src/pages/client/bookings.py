import streamlit as st
from src.utils.navigation import navigate_to, render_bottom_nav

STEPS = ["Assigned", "En Route", "Arrived", "Completed"]


def render_bookings():
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("←", key="back_from_bookings", type="secondary"):
            navigate_to("home")
    with col_title:
        st.markdown("#### My Bookings & Orders")

    tab_active, tab_history = st.tabs(["🚀 Active Order", "📜 Past History"])

    with tab_active:
        active_bookings = [b for b in st.session_state.bookings if b["status"] == "In Progress"]

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
            step_idx = job.get("step", 0)
            step_name = STEPS[step_idx]

            st.markdown(
                f"""<div class='highlight-card'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<div>
<span class='badge-active'><span class='pulse-dot'></span> Status: {step_name}</span>
<h3 style='margin:6px 0 2px 0;font-size:18px;'>{job['service']}</h3>
<span style='color:#9ca3af;font-size:12px;'>Order ID: {job['id']}</span>
</div>
<div style='text-align:right;'>
<span style='font-size:10px;color:#94a3af;'>DRIVER PIN</span><br>
<span style='background:#10b981;color:white;padding:3px 8px;border-radius:8px;font-weight:700;font-size:13px;'>
{job['otp_pin']}
</span>
</div>
</div>
<div style='margin-top:14px;background:#1f2937;border-radius:10px;height:8px;overflow:hidden;'>
<div style='background:linear-gradient(90deg, #2563eb, #10b981);height:100%;width:{(step_idx + 1) * 25}%;transition:all 0.3s;'></div>
</div>
<div style='display:flex;justify-content:space-between;font-size:10px;color:#9ca3af;margin-top:4px;'>
<span style='color:{"#60a5fa" if step_idx >= 0 else "#6b7280"};'>Assigned</span>
<span style='color:{"#60a5fa" if step_idx >= 1 else "#6b7280"};'>En Route</span>
<span style='color:{"#60a5fa" if step_idx >= 2 else "#6b7280"};'>Arrived</span>
<span style='color:{"#34d399" if step_idx >= 3 else "#6b7280"};'>Done</span>
</div>
</div>""",
                unsafe_allow_html=True,
            )

            # Details card
            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div>
                            <b style='font-size:14px;'>{job['provider']}</b><br>
                            <span style='color:#9ca3af;font-size:12px;'>📞 {job.get('provider_phone', '+92 300 0000000')}</span>
                        </div>
                        <div style='text-align:right;'>
                            <b style='color:#60a5fa;font-size:15px;'>Rs. {job['fare']}</b><br>
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
                    st.session_state.active_chat_provider = job["provider"]
                    navigate_to("chat")
            with col_call:
                if st.button("📞 Call", key="order_call_btn", type="secondary", use_container_width=True):
                    st.toast(f"Dialing {job['provider']} ({job.get('provider_phone', '')})...")
            with col_cancel:
                if st.button("❌ Cancel", key="order_cancel_btn", type="secondary", use_container_width=True):
                    job["status"] = "Cancelled"
                    st.toast("Order cancelled.")
                    st.rerun()

            # Advance state simulation button for Demo
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if step_idx < 3:
                if st.button(f"⚡ Demo: Simulate '{STEPS[step_idx + 1]}' Stage ➔", type="secondary", use_container_width=True):
                    job["step"] = step_idx + 1
                    if job["step"] == 3:
                        job["status"] = "Completed"
                        st.toast("🎉 Job completed successfully!")
                    st.rerun()

    with tab_history:
        past_bookings = [b for b in st.session_state.bookings if b["status"] != "In Progress"]
        if not past_bookings:
            st.caption("No past bookings recorded.")

        for b in past_bookings:
            status_badge = (
                "<span class='badge-completed'>✓ Completed</span>"
                if b["status"] == "Completed"
                else "<span class='badge-pending'>Cancelled</span>"
            )
            st.markdown(
                f"""
                <div class='startup-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <b style='font-size:14px;'>{b['service']}</b>
                        {status_badge}
                    </div>
                    <span style='color:#9ca3af;font-size:12px;'>Provider: {b['provider']} · {b['date']}</span>
                    <div style='display:flex;justify-content:space-between;margin-top:8px;'>
                        <span style='color:#9ca3af;font-size:12px;'>Final Paid Fare</span>
                        <b style='color:#60a5fa;'>Rs. {b['fare']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"🧾 View Receipt ({b['id']})", key=f"rec_{b['id']}", type="secondary"):
                st.toast(f"Receipt for {b['id']} downloaded to device.")

    render_bottom_nav()
