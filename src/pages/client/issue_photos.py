import streamlit as st
from database import add_issue_photos


def render_issue_photos(current_booking):
    provider_name = current_booking.get("provider_name", "your specialist") if current_booking else "your specialist"
    booking_code = current_booking.get("booking_code", "BK-LIVE") if current_booking else "BK-LIVE"
    booking_id = current_booking.get("id") if current_booking else None

    st.markdown(
        f"""
        <div class='highlight-card' style='text-align:center;padding:16px;margin-bottom:14px;'>
            <div style='font-size:28px;margin-bottom:4px;'>📸</div>
            <b style='font-size:16px;color:#ffffff;'>Add Photos of the Issue</b>
            <p style='color:#94a3b8;font-size:12px;margin:4px 0 0 0;'>
                Help <b>{provider_name}</b> prepare the right parts & tools before arriving.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Attach photo of the issue",
        type=["jpg", "png", "jpeg"],
        help="Optional: Upload a clear picture of the damaged or service area",
        key="issue_file_uploader",
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Selected Issue Photo Preview", use_container_width=True)

    description = st.text_area(
        "Issue Notes / Specific Details:",
        placeholder="e.g., Pipe joint is rusted under the main kitchen sink. Please bring a 1/2 inch PVC connector...",
        max_chars=500,
        key="issue_desc_textarea",
    )

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Skip Photos ➔", type="secondary", use_container_width=True, key="btn_skip_photos"):
            st.session_state.skip_photos = True
            st.rerun()

    with col2:
        if st.button("Submit Details ✅", type="primary", use_container_width=True, key="btn_submit_photos"):
            if uploaded_file or (description and description.strip()):
                photo_path = f"bookings/{booking_code}/{uploaded_file.name}" if uploaded_file else ""
                desc_text = description.strip() if description else ""

                if booking_id:
                    add_issue_photos(
                        booking_id,
                        photo_path,
                        desc_text,
                    )

                st.session_state.photos_uploaded = True
                st.session_state.attached_photo_name = uploaded_file.name if uploaded_file else None
                st.toast("Photos & details attached! Specialist notified.")
                st.rerun()
            else:
                st.warning("Please attach a photo or enter a note, or click 'Skip Photos'.")
