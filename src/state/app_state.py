import streamlit as st
import copy
from src.data.mock_data import (
    INITIAL_BOOKINGS,
    INITIAL_INCOMING_REQUESTS,
    INITIAL_NOTIFICATIONS,
    INITIAL_SAVED_LOCATIONS,
    CHAT_MESSAGES,
)


def init_session_state():
    """
    Initializes all application state variables required for smooth client and provider workflows.
    """
    defaults = {
        # Navigation & Auth
        "app_mode": "Client",  # "Client" or "Provider"
        "current_page": "login",
        "is_authenticated": False,
        "otp_stage": "phone",  # "phone" or "otp"
        "user_phone": "+92 300 1234567",
        "user_name": "Abeer Ahmed",
        "user_email": "abeer@skilllink.pk",
        "current_location": "F-8 Markaz, Islamabad",
        # Client Flow State
        "search_query": "",
        "selected_service": None,
        "selected_category_filter": "All",
        "wallet_balance": 1850,
        "applied_promo": None,
        "discount_amount": 0,
        "negotiating_with": None,  # Provider object if modal open
        "negotiated_fare": None,
        "booking_in_progress": None,  # Provider object for direct checkout modal
        # Active Data Stores
        "bookings": copy.deepcopy(INITIAL_BOOKINGS),
        "notifications": copy.deepcopy(INITIAL_NOTIFICATIONS),
        "saved_locations": copy.deepcopy(INITIAL_SAVED_LOCATIONS),
        "chat_history": copy.deepcopy(CHAT_MESSAGES),
        "active_chat_provider": "Ahmed Khan",
        "show_notifications": False,
        "profile_subpage": None,  # "wallet", "locations", "settings", "help", "edit_profile"
        # Provider Mode State
        "provider_online": True,
        "provider_name": "Ahmed Khan",
        "provider_service": "Ride & Express Delivery",
        "provider_today_earnings": 2400,
        "provider_today_jobs": 3,
        "incoming_requests": copy.deepcopy(INITIAL_INCOMING_REQUESTS),
        "provider_active_job": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
