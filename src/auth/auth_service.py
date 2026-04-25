import streamlit as st
from supabase import create_client
from clerk_backend_api import Clerk
from datetime import datetime
import re


class AuthService:
    def __init__(self):
        try:
            # Initialize Supabase client for database operations
            self.supabase = create_client(
                st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
            )
            # Initialize Clerk client for authentication
            self.clerk = Clerk(
                bearer_auth=st.secrets["CLERK_SECRET_KEY"]
            )
        except Exception as e:
            st.error(f"Failed to initialize services: {str(e)}")
            raise e

        # Try to restore session from storage
        self.try_restore_session()

        # Validate session on initialization
        if "auth_token" in st.session_state:
            if not self.validate_session_token():
                pass

    def try_restore_session(self):
        """Try to restore session from persistent storage."""
        try:
            # Check if we have a Clerk user ID in session state
            if "clerk_user_id" in st.session_state:
                # Verify the user still exists in Clerk
                try:
                    user = self.clerk.users.get(user_id=st.session_state.clerk_user_id)
                    if user:
                        # Get user data from Supabase
                        user_data = self.get_user_data(user.id)
                        if user_data:
                            st.session_state.user = user_data
                            # Set a dummy token if not present
                            if "auth_token" not in st.session_state:
                                st.session_state.auth_token = "restored"
                            if "clerk_token" not in st.session_state:
                                st.session_state.clerk_token = "restored"
                            return True
                except Exception:
                    # User invalid, clear IDs
                    if "clerk_user_id" in st.session_state:
                        del st.session_state.clerk_user_id
                    if "clerk_token" in st.session_state:
                        del st.session_state.clerk_token
                    if "auth_token" in st.session_state:
                        del st.session_state.auth_token
            return False
        except Exception:
            return False

    def validate_email(self, email):
        """Validate email format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    def check_existing_user(self, email):
        """Check if user already exists in Supabase."""
        try:
            result = (
                self.supabase.table("users").select("id").eq("email", email).execute()
            )
            return len(result.data) > 0
        except Exception:
            return False

    def sign_up(self, email, password, name):
        try:
            # Generate a username from email (Clerk requires it)
            import random
            import string
            base = email.split('@')[0].lower()
            # Keep only alphanumeric and hyphens/underscores
            base = ''.join(c for c in base if c.isalnum() or c in ['_', '-'])
            if not base:
                base = 'user'
            # Append random suffix to avoid collisions
            suffix = ''.join(random.choices(string.digits, k=4))
            username = f"{base}_{suffix}"

            # Create user in Clerk
            clerk_user = self.clerk.users.create(
                email_address=[email],
                password=password,
                first_name=name,
                last_name="",
                username=username,
                skip_user_requirement=True  # Bypass strict requirement checks
            )

            if not clerk_user or not clerk_user.id:
                return False, "Failed to create user account in Clerk"

            # Create user record in Supabase
            user_data = {
                "id": clerk_user.id,
                "email": email,
                "name": name,
                "created_at": datetime.now().isoformat(),
            }

            try:
                insert_result = self.supabase.table("users").insert(user_data).execute()
                if not insert_result or not insert_result.data:
                    st.error("Supabase insert succeeded but returned no data")
            except Exception as insert_error:
                st.error(f"Supabase insert failed: {insert_error}")
                import traceback
                st.error(traceback.format_exc())
                raise insert_error

            # Store session info (dummy token since we're server-side)
            st.session_state.clerk_token = "dummy"
            st.session_state.clerk_user_id = clerk_user.id
            st.session_state.auth_token = "dummy"
            st.session_state.user = user_data

            return True, user_data

        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate" in error_msg or "already registered" in error_msg or "exists" in error_msg:
                return False, "Email already registered"
            return False, f"Sign up failed: {str(e)}"

    def sign_in(self, email, password):
        try:
            # Clear any existing session data first
            for key in ["clerk_token", "clerk_user_id", "auth_token", "user"]:
                if key in st.session_state:
                    del st.session_state[key]

            # Find user by email in Clerk
            users = self.clerk.users.list(
                request={"email_address": [email], "limit": 1}
            )
            if not users:
                return False, "Invalid credentials"

            clerk_user = users[0]

            # Verify password using Clerk's verify_password endpoint
            verify_resp = self.clerk.users.verify_password(
                user_id=clerk_user.id,
                password=password
            )
            # verify_password returns an object; check if verification succeeded
            if not verify_resp:
                return False, "Invalid credentials"

            # Get user data from Supabase using email (more reliable than ID lookup)
            user_data = self.get_user_data_by_email(email)
            if not user_data:
                # If not found, try to get from Clerk and create in Supabase
                user_data = {
                    "id": clerk_user.id,
                    "email": email,
                    "name": f"{clerk_user.first_name or ''} {clerk_user.last_name or ''}".strip(),
                    "created_at": datetime.now().isoformat(),
                }
                try:
                    self.supabase.table("users").insert(user_data).execute()
                except Exception as insert_error:
                    st.error(f"Failed to create user record: {insert_error}")
                    return False, "User exists in Clerk but database setup failed"

            # Store session info
            st.session_state.clerk_token = "dummy"
            st.session_state.clerk_user_id = clerk_user.id
            st.session_state.auth_token = "dummy"
            st.session_state.user = user_data

            return True, user_data

        except Exception as e:
            error_msg = str(e).lower()
            if "incorrect_password" in error_msg or "incorrect password" in error_msg:
                return False, "Invalid credentials"
            return False, str(e)

    def sign_out(self):
        """Sign out user and clear all session data."""
        for key in ["clerk_token", "clerk_user_id", "auth_token", "user"]:
            if key in st.session_state:
                del st.session_state[key]

        try:
            from auth.session_manager import SessionManager
            SessionManager.clear_session_state()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_user(self):
        try:
            if "clerk_user_id" in st.session_state:
                return self.clerk.users.get(user_id=st.session_state.clerk_user_id)
            return None
        except Exception:
            return None

    def create_session(self, user_id, title=None):
        try:
            current_time = datetime.now()
            default_title = f"{current_time.strftime('%d-%m-%Y')} | {current_time.strftime('%H:%M:%S')}"

            session_data = {
                "user_id": user_id,
                "title": title or default_title,
                "created_at": current_time.isoformat(),
            }
            result = self.supabase.table("chat_sessions").insert(session_data).execute()
            return True, result.data[0] if result.data else None
        except Exception as e:
            return False, str(e)

    def get_user_sessions(self, user_id):
        try:
            result = (
                self.supabase.table("chat_sessions")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return True, result.data
        except Exception as e:
            st.error(f"Error fetching sessions: {str(e)}")
            return False, []

    def save_chat_message(self, session_id, content, role="user"):
        try:
            message_data = {
                "session_id": session_id,
                "content": content,
                "role": role,
                "created_at": datetime.now().isoformat(),
            }
            result = self.supabase.table("chat_messages").insert(message_data).execute()
            return True, result.data[0] if result.data else None
        except Exception as e:
            return False, str(e)

    def get_session_messages(self, session_id):
        try:
            result = (
                self.supabase.table("chat_messages")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at")
                .execute()
            )
            return True, result.data
        except Exception as e:
            return False, str(e)

    def delete_session(self, session_id):
        try:
            self.supabase.table("chat_messages").delete().eq(
                "session_id", session_id
            ).execute()

            self.supabase.table("chat_sessions").delete().eq("id", session_id).execute()

            return True, None
        except Exception as e:
            st.error(f"Failed to delete session: {str(e)}")
            return False, str(e)

    def validate_session_token(self):
        """Validate existing session token on startup."""
        try:
            if "clerk_user_id" not in st.session_state:
                return None

            # Verify with Clerk that the user still exists
            user = self.clerk.users.get(user_id=st.session_state.clerk_user_id)
            if not user:
                return None

            # Get user data from Supabase
            return self.get_user_data(user.id)
        except Exception:
            return None

    def get_user_data(self, user_id):
        """Get user data from Supabase database by user ID."""
        try:
            response = (
                self.supabase.table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )
            return response.data if response else None
        except Exception:
            return None

    def get_user_data_by_email(self, email):
        """Get user data from Supabase database by email."""
        try:
            response = (
                self.supabase.table("users")
                .select("*")
                .eq("email", email)
                .single()
                .execute()
            )
            return response.data if response else None
        except Exception:
            return None
