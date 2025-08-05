# components/dashboard.py

import streamlit as st

def show_dashboard(user, consultant):
    st.title("🩺 Medical Dashboard")
    
    st.markdown(f"### Welcome, **{consultant}** 👨‍⚕️")
    st.success(f"You're logged in as **{user}** and ready to analyze medical reports.")

    st.markdown("---")
    st.info("👉 Upload a new report from the left menu or view past reports here (feature coming soon).")

