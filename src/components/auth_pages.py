import streamlit as st
from auth.session_manager import SessionManager
from config.app_config import APP_ICON, APP_NAME, APP_TAGLINE, APP_DESCRIPTION
from utils.validators import validate_signup_fields
import time

def _inject_auth_styles():
    """Inject premium auth-page-specific styles."""
    st.markdown("""
    <style>
        /* ===== AUTH PAGE — Premium Split-Screen ===== */

        @keyframes floatOrb {
            0%   { transform: translate(0, 0) scale(1); }
            33%  { transform: translate(30px, -30px) scale(1.1); }
            66%  { transform: translate(-20px, 20px) scale(0.95); }
            100% { transform: translate(0, 0) scale(1); }
        }

        @keyframes fadeSlideUp {
            0%   { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes shimmer {
            0%   { background-position: -200% center; }
            100% { background-position: 200% center; }
        }

        @keyframes pulseRing {
            0%   { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.4); }
            70%  { box-shadow: 0 0 0 15px rgba(56, 189, 248, 0); }
            100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
        }

        @keyframes gradientMove {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Hero brand section */
        .auth-hero-section {
            position: relative;
            padding: 2.5rem 2rem;
            border-radius: 24px;
            background: linear-gradient(160deg, rgba(56,189,248,0.12) 0%, rgba(99,102,241,0.12) 50%, rgba(6,182,212,0.08) 100%);
            border: 1px solid rgba(255,255,255,0.08);
            overflow: hidden;
            animation: fadeSlideUp 0.8s ease-out;
        }

        /* Floating decorative orbs */
        .auth-hero-section::before {
            content: "";
            position: absolute;
            top: -40px; right: -40px;
            width: 180px; height: 180px;
            background: radial-gradient(circle, rgba(56,189,248,0.25) 0%, transparent 70%);
            border-radius: 50%;
            animation: floatOrb 8s ease-in-out infinite;
            pointer-events: none;
        }
        .auth-hero-section::after {
            content: "";
            position: absolute;
            bottom: -30px; left: -30px;
            width: 140px; height: 140px;
            background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
            border-radius: 50%;
            animation: floatOrb 10s ease-in-out infinite reverse;
            pointer-events: none;
        }

        .auth-hero-logo {
            font-size: 3rem;
            margin-bottom: 0.25rem;
            display: inline-block;
            filter: drop-shadow(0 0 20px rgba(56,189,248,0.5));
        }

        .auth-hero-brand {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38bdf8, #818cf8, #06b6d4);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 3s linear infinite;
            margin-bottom: 0.5rem;
            line-height: 1.1;
        }

        .auth-hero-tagline {
            color: #e2e8f0 !important;
            font-size: 1.15rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .auth-hero-sub {
            color: #94a3b8 !important;
            font-size: 0.95rem;
            line-height: 1.6;
            max-width: 380px;
        }

        /* Feature pill — single self-contained row */
        .auth-feat {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.7rem 1rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 14px;
            margin-bottom: 0.6rem;
            transition: all 0.3s ease;
            cursor: default;
        }
        .auth-feat:hover {
            background: rgba(56,189,248,0.08);
            border-color: rgba(56,189,248,0.25);
            transform: translateX(6px);
        }
        .auth-feat-ico {
            width: 38px; height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            flex-shrink: 0;
        }
        .auth-feat-ico.c1 { background: rgba(56,189,248,0.15); }
        .auth-feat-ico.c2 { background: rgba(129,140,248,0.15); }
        .auth-feat-ico.c3 { background: rgba(6,182,212,0.15); }
        .auth-feat-ico.c4 { background: rgba(74,222,128,0.15); }

        .auth-feat-txt { color: #cbd5e1 !important; font-size: 0.88rem; font-weight: 500; line-height: 1.35; }
        .auth-feat-txt b { color: #f1f5f9 !important; font-weight: 700; }

        /* Form header */
        .auth-form-hdr {
            text-align: center;
            margin-bottom: 0.75rem;
            padding-top: 0.5rem;
        }
        .auth-form-hdr h2 {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #f8fafc !important;
            margin-bottom: 0.25rem !important;
        }
        .auth-form-hdr p {
            color: #94a3b8 !important;
            font-size: 0.92rem;
        }

        /* Trust badges */
        .auth-trust-row {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 1.25rem;
            flex-wrap: wrap;
        }
        .auth-trust-badge {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            color: #64748b !important;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .bdot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #22c55e;
            display: inline-block;
            animation: pulseRing 2s ease-out infinite;
        }

        /* Password requirements (signup) */
        .auth-pw-reqs {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-top: 0.25rem;
        }
        .auth-pw-reqs p {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
            margin-bottom: 0.3rem;
            font-weight: 600;
        }
        .auth-pw-reqs ul {
            margin: 0;
            padding-left: 1.2rem;
        }
        .auth-pw-reqs li {
            color: #64748b !important;
            font-size: 0.78rem;
            line-height: 1.6;
        }

        /* Auth toggle button override */
        .auth-toggle-wrap button {
            background: transparent !important;
            border: 1px dashed rgba(56,189,248,0.3) !important;
            color: #38bdf8 !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px;
            box-shadow: none !important;
        }
        .auth-toggle-wrap button:hover {
            background: rgba(56,189,248,0.08) !important;
            border-color: #38bdf8 !important;
        }

        /* Stat counters in hero */
        .auth-stats-row {
            display: flex;
            gap: 1.5rem;
            margin-top: 1.75rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.06);
        }
        .auth-stat {
            text-align: center;
            flex: 1;
        }
        .auth-stat-num {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }
        .auth-stat-lbl {
            color: #64748b !important;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.15rem;
        }

    </style>
    """, unsafe_allow_html=True)


def show_login_page():
    # IMPORTANT: Initialize form_type immediately
    if 'form_type' not in st.session_state:
        st.session_state['form_type'] = 'login'

    current_form = st.session_state['form_type']

    # Inject auth-specific premium styles
    _inject_auth_styles()

    # ── Split-screen layout: Hero | Form ──
    hero_col, form_col = st.columns([1.1, 1], gap="large")

    # ── LEFT: Animated hero / brand section ──
    with hero_col:
        # Top branding block
        st.markdown(f"""<div class="auth-hero-section"><div class="auth-hero-logo">🩺</div><div class="auth-hero-brand">{APP_NAME}</div><div class="auth-hero-tagline">{APP_DESCRIPTION}</div><div class="auth-hero-sub">{APP_TAGLINE} — powered by clinical-grade AI that turns complex medical data into clear, actionable insights.</div></div>""", unsafe_allow_html=True)

        # Feature items — each as its own st.markdown to avoid nested-div rendering bugs
        st.markdown("", unsafe_allow_html=True)  # spacer

        st.markdown("""<div class="auth-feat"><div class="auth-feat-ico c1">🩸</div><div class="auth-feat-txt"><b>Blood Work Analysis</b> — CBC, Lipids, Metabolic panels decoded instantly</div></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="auth-feat"><div class="auth-feat-ico c2">📑</div><div class="auth-feat-txt"><b>Radiology Reports</b> — MRI, CT, X-Ray findings in plain English</div></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="auth-feat"><div class="auth-feat-ico c3">🧠</div><div class="auth-feat-txt"><b>AI Health Score</b> — Personalized 0-100 wellness scoring</div></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="auth-feat"><div class="auth-feat-ico c4">🛡️</div><div class="auth-feat-txt"><b>Private & Secure</b> — End-to-end encrypted, HIPAA-aligned</div></div>""", unsafe_allow_html=True)

        # Stats row
        st.markdown("""<div class="auth-stats-row"><div class="auth-stat"><div class="auth-stat-num">50+</div><div class="auth-stat-lbl">Biomarkers</div></div><div class="auth-stat"><div class="auth-stat-num">99%</div><div class="auth-stat-lbl">Accuracy</div></div><div class="auth-stat"><div class="auth-stat-num">10s</div><div class="auth-stat-lbl">Avg Analysis</div></div></div>""", unsafe_allow_html=True)


    # ── RIGHT: Auth form card ──
    with form_col:
        if current_form == 'login':
            greeting = "Welcome Back!"
            subtext = "Sign in to access your health dashboard"
        else:
            greeting = "Create Account"
            subtext = "Start your journey to better health insights"

        st.markdown(f"""<div class="auth-form-hdr"><h2>{greeting}</h2><p>{subtext}</p></div>""", unsafe_allow_html=True)

        if current_form == 'login':
            show_login_form()
        else:
            show_signup_form()

        # Toggle between login / signup
        st.markdown("<div class='auth-toggle-wrap'>", unsafe_allow_html=True)
        toggle_text = "Don't have an account? Sign up" if current_form == 'login' else "Already have an account? Login"
        if st.button(toggle_text, use_container_width=True, key="toggle_auth"):
            st.session_state['form_type'] = 'signup' if current_form == 'login' else 'login'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Trust badges
        st.markdown("""<div class="auth-trust-row"><div class="auth-trust-badge"><span class="bdot"></span> Encrypted</div><div class="auth-trust-badge"><span class="bdot"></span> HIPAA Aligned</div><div class="auth-trust-badge"><span class="bdot"></span> No Data Stored</div></div>""", unsafe_allow_html=True)


def show_login_form():
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

    if submitted:
        if email and password:
            with st.status("Verifying credentials...") as status:
                success, result = SessionManager.login(email, password)
                if success:
                    status.update(label="Login successful! Redirecting...", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label=result, state="error")
        else:
            st.error("Please enter both email and password")

def show_signup_form():
    with st.form("signup_form", clear_on_submit=False):
        new_name = st.text_input("Full Name", key="signup_name", placeholder="John Doe")
        new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_password2", placeholder="Repeat your password")

        st.markdown("""<div class="auth-pw-reqs"><p>Password requirements</p><ul><li>At least 8 characters</li><li>One uppercase letter</li><li>One lowercase letter</li><li>One number</li></ul></div>""", unsafe_allow_html=True)

        submitted = st.form_submit_button("Create Account →", use_container_width=True, type="primary")

    if submitted:
        validation_result = validate_signup_fields(
            new_name, new_email, new_password, confirm_password
        )

        if not validation_result[0]:
            st.error(validation_result[1])
            return

        with st.status("Creating your account...") as status:
            success, response = st.session_state.auth_service.sign_up(
                new_email, new_password, new_name
            )
            if success:
                # Update session manually to ensure immediate redirect
                st.session_state.authenticated = True
                st.session_state.user = response
                status.update(label="Account created successfully! Redirecting...", state="complete", expanded=False)
                st.rerun()
            else:
                status.update(label=response, state="error")
