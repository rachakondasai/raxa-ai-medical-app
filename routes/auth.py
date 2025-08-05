import streamlit as st

# For testing — store valid creds here
valid_users = {
    "sai": "admin123",
    "lasya.priya": "admin123",
    "vamsi.krishna": "admin123"
}

def show_login():
    st.subheader("Login ↩️")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in valid_users and valid_users[username] == password:
            st.success("Login successful ✅")
            st.session_state.authenticated = True
            st.session_state.user_id = username
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

def show_signup():
    st.subheader("Sign Up 📝")
    st.info("Signup is demo only. Use 'sai', 'lasya.priya', or 'vamsi.krishna' with password 'admin123'")
