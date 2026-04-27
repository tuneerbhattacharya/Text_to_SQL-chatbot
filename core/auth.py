import os
import streamlit as st
from supabase import create_client


def _get_secret(name: str):
    return os.getenv(name) or st.secrets.get(name, None)


def get_supabase_client():
    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_ANON_KEY")

    if not url or not key:
        st.error("Supabase credentials are missing. Set SUPABASE_URL and SUPABASE_ANON_KEY.")
        st.stop()

    return create_client(url, key)


def login_page():
    st.markdown("""
    <div style="max-width:760px;margin:3rem auto;padding:2rem;border-radius:24px;background:#0f172a;border:1px solid #334155;">
      <h1 style="color:white;margin-bottom:0.3rem;">🔐 AI Data Analyst SaaS</h1>
      <p style="color:#cbd5e1;">Login or create an account to access your analytics workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    supabase = get_supabase_client()
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            if not email or not password:
                st.error("Please enter both email and password.")
                return

            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state["user"] = result.user
                st.session_state["access_token"] = result.session.access_token
                st.success("Login successful.")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Create account"):
            if not email or not password:
                st.error("Please enter both email and password.")
                return

            try:
                supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.success("Account created. If email confirmation is enabled, check your inbox.")
            except Exception as e:
                st.error(f"Signup failed: {e}")


def require_login():
    if "user" not in st.session_state:
        login_page()
        st.stop()


def logout_button():
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()


def get_current_user_email():
    user = st.session_state.get("user")
    return user.email if user else None
