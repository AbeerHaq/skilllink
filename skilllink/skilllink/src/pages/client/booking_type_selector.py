import streamlit as st
from datetime import datetime, timedelta


def render_booking_type_selector():
    st.markdown("### ⏰ Booking Method")

    booking_method = st.radio(
        "How do you want to book?",
        ["Book Now", "Schedule for Later"],
        horizontal=True
    )

    booking_data = {}

    if booking_method == "Book Now":
        booking_data["type"] = "instant"
        st.success("Provider will be matched immediately.")

    else:
        booking_data["type"] = "scheduled"

        col1, col2 = st.columns(2)

        with col1:
            booking_date = st.date_input(
                "Select Date",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=30)
            )

        with col2:
            booking_time = st.time_input("Select Time")

        time_window = st.selectbox(
            "Preferred Time Window",
            ["Exact time", "Within ±30 mins", "Within ±1 hour"]
        )

        booking_data["scheduled_datetime"] = f"{booking_date} {booking_time}"
        booking_data["time_window"] = time_window

        st.info(
            f"📅 Scheduled for {booking_date.strftime('%B %d, %Y')} "
            f"at {booking_time.strftime('%I:%M %p')}"
        )

    return booking_data
