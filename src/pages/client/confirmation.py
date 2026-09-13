import streamlit as st
from src.utils.navigation import navigate_to, render_bottom_nav


def render_confirmation():
    booking = st.session_state.get("last_confirmed_booking", {})

    if not booking:
        st.info("No recent booking found.")
        if st.button("Go to Home ➔", type="primary", use_container_width=True):
            navigate_to("home")
        render_bottom_nav()
        return

    # Trigger celebration balloons once
    if not st.session_state.get("confirmation_balloons_shown", False):
        st.balloons()
        st.session_state.confirmation_balloons_shown = True

    st.markdown(
        """
        <div style='text-align:center;padding:12px 0 6px 0;'>
            <div style='display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;border-radius:24px;background:rgba(16,185,129,0.18);border:2px solid #10b981;font-size:30px;margin-bottom:12px;'>
                ✅
            </div>
            <h2 style='margin:0;font-size:22px;font-weight:800;color:#ffffff;'>Booking Confirmed!</h2>
            <p style='margin:4px 0 0 0;color:#94a3b8;font-size:13px;'>Your specialist has been dispatched and is on the way.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    booking_code = booking.get("booking_code", "BK-LIVE")
    otp_pin = booking.get("otp_pin", "4821")
    provider_name = booking.get("provider_name", "Assigned Specialist")
    provider_phone = booking.get("provider_phone", "+92 300 0000000")
    service_name = booking.get("service_name", "On-Demand Service")
    fare = booking.get("fare", 0.0)
    payment_method = booking.get("payment_method", "Cash on Delivery")
    pickup = booking.get("pickup", "Current Location")
    dropoff = booking.get("dropoff", "Work Location")

    # OTP Security Card
    st.markdown(
        f"""
        <div class='highlight-card' style='text-align:center;padding:18px;'>
            <span style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;'>SECURITY VERIFICATION PIN</span>
            <div style='font-size:32px;font-weight:900;letter-spacing:6px;color:#10b981;margin:6px 0;'>
                {otp_pin}
            </div>
            <span style='color:#cbd5e1;font-size:11.5px;'>Share this 4-digit code with your specialist upon arrival.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Order Summary Card
    st.markdown(
        f"""
        <div class='startup-card' style='padding:16px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.08);'>
                <div>
                    <span style='color:#60a5fa;font-size:11px;font-weight:700;'>ORDER ID: {booking_code}</span>
                    <h4 style='margin:2px 0 0 0;font-size:15px;color:#ffffff;'>{service_name}</h4>
                </div>
                <div style='text-align:right;'>
                    <b style='color:#60a5fa;font-size:17px;'>Rs. {int(fare)}</b><br>
                    <span style='color:#94a3b8;font-size:10.5px;'>{payment_method}</span>
                </div>
            </div>
            <div style='display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.08);'>
                <div>
                    <span style='color:#94a3b8;font-size:11px;'>Specialist</span><br>
                    <b style='color:#f8fafc;font-size:13px;'>{provider_name}</b>
                </div>
                <div style='text-align:right;'>
                    <span style='color:#94a3b8;font-size:11px;'>Phone</span><br>
                    <span style='color:#cbd5e1;font-size:12px;'>{provider_phone}</span>
                </div>
            </div>
            <div style='padding-top:10px;font-size:12px;color:#cbd5e1;line-height:1.5;'>
                📍 <b>Pickup:</b> {pickup}<br>
                🎯 <b>Destination:</b> {dropoff}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action Buttons
    col_track, col_chat = st.columns(2)
    with col_track:
        if st.button("Track Live Order ➔", type="primary", use_container_width=True, key="btn_confirm_track"):
            navigate_to("bookings")
    with col_chat:
        if st.button("💬 Chat with Specialist", type="secondary", use_container_width=True, key="btn_confirm_chat"):
            st.session_state.active_chat_provider = provider_name
            navigate_to("chat")

    if st.button("Return to Home", type="secondary", use_container_width=True, key="btn_confirm_home"):
        navigate_to("home")

    render_bottom_nav()
