import streamlit as st
import random
from database import get_all_providers, create_booking, create_negotiation, calculate_commission
from src.utils.navigation import navigate_to, render_bottom_nav
from src.data.mock_data import SERVICES


def render_providers():
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("←", key="back_from_providers", type="secondary"):
            st.session_state.negotiating_with = None
            st.session_state.booking_in_progress = None
            navigate_to("home")
    with col_title:
        title_text = "Available Providers"
        if st.session_state.get("selected_service"):
            title_text = f"{st.session_state.selected_service} Specialists"
        st.markdown(f"#### {title_text}")

    # ---- Category & Sort Bar ----
    col_f1, col_f2 = st.columns([1.2, 1])
    with col_f1:
        current_service = st.session_state.get("selected_service", "All")
        srv_options = ["All"] + [s["label"] for s in SERVICES]
        idx = srv_options.index(current_service) if current_service in srv_options else 0
        service_filter = st.selectbox(
            "Filter Category",
            srv_options,
            index=idx,
            label_visibility="collapsed",
        )
    with col_f2:
        sort_by = st.selectbox(
            "Sort by",
            ["⚡ Fastest ETA", "💰 Lowest Fare", "⭐ Top Rated"],
            label_visibility="collapsed",
        )

    # Fetch from SQLite Database
    query = st.session_state.get("search_query", "").strip()
    filtered_providers = get_all_providers(service_filter=service_filter, search_query=query)

    # Sorting
    if "Lowest Fare" in sort_by:
        filtered_providers.sort(key=lambda x: x["price"])
    elif "Top Rated" in sort_by:
        filtered_providers.sort(key=lambda x: x["rating"], reverse=True)
    else:
        filtered_providers.sort(key=lambda x: int(str(x["eta"]).split()[0]))

    st.markdown(
        f"<span style='color:#94a3b8;font-size:12px;font-weight:600;'>{len(filtered_providers)} verified professionals active in your area</span>",
        unsafe_allow_html=True,
    )

    # ==================== NEGOTIATION MODAL ====================
    neg_p = st.session_state.get("negotiating_with")
    if neg_p:
        st.markdown(
            f"""
            <div class='modal-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <b style='color:#60a5fa;font-size:16px;'>🤝 Real-Time Fare Negotiation</b>
                    <span class='badge-pending'>Live Bid</span>
                </div>
                <div style='margin:10px 0;background:#1e293b;padding:12px;border-radius:14px;'>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='font-size:13px;color:#f8fafc;'><b>{neg_p['name']}</b> ({neg_p['service']})</span>
                        <span style='color:#fbbf24;font-size:12px;font-weight:700;'>★ {neg_p['rating']}</span>
                    </div>
                    <div style='margin-top:6px;font-size:12px;color:#94a3b8;'>
                        Standard Asking Fare: <b style='color:#ffffff;font-size:14px;'>Rs. {neg_p['price']}</b>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        proposed_bid = st.number_input(
            "Your Counter Offer (Rs.)",
            min_value=100,
            max_value=int(neg_p["price"] * 2),
            value=max(100, int(neg_p["price"]) - 150),
            step=50,
        )

        col_submit_bid, col_cancel_bid = st.columns(2)
        with col_submit_bid:
            if st.button("Submit Offer ➔", type="primary", use_container_width=True):
                create_negotiation(
                    client_name=st.session_state.user_name,
                    client_phone=st.session_state.user_phone,
                    provider_name=neg_p["name"],
                    provider_phone=neg_p.get("phone", "+92 300 0000000"),
                    service_name=neg_p["service"],
                    proposed_by="Client",
                    offer_amount=float(proposed_bid),
                )
                ratio = proposed_bid / neg_p["price"]
                if ratio >= 0.8:
                    st.toast(f"🎉 {neg_p['name']} ACCEPTED your bid of Rs. {proposed_bid}!")
                    # Persist booking to SQLite
                    created_b = create_booking(
                        client_name=st.session_state.user_name,
                        client_phone=st.session_state.user_phone,
                        provider_name=neg_p["name"],
                        provider_phone=neg_p.get("phone", "+92 300 0000000"),
                        service_name=f"{neg_p['service']} Service",
                        pickup=st.session_state.current_location,
                        dropoff="Destination / Work Location",
                        fare=float(proposed_bid),
                        payment_method="Cash on Delivery",
                    )
                    st.session_state.active_chat_provider = neg_p["name"]
                    st.session_state.negotiating_with = None
                    navigate_to("bookings")
                else:
                    counter = int(neg_p["price"] * 0.9)
                    st.warning(f"⚠️ {neg_p['name']} countered with **Rs. {counter}**.")
        with col_cancel_bid:
            if st.button("Close", type="secondary", use_container_width=True):
                st.session_state.negotiating_with = None
                st.rerun()

    # ==================== DIRECT CHECKOUT MODAL ====================
    book_p = st.session_state.get("booking_in_progress")
    if book_p:
        discount = st.session_state.get("discount_amount", 0)
        final_fare = max(50.0, float(book_p["price"]) - discount)
        split = calculate_commission(final_fare)

        st.markdown(
            f"""
            <div class='modal-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <b style='color:#34d399;font-size:16px;'>📝 Order Summary & Booking</b>
                    <span class='badge-active'>Checkout</span>
                </div>
                <div style='margin-top:10px;background:#1e293b;padding:12px;border-radius:14px;'>
                    <b style='font-size:14px;color:#f8fafc;'>{book_p['name']}</b> · <span style='color:#94a3b8;'>{book_p['service']}</span><br>
                    <span style='color:#94a3b8;font-size:12px;'>Vehicle / Tools: {book_p['vehicle']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pickup_addr = st.text_input("Pickup / Job Location", value=st.session_state.current_location)
        dropoff_addr = st.text_input("Destination / Notes", value="Blue Area, Islamabad")

        payment_method = st.selectbox(
            "Payment Channel",
            ["JazzCash (+92 300 1234567)", "EasyPaisa", f"SkillLink Wallet (Rs. {int(st.session_state.wallet_balance):,})", "Cash on Delivery"],
        )

        st.markdown(
            f"""
            <div style='background:#1e293b;padding:14px;border-radius:16px;margin:12px 0;'>
                <div style='display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;'>
                    <span>Service Asking Rate</span><span>Rs. {book_p['price']}</span>
                </div>
                <div style='display:flex;justify-content:space-between;font-size:12px;color:#34d399;margin-top:4px;'>
                    <span>Promo Discount ({st.session_state.get('applied_promo', 'None')})</span><span>- Rs. {discount}</span>
                </div>
                <hr style='border-color:rgba(255,255,255,0.1);margin:8px 0;'>
                <div style='display:flex;justify-content:space-between;font-size:15px;font-weight:800;color:#60a5fa;'>
                    <span>Total Client Fare</span><span>Rs. {int(final_fare)}</span>
                </div>
                <div style='margin-top:8px;padding:8px 10px;background:rgba(15,23,42,0.6);border-radius:8px;font-size:11px;color:#94a3b8;line-height:1.4;'>
                    ℹ️ <b>Transparency:</b> Includes 25% platform fee (Rs. {int(split['platform_fee'])}). Partner payout: <b>Rs. {int(split['provider_payout'])}</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_cb1, col_cb2 = st.columns(2)
        with col_cb1:
            if st.button("Confirm Order 🚀", type="primary", use_container_width=True):
                created_b = create_booking(
                    client_name=st.session_state.user_name,
                    client_phone=st.session_state.user_phone,
                    provider_name=book_p["name"],
                    provider_phone=book_p.get("phone", "+92 300 0000000"),
                    service_name=f"{book_p['service']} Service",
                    pickup=pickup_addr,
                    dropoff=dropoff_addr,
                    fare=final_fare,
                    payment_method=payment_method.split()[0],
                )
                st.session_state.active_chat_provider = book_p["name"]
                st.session_state.booking_in_progress = None
                st.toast(f"Order confirmed with {book_p['name']}!")
                navigate_to("bookings")
        with col_cb2:
            if st.button("Cancel", type="secondary", use_container_width=True):
                st.session_state.booking_in_progress = None
                st.rerun()

    # ==================== PROVIDER CARDS LIST ====================
    if not filtered_providers:
        st.warning("No specialists found matching your filter.")

    for i, p in enumerate(filtered_providers):
        badge_text = p.get("badge", "Verified Pro")
        st.markdown(
            f"""
            <div class='startup-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div style='line-height:1.3;'>
                        <div style='display:flex;align-items:center;gap:6px;'>
                            <b style='font-size:15px;color:#f8fafc;'>{p['name']}</b>
                            <span class='badge-verified'>✅</span>
                            <span class='badge-tag' style='font-size:9px;padding:2px 6px;'>{badge_text}</span>
                        </div>
                        <span style='color:#94a3b8;font-size:12px;'>{p['service']} · {p['vehicle']}</span><br>
                        <span style='color:#fbbf24;font-size:12px;font-weight:700;'>★ {p['rating']}</span>
                        <span style='color:#64748b;font-size:11px;'>({p['trips']} completed jobs)</span>
                    </div>
                    <div style='text-align:right;'>
                        <b style='color:#60a5fa;font-size:17px;font-weight:800;'>Rs. {int(p['price'])}</b><br>
                        <span style='color:#34d399;font-size:11px;font-weight:700;'>📍 {p['distance']} · {p['eta']}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_n, col_b = st.columns(2)
        with col_n:
            if st.button("🤝 Negotiate", key=f"p_neg_{p['id']}_{i}", type="secondary", use_container_width=True):
                st.session_state.negotiating_with = p
                st.session_state.booking_in_progress = None
                st.rerun()
        with col_b:
            if st.button("⚡ Book Now", key=f"p_book_{p['id']}_{i}", type="primary", use_container_width=True):
                st.session_state.booking_in_progress = p
                st.session_state.negotiating_with = None
                st.rerun()

    render_bottom_nav()
