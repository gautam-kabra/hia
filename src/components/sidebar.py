import streamlit as st
from auth.session_manager import SessionManager
from components.footer import show_footer

def show_sidebar():
    with st.sidebar:
        # Profile Header
        if st.session_state.user:
            display_name = st.session_state.user.get("name") or st.session_state.user.get("email", "").split("@")[0]
            display_name = display_name[:15] + "..." if len(display_name) > 15 else display_name
            initials = display_name[0].upper() if display_name else "U"
            
            st.markdown(
                f"""
                <div class="profile-header">
                    <div class="profile-avatar">{initials}</div>
                    <div style="flex: 1; overflow: hidden;">
                        <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{display_name}</div>
                        <div style="color: #38bdf8; font-size: 0.8rem; font-weight: 600; display: inline-block; background: rgba(56, 189, 248, 0.1); padding: 2px 8px; border-radius: 99px; margin-top: 2px;">Pro Member</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.title("💬 Chat Sessions")
        
        if st.button("+ New Analysis Session", use_container_width=True):
            if st.session_state.user and 'id' in st.session_state.user:
                success, session = SessionManager.create_chat_session()
                if success:
                    st.session_state.current_session = session
                    st.rerun()
                else:
                    st.error("Failed to create session")
            else:
                st.error("Please log in again")
                SessionManager.logout()
                st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        show_session_list()
        
        # Logout button
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True, type="secondary"):
            SessionManager.logout()
            st.rerun()
        
        # Add footer to sidebar
        show_footer(in_sidebar=True)

def show_session_list():
    if st.session_state.user and 'id' in st.session_state.user:
        success, sessions = SessionManager.get_user_sessions()
        if success:
            if sessions:
                st.markdown("<h4 style='color: #f8fafc; font-size: 1rem; margin-bottom: 1rem;'>Previous Sessions</h4>", unsafe_allow_html=True)
                render_session_list(sessions)
            else:
                # Beautiful Empty State
                st.markdown(
                    """
                    <div style="text-align: center; padding: 2rem 1rem; color: #475569; opacity: 0.7;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                        <h4 style="color: #94a3b8; font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;">No History Yet</h4>
                        <p style="font-size: 0.8rem; line-height: 1.4;">Your medical analysis sessions will safely securely appear here.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def render_session_list(sessions):
    # Store deletion state
    if 'delete_confirmation' not in st.session_state:
        st.session_state.delete_confirmation = None
    
    for session in sessions:
        render_session_item(session)

def render_session_item(session):
    if not session or not isinstance(session, dict) or 'id' not in session:
        return
        
    session_id = session['id']
    title_lower = session['title'].lower()
    
    # Dynamic Icons based on title heuristics
    icon = "📝"
    if "blood" in title_lower or "cbc" in title_lower:
        icon = "🩸"
    elif "radio" in title_lower or "x-ray" in title_lower or "scan" in title_lower:
        icon = "📑"
    elif "well" in title_lower or "diet" in title_lower:
        icon = "🧘"
    elif "heart" in title_lower or "cardio" in title_lower:
        icon = "🫀"
    elif "lung" in title_lower or "resp" in title_lower:
        icon = "🫁"
        
    current_session = st.session_state.get('current_session', {})
    current_session_id = current_session.get('id') if isinstance(current_session, dict) else None
    
    # Create container for each session
    with st.container():
        # Session title and delete button side by side
        title_col, delete_col = st.columns([4.5, 1], gap="small", vertical_alignment="center")
        
        with title_col:
            is_active = current_session_id == session_id
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {session['title']}", key=f"session_{session_id}", use_container_width=True, type=btn_type):
                st.session_state.current_session = session
                st.rerun()
        
        with delete_col:
            if st.button("🗑️", key=f"delete_{session_id}", help="Delete this session", type="secondary"):
                if st.session_state.delete_confirmation == session_id:
                    st.session_state.delete_confirmation = None
                else:
                    st.session_state.delete_confirmation = session_id
                st.rerun()
        
        # Show confirmation below if this session is being deleted
        if st.session_state.delete_confirmation == session_id:
            st.warning("Delete above session?")
            left_btn, right_btn = st.columns(2)
            with left_btn:
                if st.button("Yes", key=f"confirm_delete_{session_id}", type="primary", use_container_width=True):
                    handle_delete_confirmation(session_id, current_session_id)
            with right_btn:
                if st.button("No", key=f"cancel_delete_{session_id}", use_container_width=True):
                    st.session_state.delete_confirmation = None
                    st.rerun()

def handle_delete_confirmation(session_id, current_session_id):
    if not session_id:
        st.error("Invalid session")
        return
        
    success, error = SessionManager.delete_session(session_id)
    if success:
        st.session_state.delete_confirmation = None
        # Clear current session if it was deleted
        if current_session_id and current_session_id == session_id:
            st.session_state.current_session = None
        st.rerun()
    else:
        st.error(f"Failed to delete: {error}")
