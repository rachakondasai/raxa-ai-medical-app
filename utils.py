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
