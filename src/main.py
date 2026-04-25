import streamlit as st
from auth.session_manager import SessionManager
from components.auth_pages import show_login_page
from components.sidebar import show_sidebar
from components.analysis_form import show_analysis_form
from components.footer import show_footer
from config.app_config import APP_NAME, APP_TAGLINE, APP_DESCRIPTION, APP_ICON
from services.ai_service import get_chat_response
from styles import inject_custom_theme
from utils.health_score import get_latest_health_score

# Must be the first Streamlit command
st.set_page_config(
    page_title="HIA - Health Insights Agent", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
SessionManager.init_session()
inject_custom_theme()

# Hide all Streamlit form-related elements
st.markdown(
    """
    <style>
        /* Hide form submission helper text */
        div[data-testid="InputInstructions"] > span:nth-child(1) {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar Toggle Logic Handled via CSS Reskinning in styles.py ---

def show_welcome_screen():
    st.markdown(
        f"""
        <div style='text-align: center; padding: 1rem 0 3rem 0;'>
            <div class="welcome-title">{APP_NAME}</div>
            <h3 style='color: #e2e8f0; font-weight: 500; font-size: 1.5rem; margin-bottom: 0.5rem;'>{APP_DESCRIPTION}</h3>
            <p style='color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;'>{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def trigger_new_session(specialty="comprehensive_analyst"):
        success, session = SessionManager.create_chat_session()
        if success:
            st.session_state.current_session = session
            st.rerun()
        else:
            st.error("Failed to create session")

    # Interactive Launchpad Cards
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
            """
            <div class="launchpad-card">
                <div>
                    <div class="launchpad-icon">🩸</div>
                    <div class="launchpad-title">Blood Insights</div>
                    <div class="launchpad-desc">Deep-dive into CBC, Liver panels, Lipids, and Metabolic markers to spot early trends.</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Analysis", key="btn_blood", use_container_width=True):
            trigger_new_session()

    with c2:
        st.markdown(
            """
            <div class="launchpad-card">
                <div>
                    <div class="launchpad-icon">📑</div>
                    <div class="launchpad-title">Radiology Summary</div>
                    <div class="launchpad-desc">Extract key findings from X-Ray, MRI, or CT Scan text reports into plain English.</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Analysis", key="btn_radio", use_container_width=True):
            trigger_new_session()

    with c3:
        st.markdown(
            """
            <div class="launchpad-card">
                <div>
                    <div class="launchpad-icon">🧘</div>
                    <div class="launchpad-title">Wellness Trends</div>
                    <div class="launchpad-desc">Upload clinical notes or wellness summaries for general lifestyle and dietary guidance.</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Analysis", key="btn_wellness", use_container_width=True):
            trigger_new_session()

    # --- Dynamic Health Score Dashboard ---
    health_score = get_latest_health_score()
    
    if health_score is not None:
        status_class = "status-excellent" if health_score >= 85 else "status-good" if health_score >= 70 else "status-fair" if health_score >= 50 else "status-poor"
        status_label = "Excellent" if health_score >= 85 else "Good" if health_score >= 70 else "Fair" if health_score >= 50 else "Needs Attention"
        
        st.markdown(
            f"""
            <div class="health-score-container">
                <h4 style="color: #f8fafc; margin-bottom: 1.5rem; font-weight: 700;">Your Current Health Status</h4>
                <div class="score-circle-outer" style="--score-percent: {health_score}%">
                    <div class="score-circle-inner">
                        <div class="score-value">{health_score}</div>
                        <div class="score-label">Score</div>
                    </div>
                </div>
                <div class="health-status-badge {status_class}">{status_label}</div>
                <div class="health-insight-pill">
                    <span style="color: #38bdf8; font-weight: 700;">💡 Pro Insight:</span> 
                    Based on your latest report, your biomarkers show a <b>{status_label.lower()}</b> trend. 
                    { "Continue with your current lifestyle and focus on preventive care." if health_score >= 70 else "Consider discussing the highlighted metabolic markers with your physician soon." }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Show a placeholder if no score is available yet
        st.markdown(
            """
            <div class="health-score-container" style="opacity: 0.7;">
                <h4 style="color: #f8fafc; margin-bottom: 1rem; font-weight: 700;">Health Score Snapshot</h4>
                <p style="color: #94a3b8; font-size: 0.95rem;">Upload your first report to unlock your personal health score and clinical trends dashboard.</p>
                <div style="font-size: 2rem; margin-top: 1rem;">🔒</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # "How it Works" Visuals
    st.markdown(
        """
        <div class="how-it-works-box">
            <h4 style="color: #38bdf8; margin-bottom: 2rem; font-weight: 700; letter-spacing: 0.5px;">How It Works</h4>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; max-width: 800px; margin: 0 auto; gap: 1rem;">
                <div style="flex: 1;">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">☁️</div>
                    <h5 style="color: #f8fafc; font-weight: 600; margin-bottom: 0.5rem;">1. Upload</h5>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Securely upload your medical report to our encrypted environment.</p>
                </div>
                <div style="color: #475569; font-size: 1.5rem; margin-top: 1rem; font-weight: 900;">➔</div>
                <div style="flex: 1;">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧠</div>
                    <h5 style="color: #f8fafc; font-weight: 600; margin-bottom: 0.5rem;">2. Process</h5>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Our clinical-grade AI analyzes the biomarkers and identifies patterns.</p>
                </div>
                <div style="color: #475569; font-size: 1.5rem; margin-top: 1rem; font-weight: 900;">➔</div>
                <div style="flex: 1;">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">💡</div>
                    <h5 style="color: #f8fafc; font-weight: 600; margin-bottom: 0.5rem;">3. Insight</h5>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Receive actionable plain-English recommendations based on your data.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def show_chat_history():
    success, messages = st.session_state.auth_service.get_session_messages(
        st.session_state.current_session["id"]
    )

    if success:
        for msg in messages:
            # Skip system messages (they contain report text metadata)
            if msg.get("role") == "system":
                continue
            if msg["role"] == "user":
                st.info(msg["content"])
            else:
                st.success(msg["content"])
        return messages
    return []


def handle_chat_input(messages):
    if prompt := st.chat_input("Ask a follow-up question about the report..."):
        # Display user message immediately
        st.info(prompt)

        # Save user message
        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"], prompt, role="user"
        )

        # Get context (report text)
        # We try to get it from session state first (for immediate use)
        context_text = st.session_state.get("current_report_text", "")

        # If not in session state, try to retrieve from stored system message
        if not context_text and messages:
            from services.ai_service import _extract_report_from_system_message
            for msg in messages:
                if msg.get("role") == "system":
                    extracted = _extract_report_from_system_message(
                        msg.get("content", "")
                    )
                    if extracted:
                        context_text = extracted
                        st.session_state.current_report_text = context_text
                        break

        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, context_text, messages)

            st.success(response)

            # Save AI response
            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], response, role="assistant"
            )
            # Rerun to update history display properly
            st.rerun()


def show_user_greeting():
    if st.session_state.user:
        display_name = st.session_state.user.get("name") or st.session_state.user.get(
            "email", ""
        )
        st.markdown(
            f"""
            <div style='text-align: right; padding: 1rem; color: #64B5F6; font-size: 1.1em;'>
                👋 Hi, {display_name}
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    SessionManager.init_session()

    if not SessionManager.is_authenticated():
        show_login_page()
        show_footer()
        return

    # Show sidebar
    show_sidebar()
    
    # Show user greeting at the top
    show_user_greeting()

    # Main chat area
    if st.session_state.get("current_session"):
        st.title(f"📊 {st.session_state.current_session['title']}")
        messages = show_chat_history()

        # If we have messages (meaning analysis is done), show chat input
        # Otherwise show analysis form
        if messages:
            with st.expander("New Analysis / Update Report", expanded=False):
                show_analysis_form()

            handle_chat_input(messages)
        else:
            show_analysis_form()
    else:
        show_welcome_screen()


if __name__ == "__main__":
    main()
