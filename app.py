# app.py (Streamlit AI Medical App – Full Version)
import streamlit as st
import requests
import fitz  # PyMuPDF
import time
from serpapi import GoogleSearch
import os
from pathlib import Path
import json
import re
import subprocess

# --- File paths for persistent storage ---
USER_DB_FILE = "users.json"
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# --- Load/Save Users ---
def load_users():
    if Path(USER_DB_FILE).exists():
        return json.loads(Path(USER_DB_FILE).read_text())
    return {}

def save_users(users):
    Path(USER_DB_FILE).write_text(json.dumps(users))

# --- Signup/Login Page ---
def login_page():
    st.title("👤 Login / Signup")
    users = load_users()

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password.")

    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            if new_user in users:
                st.warning("Username already exists.")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Signup successful! Please login.")

# --- Extract Text from PDF ---
def extract_text_from_pdf(uploaded_file, max_pages=5):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc[:max_pages]:
        text += page.get_text()
    return text

# --- Advanced AI Diagnosis using LLM ---
def analyze_text_with_ai(text):
    prompt = f"""
You are a clinical AI assistant. Analyze the following medical report text deeply and list out any medical abnormalities or red flags found. Be specific and use medical terms. If normal, say so clearly.

{text}
"""
    try:
        result = subprocess.run(["ollama", "run", "llama3"], input=prompt.encode(), capture_output=True, timeout=60)
        return result.stdout.decode()
    except Exception as e:
        return f"AI analysis failed: {e}"

# --- IP-Based Location ---
def get_city_from_ip():
    try:
        res = requests.get("https://ipinfo.io", timeout=3)
        return res.json().get("city", "")
    except:
        return ""

# --- Search Doctors via SerpAPI ---
def search_doctors(city):
    params = {
        "engine": "google",
        "q": f"best doctors near {city}",
        "api_key": st.secrets["SERPAPI_KEY"]
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    doctors = []
    for result in results.get("organic_results", [])[:5]:
        doctors.append(f"- [{result['title']}]({result['link']})")
    return doctors

# --- Save Report for User ---
def save_report(user, text):
    report_path = REPORT_DIR / f"{user}_{int(time.time())}.txt"
    report_path.write_text(text)

# --- Main UI Page ---
def main_app():
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio("Select a page:", ["Upload", "Dashboard"])

    st.success(f"✅ Logged in as **{st.session_state.username}**")

    if page == "Upload":
        st.header("📤 Upload Medical Report")
        uploaded_file = st.file_uploader("Upload a PDF report", type="pdf")
        city = st.text_input("📍 Location", value=get_city_from_ip())

        if uploaded_file:
            st.success("✅ File uploaded successfully.")
            with st.spinner("Extracting..."):
                try:
                    report_text = extract_text_from_pdf(uploaded_file)
                    st.text_area("Extracted Report Text", report_text[:3000], height=200)
                    save_report(st.session_state.username, report_text)
                except Exception as e:
                    st.error(f"Error: {e}")

            st.subheader("🧠 AI Diagnosis")
            with st.spinner("Analyzing deeply with LLM..."):
                response = analyze_text_with_ai(report_text)
                time.sleep(1)
                st.success("✅ AI Diagnosis complete!")
                st.markdown(response)

            st.subheader("👨‍⚕️ Doctor Recommendations")
            if not city:
                st.warning("Location not detected. Set manually.")
            else:
                try:
                    doctors = search_doctors(city)
                    st.markdown("\n".join(doctors))
                except:
                    st.error("Couldn't fetch doctors.")

    elif page == "Dashboard":
        st.header("📊 My Health Dashboard")
        user_files = list(REPORT_DIR.glob(f"{st.session_state.username}_*.txt"))
        if not user_files:
            st.info("No past reports found.")
        else:
            for file in sorted(user_files, reverse=True):
                with st.expander(file.name):
                    st.code(file.read_text())

# --- App Launch ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    main_app()