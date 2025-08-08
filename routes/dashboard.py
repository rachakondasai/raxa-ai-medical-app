# routes/dashboard.py (updated for automatic location fallback)
import streamlit as st
from utils import analyze_text, extract_text_from_pdf, get_current_user, search_doctors_online
import requests
from streamlit_js_eval import streamlit_js_eval


def show_dashboard():
    user = get_current_user()
    st.markdown("## 🩺 Medical Dashboard")
    st.success(f"You're now logged in as **{user}**")

    if "location" not in st.session_state:
        st.session_state.location = {"city": "", "region": "", "country": "", "lat": None, "lon": None}

    with st.spinner("📍 Detecting your location..."):
        js_data = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
                                    key="get_coords")

        if js_data and "latitude" in js_data and "longitude" in js_data:
            lat = js_data["latitude"]
            lon = js_data["longitude"]
            st.session_state.location["lat"] = lat
            st.session_state.location["lon"] = lon
            try:
                res = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
                data = res.json()
                addr = data.get("address", {})
                st.session_state.location["city"] = addr.get("city") or addr.get("town") or addr.get("village", "")
                st.session_state.location["region"] = addr.get("state", "")
                st.session_state.location["country"] = addr.get("country", "")
            except:
                st.warning("⚠️ Reverse geocoding via GPS failed. Trying IP-based location...")
        
        # If still no city from GPS, fallback to IP
        if not st.session_state.location["city"]:
            try:
                ipinfo = requests.get("https://ipinfo.io/json?token=c7376765bc398d344b7e666fb4027adb288b40e2e4feadc5bcdb600c4a196d3f").json()
                city = ipinfo.get("city", "")
                region = ipinfo.get("region", "")
                country = ipinfo.get("country", "")
                if city:
                    st.session_state.location.update({"city": city, "region": region, "country": country})
                    st.info("🌐 Used IP-based location fallback.")
            except:
                st.warning("❌ Could not determine your location from IP either.")

    city = st.session_state.location.get("city", "Unknown")
    st.markdown(f"###📍 Detected Location: `{city}`")

    with st.expander("✏️ Override Location"):
        manual_city = st.text_input("City", city)
        manual_state = st.text_input("State/Region", st.session_state.location.get("region", ""))
        manual_country = st.text_input("Country", st.session_state.location.get("country", ""))
        if st.button("Use Manual Location"):
            st.session_state.location = {"city": manual_city, "region": manual_state, "country": manual_country, "lat": None, "lon": None}
            st.rerun()

    st.subheader("📤 Upload Medical Report")
    uploaded_file = st.file_uploader("Upload a PDF medical report", type="pdf")

    if uploaded_file:
        st.success("✅ File uploaded successfully.")
        with st.expander("📝 Extracted Text"):
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text", text, height=300)

        with st.spinner("🔍 Analyzing report with AI..."):
            ai_summary = analyze_text(text)
        st.subheader("🧠 AI Diagnosis")
        st.write(ai_summary)

        city = st.session_state.location.get("city", "")
        if city:
            st.subheader("📢 Recommended Local Doctors")
            with st.spinner("🔎 Searching for top-rated doctors in your city..."):
                api_key = st.secrets["SERPAPI_KEY"]
                specialty = "General Medicine"
                results = search_doctors_online(specialty, city, api_key)

                if results:
                    for doc in results:
                        st.markdown(f"**👨‍⚕️ {doc['name']}**")
                        st.markdown(f"📍 {doc['address']}")
                        st.markdown(f"⭐ {doc['rating']} ({doc['reviews']} reviews)")
                        st.markdown(f"🔗 [View Online]({doc['link']})")
                        st.markdown("---")
                else:
                    st.info("No doctors found via search. Please try again later or update your location.")
        else:
            st.warning("Unable to determine your city. Doctor recommendations are disabled.")