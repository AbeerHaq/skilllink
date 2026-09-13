"""
Live Map Component for SkillLink.
Powered by:
- Leaflet: Included directly inside folium (no extra JS files or keys).
- OpenStreetMap tiles: Automatically rendered by Folium (free, no API key needed).
- streamlit-folium: Bridges Folium maps into Streamlit components.
- Nominatim: Optional geocoding via OpenStreetMap public endpoint (no registration required).
"""

import streamlit as st
import folium
try:
    from streamlit_folium import st_folium
except ImportError:
    st_folium = None

import requests
import html


# Default location: F-8 Markaz, Islamabad
DEFAULT_LAT = 33.7073
DEFAULT_LON = 73.0428

# Known Islamabad coordinates for instant offline fallback
KNOWN_COORDINATES = {
    "f-8 markaz, islamabad": (33.7073, 73.0428),
    "f-8 markaz": (33.7073, 73.0428),
    "f-7 markaz, islamabad": (33.7215, 73.0558),
    "blue area, islamabad": (33.7145, 73.0645),
    "centaurus mall, islamabad": (33.7077, 73.0553),
    "centaurus mall": (33.7077, 73.0553),
    "g-9 markaz, islamabad": (33.6896, 73.0336),
    "f-10 markaz, islamabad": (33.6934, 73.0118),
    "islamabad": (33.6844, 73.0479),
    "rawalpindi": (33.5651, 73.0169),
}


@st.cache_data(ttl=3600, show_spinner=False)
def geocode_with_nominatim(query: str):
    """
    Geocodes an address or landmark using OpenStreetMap's free public Nominatim endpoint.
    No API key registration is required.
    Includes fallback to known Pakistani coordinates if offline or rate limited.
    """
    if not query or not query.strip():
        return DEFAULT_LAT, DEFAULT_LON, "Islamabad"

    normalized_q = query.strip().lower()
    for key, coords in KNOWN_COORDINATES.items():
        if key in normalized_q or normalized_q in key:
            return coords[0], coords[1], query

    endpoint = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "SkillLink-Streamlit-App/1.0 (https://skilllink.pk; support@skilllink.pk)"
    }
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=4)
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                first = results[0]
                lat = float(first["lat"])
                lon = float(first["lon"])
                display_name = first.get("display_name", query)
                return lat, lon, display_name
    except Exception:
        pass

    # Fallback default
    return DEFAULT_LAT, DEFAULT_LON, query


def get_category_marker_config(service: str):
    """Returns color and icon configuration for different service types in Leaflet."""
    srv = (service or "").lower()
    if "ride" in srv or "cab" in srv:
        return {"color": "blue", "icon": "car", "prefix": "fa", "badge": "🚗"}
    elif "plumb" in srv:
        return {"color": "green", "icon": "wrench", "prefix": "fa", "badge": "🔧"}
    elif "elect" in srv:
        return {"color": "orange", "icon": "bolt", "prefix": "fa", "badge": "⚡"}
    elif "deliv" in srv:
        return {"color": "red", "icon": "shopping-bag", "prefix": "fa", "badge": "📦"}
    elif "ac" in srv or "cool" in srv:
        return {"color": "purple", "icon": "snowflake-o", "prefix": "fa", "badge": "❄️"}
    elif "clean" in srv:
        return {"color": "cadetblue", "icon": "tint", "prefix": "fa", "badge": "🧹"}
    return {"color": "darkblue", "icon": "user", "prefix": "fa", "badge": "🛠️"}


def render_live_map():
    """
    Renders an interactive Leaflet map powered by Folium, OpenStreetMap tiles,
    and optional Nominatim geocoding directly in Streamlit.
    """
    # 1. Resolve current user position
    loc_str = st.session_state.get("current_location", "F-8 Markaz, Islamabad")
    
    # Check if cached coordinates are in session_state, else geocode
    if "user_lat" not in st.session_state or "user_lon" not in st.session_state or st.session_state.get("last_geocoded_loc") != loc_str:
        user_lat, user_lon, _ = geocode_with_nominatim(loc_str)
        st.session_state.user_lat = user_lat
        st.session_state.user_lon = user_lon
        st.session_state.last_geocoded_loc = loc_str
    else:
        user_lat = st.session_state.user_lat
        user_lon = st.session_state.user_lon

    # Nearby providers
    try:
        from database import get_all_providers
        active_providers = get_all_providers()
    except Exception:
        from src.data.mock_data import PROVIDERS
        active_providers = PROVIDERS

    # Header Bar for the Map
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:6px;">
                <span class="pulse-dot"></span>
                <b style="font-size:13px;color:#93c5fd;">Leaflet & OpenStreetMap Live GPS</b>
            </div>
            <span style="background:rgba(37,99,235,0.25);border:1px solid rgba(59,130,246,0.45);border-radius:9999px;padding:2px 8px;font-size:11px;color:#60a5fa;font-weight:700;">
                ⚡ {len(active_providers)} Pros nearby
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Build Folium Map (Leaflet) using OpenStreetMap Tiles
    # OpenStreetMap tiles are built-in and require no API keys
    m = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=14,
        tiles="OpenStreetMap",
        control_scale=True,
        prefer_canvas=True,
    )

    # Add Proximity Coverage Circle (1.2 km radar radius)
    folium.Circle(
        location=[user_lat, user_lon],
        radius=1200,
        color="#3b82f6",
        weight=2,
        fill=True,
        fill_color="#2563eb",
        fill_opacity=0.12,
        dash_array="6, 6",
        tooltip="5-Minute Dispatch Coverage Zone",
    ).add_to(m)

    # Add Client / User Location Marker
    user_popup_html = f"""
    <div style='font-family:sans-serif;font-size:12px;line-height:1.4;'>
        <b style='color:#2563eb;'>📍 Your Location</b><br>
        <span>{html.escape(loc_str)}</span><br>
        <span style='color:#64748b;font-size:10px;'>GPS: {user_lat:.4f}, {user_lon:.4f}</span>
    </div>
    """
    folium.Marker(
        location=[user_lat, user_lon],
        popup=folium.Popup(user_popup_html, max_width=220),
        tooltip=f"You are here ({loc_str})",
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(m)

    # Known offset coordinates for demo providers relative to user
    provider_offsets = [
        (0.0032, 0.0024),
        (-0.0038, 0.0031),
        (0.0048, -0.0039),
        (-0.0022, -0.0033),
        (0.0058, 0.0048),
        (-0.0045, -0.0042),
    ]

    # Plot each provider on the Leaflet Map
    for idx, p in enumerate(active_providers[:6]):
        offset = provider_offsets[idx % len(provider_offsets)]
        p_lat = user_lat + p.get("lat_offset", offset[0])
        p_lon = user_lon + p.get("lon_offset", offset[1])

        cfg = get_category_marker_config(p.get("service", ""))
        p_name = html.escape(str(p.get("name", "Provider")))
        p_service = html.escape(str(p.get("service", "Service")))
        p_rating = p.get("rating", 4.9)
        p_eta = html.escape(str(p.get("eta", "5m")))
        p_price = p.get("price", 500)
        p_vehicle = html.escape(str(p.get("vehicle", "Vehicle")))

        popup_content = f"""
        <div style='font-family:sans-serif;font-size:12px;min-width:140px;line-height:1.4;'>
            <b style='color:#0f172a;font-size:13px;'>{cfg['badge']} {p_name}</b><br>
            <span style='color:#2563eb;font-weight:600;'>{p_service} Specialist</span><br>
            <span>⭐ <b>{p_rating}</b> &bull; ⏱️ <b>{p_eta}</b></span><br>
            <span>💰 <b>Rs. {int(p_price)}</b></span><br>
            <span style='color:#64748b;font-size:10px;'>🚗 {p_vehicle}</span>
        </div>
        """

        folium.Marker(
            location=[p_lat, p_lon],
            popup=folium.Popup(popup_content, max_width=240),
            tooltip=f"{cfg['badge']} {p_name} ({p_service}) - {p_eta} away",
            icon=folium.Icon(color=cfg["color"], icon=cfg["icon"], prefix=cfg["prefix"]),
        ).add_to(m)

    # 3. Render Leaflet Map in Streamlit
    map_container_style = """
    <style>
    .folium-map-wrapper iframe {
        border-radius: 18px !important;
        border: 1px solid rgba(59, 130, 246, 0.35) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    }
    </style>
    """
    st.markdown(map_container_style, unsafe_allow_html=True)

    # Display map via streamlit-folium or fallback
    rendered = False
    if st_folium is not None:
        try:
            st_folium(
                m,
                height=230,
                use_container_width=True,
                returned_objects=[],
                key="skilllink_live_folium_map",
            )
            rendered = True
        except Exception:
            rendered = False

    if not rendered:
        # Graceful fallback: render folium HTML directly via iframe
        map_html = m._repr_html_()
        st.components.v1.html(map_html, height=235)

    # 4. Interactive Nominatim Geocoding Tool (Optional address finder)
    with st.expander("📍 Change Location (OSM Geocoder)", expanded=False):
        st.markdown(
            """
            <div style='font-size:11px;color:#94a3b8;margin-bottom:6px;'>
                Using <b>OpenStreetMap Nominatim</b> public API (No API key required). Enter any city, sector, or landmark:
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_g1, col_g2 = st.columns([2.5, 1])
        with col_g1:
            geo_input = st.text_input(
                "Search address or landmark",
                value=st.session_state.current_location,
                label_visibility="collapsed",
                placeholder="e.g. Blue Area, Islamabad or Centaurus Mall",
                key="nominatim_search_input",
            )
        with col_g2:
            if st.button("Geocode ➔", key="btn_geocode_nominatim", type="secondary", use_container_width=True):
                if geo_input and geo_input.strip():
                    new_lat, new_lon, display_label = geocode_with_nominatim(geo_input.strip())
                    st.session_state.user_lat = new_lat
                    st.session_state.user_lon = new_lon
                    st.session_state.current_location = geo_input.strip()
                    st.session_state.last_geocoded_loc = geo_input.strip()
                    st.toast(f"📍 Relocated to: {geo_input.strip()} ({new_lat:.4f}, {new_lon:.4f})")
                    st.rerun()

        # Quick location buttons
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            if st.button("F-8 Markaz", key="btn_q_f8", type="secondary", use_container_width=True):
                st.session_state.current_location = "F-8 Markaz, Islamabad"
                st.session_state.user_lat, st.session_state.user_lon, _ = geocode_with_nominatim("F-8 Markaz, Islamabad")
                st.rerun()
        with col_q2:
            if st.button("Blue Area", key="btn_q_blue", type="secondary", use_container_width=True):
                st.session_state.current_location = "Blue Area, Islamabad"
                st.session_state.user_lat, st.session_state.user_lon, _ = geocode_with_nominatim("Blue Area, Islamabad")
                st.rerun()
        with col_q3:
            if st.button("Centaurus", key="btn_q_cent", type="secondary", use_container_width=True):
                st.session_state.current_location = "Centaurus Mall, Islamabad"
                st.session_state.user_lat, st.session_state.user_lon, _ = geocode_with_nominatim("Centaurus Mall, Islamabad")
                st.rerun()