import streamlit as st
from datetime import datetime, timedelta


def render_booking_type_selector():
    st.markdown(
        """
        <div style='margin:10px 0 6px 0;padding-top:4px;'>
            <span style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:0.5px;'>⏰ DISPATCH SCHEDULE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    booking_method = st.radio(
        "Booking Schedule",
        ["Book Now (Urgent)", "Schedule for Later"],
        horizontal=True,
        label_visibility="collapsed",
        key="booking_schedule_radio",
    )

    booking_data = {}

    if "Book Now" in booking_method:
        booking_data["type"] = "instant"
        st.markdown(
            """
            <div style='background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:8px 12px;font-size:11.5px;color:#34d399;margin-bottom:8px;'>
                ⚡ Specialist will be dispatched immediately upon order confirmation.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        booking_data["type"] = "scheduled"

        col1, col2 = st.columns(2)

        with col1:
            booking_date = st.date_input(
                "Select Date",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=30),
                key="booking_sched_date",
            )

        with col2:
            booking_time = st.time_input("Select Time", key="booking_sched_time")

        time_window = st.selectbox(
            "Preferred Time Window",
            ["Exact time", "Within ±30 mins", "Within ±1 hour"],
            key="booking_sched_window",
        )

        booking_data["scheduled_datetime"] = f"{booking_date.strftime('%d %b %Y')} at {booking_time.strftime('%I:%M %p')}"
        booking_data["time_window"] = time_window

        st.markdown(
            f"""
            <div style='background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:8px 12px;font-size:11.5px;color:#fbbf24;margin-bottom:8px;'>
                📅 <b>Reserved for:</b> {booking_data['scheduled_datetime']} ({time_window})
            </div>
            """,
            unsafe_allow_html=True,
        )

    return booking_data
