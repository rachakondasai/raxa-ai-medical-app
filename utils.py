import subprocess
from PyPDF2 import PdfReader
import streamlit as st

def get_current_user():
    return st.session_state.get("user_id", "Guest")


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def analyze_text(text):
    try:
        command = ["ollama", "run", "llama3", f"Analyze the following medical report:\n{text}"]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"❌ AI analysis failed:\n{result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "⏳ Analysis timed out. Please try with a shorter report."
    except Exception as e:
        return f"🔥 Unexpected error: {str(e)}"

import requests

def get_user_location():
    try:
        res = requests.get("https://ipinfo.io/json?token=c7376765bc398d344b7e666fb4027adb288b40e2e4feadc5bcdb600c4a196d3f")
        data = res.json()
        return data.get("city", ""), data.get("region", ""), data.get("country", "")
    except:
        return "", "", ""

def search_doctors_online(specialty, city, api_key):
    from serpapi import GoogleSearch

    query = f"Top rated {specialty} doctors in {city}"

    search = GoogleSearch({
        "q": query,
        "location": city,
        "hl": "en",
        "gl": "in",
        "api_key": api_key
    })

    results = search.get_dict()
    local_results = results.get("local_results", {}).get("places", [])

    doctors = []
    for place in local_results:
        doctors.append({
            "name": place.get("title"),
            "address": place.get("address"),
            "rating": place.get("rating"),
            "reviews": place.get("reviews"),
            "link": place.get("link")
        })
    return doctors
