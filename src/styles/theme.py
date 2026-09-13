import streamlit as st


def apply_theme():
    """Injects a world-class, professional dark mobile design system inspired by iOS 18 and Tailwind CSS."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* ---------- Universal Typography ---------- */
        html, body, [class*="css"], .stApp, p, h1, h2, h3, h4, h5, h6, input, button, select, textarea, label {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        *, *::before, *::after {
            box-sizing: border-box;
        }

        /* Preserve Streamlit / Material Symbols / FontAwesome Icons */
        [data-testid="stIcon"],
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpander"] summary svg,
        [data-testid="stExpander"] summary span,
        .material-symbols-rounded,
        .material-symbols-outlined,
        .material-symbols-sharp,
        i[class*="fa-"],
        .fa {
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons', 'FontAwesome', sans-serif !important;
        }

        /* Streamlit Expander styling */
        [data-testid="stExpander"] {
            background: #111827 !important;
            border: 1px solid rgba(59, 130, 246, 0.28) !important;
            border-radius: 16px !important;
            margin-top: 8px !important;
            margin-bottom: 12px !important;
            overflow: hidden !important;
        }
        [data-testid="stExpander"] summary {
            padding: 10px 14px !important;
            color: #cbd5e1 !important;
            font-weight: 700 !important;
            font-size: 12.5px !important;
        }
        [data-testid="stExpander"] summary:hover {
            color: #ffffff !important;
            background: rgba(30, 41, 59, 0.4) !important;
        }
        [data-testid="stExpanderDetails"] {
            padding: 12px 14px !important;
            background: #0f172a !important;
            border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
        }

        /* ---------- App Canvas Background ---------- */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #172554 0%, #030712 60%, #02040a 100%) !important;
            color: #f8fafc !important;
        }

        /* Center container in browser viewport */
        [data-testid="stAppViewContainer"] {
            display: flex;
            justify-content: center;
            background-color: #02040a;
        }

        /* ---------- Sleek Mobile Device Mockup Frame ---------- */
        [data-testid="stMainBlockContainer"] {
            max-width: 480px !important;
            min-height: 840px !important;
            padding: 1.2rem 1.2rem 2.2rem 1.2rem !important;
            margin: 1.5rem auto !important;
            background: #0b0f19 !important;
            border-radius: 42px !important;
            box-shadow: 
                0 0 0 1px rgba(255, 255, 255, 0.12),
                0 0 0 8px #1e293b,
                0 25px 50px -12px rgba(0, 0, 0, 0.9),
                0 0 50px rgba(37, 99, 235, 0.18) !important;
            position: relative;
            overflow-x: hidden;
            overflow-y: visible;
        }

        /* Seamless Edge-to-Edge on Mobile Devices */
        @media (max-width: 640px) {
            [data-testid="stMainBlockContainer"] {
                max-width: 100% !important;
                min-height: 100vh !important;
                margin: 0 !important;
                border-radius: 0px !important;
                box-shadow: none !important;
                border: none !important;
                padding: 1rem 0.9rem 4.5rem 0.9rem !important;
            }
        }

        /* Hide Streamlit default clutter */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ---------- Professional Cards & Surfaces ---------- */
        .startup-card {
            background: linear-gradient(145deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .startup-card:hover {
            border-color: rgba(59, 130, 246, 0.35);
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(37, 99, 235, 0.15);
        }

        .highlight-card {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.18) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(59, 130, 246, 0.4);
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
        }

        .modal-card {
            background: #111827;
            border: 1.5px solid #3b82f6;
            border-radius: 22px;
            padding: 18px;
            margin: 14px 0;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7), 0 0 30px rgba(37, 99, 235, 0.25);
            animation: slideUp 0.25s ease-out;
        }
        @keyframes slideUp {
            from { transform: translateY(10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* ---------- Modern Badges & Status Chips ---------- */
        .badge-completed {
            color: #34d399;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .badge-pending {
            color: #fbbf24;
            background: rgba(245, 158, 11, 0.14);
            border: 1px solid rgba(245, 158, 11, 0.35);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
        }
        .badge-active {
            color: #60a5fa;
            background: rgba(37, 99, 235, 0.18);
            border: 1px solid rgba(59, 130, 246, 0.4);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
        }
        .badge-tag {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(30, 64, 175, 0.25) 100%);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }
        .badge-verified {
            color: #38bdf8;
            font-size: 13px;
        }

        /* Pulse Dot for Live GPS / Online Providers */
        .pulse-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulseDot 1.8s infinite;
            margin-right: 6px;
        }
        @keyframes pulseDot {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* ---------- Avatars ---------- */
        .avatar-circle {
            min-width: 52px;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 18px;
            color: white;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.15);
        }

        /* ---------- Buttons Styling ---------- */
        .stButton > button {
            width: 100%;
            border: none;
            padding: 8px 10px !important;
            font-weight: 700;
            font-size: 12.5px !important;
            border-radius: 14px;
            transition: all 0.2s ease-in-out;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.2;
            letter-spacing: -0.2px;
        }
        .stButton > button p,
        .stButton > button div,
        .stButton > button span {
            white-space: nowrap !important;
            text-overflow: clip !important;
            overflow: visible !important;
            font-size: inherit !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        [data-testid="stMarkdownContainer"] p {
            white-space: normal !important;
            word-break: normal !important;
            overflow-wrap: break-word !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.6);
            transform: translateY(-1px);
        }
        .stButton > button[kind="secondary"] {
            background: #111827;
            color: #e2e8f0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton > button[kind="secondary"]:hover {
            background: #1e293b;
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-1px);
        }

        /* Danger Logout Button */
        #logout-marker + div .stButton > button {
            background: rgba(239, 68, 68, 0.14) !important;
            color: #f87171 !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            box-shadow: none !important;
        }
        #logout-marker + div .stButton > button:hover {
            background: rgba(239, 68, 68, 0.25) !important;
            color: #fca5a5 !important;
        }

        /* Bottom Navigation Bar Anchor & Auto-push to bottom */
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor),
        div.element-container:has(#bottom-nav-anchor),
        div:has(> div > div > #bottom-nav-anchor),
        div:has(#nav-marker) {
            margin-top: auto !important;
            height: 0px !important;
            min-height: 0px !important;
            padding: 0 !important;
            margin-bottom: 0 !important;
        }

        /* Bottom Floating Dock Navigation Row */
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div,
        div.element-container:has(#bottom-nav-anchor) + div,
        div:has(#nav-marker) + div {
            position: sticky !important;
            bottom: 0px !important;
            z-index: 9999 !important;
            background: rgba(11, 15, 25, 0.95) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            padding: 10px 4px 6px 4px !important;
            margin-top: 18px !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 18px 18px 0 0 !important;
            box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.5) !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div [data-testid="column"],
        div.element-container:has(#bottom-nav-anchor) + div [data-testid="column"],
        div:has(#nav-marker) + div [data-testid="column"] {
            padding: 0 2px !important;
            min-width: 0 !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button,
        div.element-container:has(#bottom-nav-anchor) + div .stButton > button,
        div:has(#nav-marker) + div .stButton > button {
            background: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: none !important;
            color: #94a3b8 !important;
            font-size: 11.5px !important;
            font-weight: 700 !important;
            padding: 9px 2px !important;
            margin: 0 !important;
            border-radius: 12px !important;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            letter-spacing: -0.2px !important;
            line-height: 1.2 !important;
            min-height: 42px !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button p,
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button span,
        div.element-container:has(#bottom-nav-anchor) + div .stButton > button p,
        div:has(#nav-marker) + div .stButton > button p {
            font-size: 11.5px !important;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            letter-spacing: -0.2px !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button:hover,
        div:has(#nav-marker) + div .stButton > button:hover {
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.1) !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button[kind="primary"],
        div:has(#nav-marker) + div .stButton > button[kind="primary"] {
            color: #ffffff !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            border: 1px solid rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.45) !important;
        }
        div[data-testid="stElementContainer"]:has(#bottom-nav-anchor) + div .stButton > button[kind="primary"] p,
        div:has(#nav-marker) + div .stButton > button[kind="primary"] span {
            color: #ffffff !important;
        }

        /* Inputs & Textareas */
        .stTextInput > div > div > input, .stNumberInput > div > div > input {
            background-color: #111827 !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px !important;
            padding: 12px 16px !important;
            font-size: 13px !important;
        }
        .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
        }

        /* Chat bubbles */
        [data-testid="stChatMessage"] {
            background: #111827;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 12px 16px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        [data-testid="stChatInput"] textarea {
            background-color: #111827 !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 24px !important;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: #0b0f19;
            padding: 6px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            border-radius: 10px;
            color: #64748b;
            font-weight: 700;
            font-size: 13px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e293b !important;
            color: #60a5fa !important;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
            color: #f8fafc !important;
            font-weight: 800;
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.8rem !important;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
