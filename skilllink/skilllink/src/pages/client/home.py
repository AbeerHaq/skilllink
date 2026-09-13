import streamlit as st
from database import get_services, add_booking, get_bookings

st.set_page_config(page_title="Client Home", page_icon="🚗", layout="centered")

st.title("📍 Client Dashboard")
destination = st.text_input("Where would you like to go today?", placeholder="Enter destination...")

st.markdown("### 🚘 Available Services (Loaded from Backend Database)")
services = get_services()

for name, price, time in services:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{name}** — {price} ({time})")
    with col2:
        if st.button(f"Book {name}", key=name):
            if destination:
                add_booking("John Doe", name, destination)
                st.success(f"Successfully booked {name} to {destination}!")
                st.balloons()
            else:
                st.error("Please enter a destination first!")

st.divider()
st.subheader("📋 Your Recent Database Bookings")
bookings = get_bookings()
if bookings:
    for b in bookings:
        st.text(f"Booking ID: {b[0]} | Client: {b[1]} | Service: {b[2]} | To: {b[3]} | Status: {b[4]}")
else:
    st.info("No bookings yet. Try booking a ride above!")

if st.button("← Back to Main Menu"):
    st.switch_page("app.py")