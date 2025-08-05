import streamlit as st
from routes.auth import show_login, show_signup
from routes.upload import show_upload
from routes.dashboard import show_dashboard
from utils import get_current_user

# App Branding
st.set_page_config(page_title="RaxaAI", page_icon="🩺")

# Init session variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "home"

if not st.session_state.authenticated:
    st.title("👋 Welcome to RaxaAI")
    st.subheader("Your personal AI assistant for smart medical analysis")
    st.image("static/logo.png", width=200)  # Optional logo
    st.write("Please login or sign up to continue")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.page = "signup"

    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "signup":
        show_signup()

else:
    user = get_current_user()
    consultant_map = {
        "vamsi.krishna": "Lasya Priya",
        "lasya.priya": "Vamsi Krishna",
        "sai": "Dr. Lasya Priya"
    }
    consultant = consultant_map.get(user, "")
    st.sidebar.success(f"Logged in as: {user}")
    page = st.sidebar.radio("Select a page:", ["📤 Upload", "📊 Dashboard"])

    if page == "📤 Upload":
        show_upload()
    elif page == "📊 Dashboard":
        show_dashboard(user, consultant)
