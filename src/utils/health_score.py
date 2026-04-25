import re
import streamlit as st

def extract_health_score(text):
    """Extract health score from text using regex."""
    if not text:
        return None
        
    # Look for "Health Score: XX" or "**Health Score**: XX" or similar
    patterns = [
        r"(?:Health Score|health score)[:\s*]+(\d+)",
        r"\*\*Health Score\*\*[:\s]+(\d+)",
        r"Health Score\s*=\s*(\d+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                score = int(match.group(1))
                if 0 <= score <= 100:
                    return score
            except ValueError:
                continue
                
    return None

def get_latest_health_score():
    """Fetch all sessions and calculate the latest health score."""
    if not st.session_state.get('user'):
        return None
        
    auth_service = st.session_state.auth_service
    user_id = st.session_state.user['id']
    
    # 1. Get all sessions for the user
    success, sessions = auth_service.get_user_sessions(user_id)
    if not success or not sessions:
        return None
        
    # 2. Iterate through sessions (starting from newest) to find a score
    # We only look at the first few sessions for performance
    for session in sessions[:10]:
        success, messages = auth_service.get_session_messages(session['id'])
        if success and messages:
            # Look at assistant messages in reverse order
            for msg in reversed(messages):
                if msg.get('role') == 'assistant':
                    score = extract_health_score(msg.get('content', ''))
                    if score is not None:
                        return score
                        
    return None

def get_health_score_trend():
    """Get health score trend from multiple sessions."""
    if not st.session_state.get('user'):
        return []
        
    auth_service = st.session_state.auth_service
    user_id = st.session_state.user['id']
    
    success, sessions = auth_service.get_user_sessions(user_id)
    if not success or not sessions:
        return []
        
    history = []
    # Limit to last 5 sessions with scores
    for session in sessions[:10]:
        success, messages = auth_service.get_session_messages(session['id'])
        if success and messages:
            for msg in reversed(messages):
                if msg.get('role') == 'assistant':
                    score = extract_health_score(msg.get('content', ''))
                    if score is not None:
                        history.append({
                            "date": session.get('created_at', ''),
                            "score": score,
                            "title": session.get('title', 'Analysis')
                        })
                        break
        if len(history) >= 5:
            break
            
    return list(reversed(history))
