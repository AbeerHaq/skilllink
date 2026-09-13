import streamlit as st
from database import add_issue_photos


def render_issue_photos(current_booking):
    st.markdown("### 📸 Share Issue Photos")
    st.write(f"Help {current_booking['provider_name']} see the problem before accepting.")

    uploaded_file = st.file_uploader(
        "Upload photo of the issue",
        type=["jpg", "png", "jpeg"]
    )

    description = st.text_area(
        "Describe the issue:",
        max_chars=500
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Skip Photos", use_container_width=True):
            st.session_state.skip_photos = True
            st.rerun()

    with col2:
        if st.button("Submit Photos", use_container_width=True, type="primary"):
            if uploaded_file and description:
                photo_path = f"bookings/{current_booking['booking_code']}/{uploaded_file.name}"

                add_issue_photos(
                    current_booking["id"],
                    photo_path,
                    description
                )

                st.success("Photos uploaded! Provider will review before accepting.")
                st.session_state.photos_uploaded = True
                st.rerun()
            else:
                st.warning("Please upload a photo and add a description.")
