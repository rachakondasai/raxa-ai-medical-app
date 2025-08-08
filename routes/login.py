from utils import get_user_location

# After successful login
user_id = st.session_state["user_id"] = username

# Get and store location
city, region, country = get_user_location()
st.session_state["location"] = {"city": city, "region": region, "country": country}

st.success(f"Welcome, {user_id}! Detected location: {city}, {region}, {country}")
st.switch_page("Dashboard")  # Or however you navigate
