import streamlit as st
import base64
from pathlib import Path

def inject_custom_theme():
    """Injects high-end, futuristic dark glassmorphism CSS with Aurora effects and animations."""
    css = """
    <style>
        /* Google Fonts & Base Formatting */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        div[data-testid="InputInstructions"] > span:nth-child(1) {
            visibility: hidden;
        }
        
        header[data-testid="stHeader"] {
            background: transparent !important;
            border-bottom: none !important;
        }

        /* Hide the right-side toolbar (menu, status, etc.) */
        div[data-testid="stStatusWidget"], 
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Permanently disable sidebar collapsing by hiding all toggle buttons */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        button[aria-label="Close sidebar"],
        button[aria-label="Open sidebar"] {
            display: none !important;
        }

        [data-testid="stAppViewBlockContainer"] {
            padding-top: 2rem !important; 
        }

        /* --------------------------------- */
        /* Core Animations & Dynamic FX      */
        /* --------------------------------- */
        
        @keyframes entranceFadeSlide {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes auroraShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 10px rgba(56, 189, 248, 0.2); }
            50% { box-shadow: 0 0 25px rgba(56, 189, 248, 0.5); }
            100% { box-shadow: 0 0 10px rgba(56, 189, 248, 0.2); }
        }

        /* Entrance Animation for Main App */
        .main .block-container {
            animation: entranceFadeSlide 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }

        /* --------------------------------- */
        /* Background & Glass Containers     */
        /* --------------------------------- */
    """

    # Load and encode background image
    try:
        bg_path = Path("src/assets/bg.png")
        if bg_path.exists():
            with open(bg_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            css += f"""
            .stApp {{
                background-color: #0f172a;
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                position: relative;
                z-index: 0;
            }}
            
            /* Dynamic Aurora Overlay */
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(
                    120deg, 
                    rgba(56, 189, 248, 0.15) 0%, 
                    rgba(129, 140, 248, 0.15) 50%, 
                    rgba(6, 182, 212, 0.15) 100%
                );
                background-size: 200% 200%;
                animation: auroraShift 15s ease infinite;
                z-index: -1;
                pointer-events: none;
            }}
            
            .main .block-container {{
                background: rgba(15, 23, 42, 0.65);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 2rem 3rem 3rem 3rem !important;
                margin-top: 2rem !important;
                margin-bottom: 3rem;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                max-width: 65rem;
            }}
            """
    except Exception as e:
        pass

    css += """
        /* --------------------------------- */
        /* Custom Launchpad & Dashboard FX   */
        /* --------------------------------- */
        
        .launchpad-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: left;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            height: 100%;
            cursor: pointer;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .launchpad-card:hover {
            transform: translateY(-8px) scale(1.02);
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.7), 0 0 20px rgba(56, 189, 248, 0.15);
        }
        
        .launchpad-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            display: inline-block;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .launchpad-title {
            color: #ffffff;
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        .launchpad-desc {
            color: #94a3b8;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .how-it-works-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 3rem;
            text-align: center;
        }
        


        
        /* --------------------------------- */
        /* Universal Inputs & Buttons        */
        /* --------------------------------- */

        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            color: white !important;
            border: none !important;
            padding: 0.6rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 4px 15px -3px rgba(59, 130, 246, 0.4);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -5px rgba(59, 130, 246, 0.7);
            background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
        }
        
        /* Secondary / Secondary Buttons */
        .stButton>button[data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: none !important;
        }
        .stButton>button[data-testid="baseButton-secondary"]:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        
        .welcome-title {
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            line-height: 1.1;
        }
        
        /* --- Text Inputs --- */
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 0.75rem 1rem !important;
            transition: all 0.3s ease !important;
            outline: none !important;
        }
        
        /* Fix for the 'doubled border' glitch */
        .stTextInput>div>div>input:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
            outline: none !important;
        }

        /* Ensure the parent container doesn't show a secondary focus ring or border */
        .stTextInput [data-baseweb="input"] {
            border: none !important;
            background-color: transparent !important;
        }

        .stTextInput>div>div:focus-within {
            border-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
        }

        /* --- Selectbox (Gender, etc.) --- */
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            transition: all 0.3s ease !important;
            cursor: pointer;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3) !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
            color: white !important;
        }
        /* Selectbox dropdown arrow */
        [data-testid="stSelectbox"] svg {
            fill: #94a3b8 !important;
        }

        /* --- Number Input (Age, etc.) --- */
        [data-testid="stNumberInput"] input {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 0.75rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stNumberInput"] input:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3) !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
        /* Number input step buttons (+/-) */
        [data-testid="stNumberInput"] button {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #cbd5e1 !important;
        }
        [data-testid="stNumberInput"] button:hover {
            background-color: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(56, 189, 248, 0.4) !important;
            color: #38bdf8 !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
        }
        
        .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        .streamlit-expanderContent {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
            background-color: rgba(0, 0, 0, 0.2) !important;
        }
        
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px;
            backdrop-filter: blur(8px);
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }

        /* Avatar colors */
        [data-testid="chatAvatarIcon-user"] {
            background-color: #334155;
            color: #f8fafc;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background-color: #0369a1;
            color: #bae6fd;
        }

        /* Profile Header */
        .profile-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 1rem;
            background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1.5rem;
        }
        .profile-avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #38bdf8, #6366f1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: white;
            font-size: 1.2rem;
            box-shadow: 0 4px 10px rgba(56, 189, 248, 0.4);
        }
        
        p, span, div {
            color: #cbd5e1;
        }

        /* --------------------------------- */
        /* Sidebar Delete Button Fix         */
        /* --------------------------------- */

        /* Remove all internal gaps/padding from sidebar column containers */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 0.25rem !important;
        }

        /* Session row: strip wrapper margins for tight alignment */
        [data-testid="stSidebar"] [data-testid="column"] .stButton {
            margin: 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="column"] > div {
            padding: 0 !important;
        }

        /* Delete icon button — compact square */
        [data-testid="stSidebar"] [data-testid="column"]:last-child .stButton > button {
            padding: 0.4rem !important;
            min-height: unset !important;
            height: 100% !important;
            width: 100% !important;
            aspect-ratio: 1 / 1 !important;
            max-width: 42px !important;
            max-height: 42px !important;
            line-height: 1 !important;
            font-size: 1.1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 10px !important;
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: none !important;
            transition: all 0.25s ease !important;
        }
        [data-testid="stSidebar"] [data-testid="column"]:last-child .stButton > button:hover {
            background: rgba(248, 113, 113, 0.15) !important;
            border-color: rgba(248, 113, 113, 0.5) !important;
            transform: scale(1.05);
        }

        /* --------------------------------- */
        /* Auth Page — Form Glass Overrides  */
        /* --------------------------------- */

        /* Make the Streamlit form on auth pages borderless & transparent */
        .auth-form-card + div [data-testid="stForm"],
        [data-testid="stForm"] {
            transition: all 0.3s ease;
        }

        /* Labels on auth pages */
        .stTextInput label p {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            letter-spacing: 0.3px;
        }

        /* Placeholder text styling */
        .stTextInput>div>div>input::placeholder {
            color: #475569 !important;
            font-weight: 400 !important;
        }

        /* Primary button glow pulse on auth pages */
        .stButton>button[data-testid="baseButton-primary"] {
            position: relative;
            overflow: hidden;
            font-size: 0.95rem !important;
        }
        .stButton>button[data-testid="baseButton-primary"]::after {
            content: "";
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255,255,255,0.08) 50%,
                transparent 70%
            );
            transform: rotate(45deg);
            transition: all 0.5s ease;
        }
        .stButton>button[data-testid="baseButton-primary"]:hover::after {
            left: 100%;
        }

        /* --- Health Score Dashboard --- */
        .health-score-container {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            animation: entranceFadeSlide 0.8s ease-out;
            position: relative;
            overflow: hidden;
        }
        
        .health-score-container::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8);
            background-size: 200% 100%;
            animation: auroraShift 5s linear infinite;
        }

        .score-circle-outer {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin: 0 auto 1.5rem auto;
            display: flex;
            align-items: center;
            justify-content: center;
            background: conic-gradient(#38bdf8 var(--score-percent), rgba(255,255,255,0.05) 0);
            position: relative;
            transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.2);
        }
        
        .score-circle-inner {
            width: 125px;
            height: 125px;
            border-radius: 50%;
            background: #0f172a;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1;
        }

        .score-value {
            font-size: 3rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1;
        }
        
        .score-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 2px;
        }

        .health-status-badge {
            display: inline-block;
            padding: 0.4rem 1.2rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 700;
            margin-top: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-excellent { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
        .status-good { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
        .status-fair { background: rgba(234, 179, 8, 0.15); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.3); }
        .status-poor { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

        .health-insight-pill {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1.5rem;
            font-size: 0.95rem;
            color: #cbd5e1;
            text-align: left;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
