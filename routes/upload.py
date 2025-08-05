import streamlit as st
from utils import extract_text_from_pdf, analyze_text

def show_upload():
    st.title("📤 Upload Medical Report")
    uploaded_file = st.file_uploader("Upload a PDF medical report", type="pdf")

    if uploaded_file is not None:
        st.success("✅ File uploaded successfully.")
        with st.spinner("📄 Extracting text..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        st.text_area("📝 Extracted Text", extracted_text, height=200)

        if st.button("🧠 Analyze Report with AI"):
            with st.spinner("Analyzing..."):
                analysis_result = analyze_text(extracted_text)

            st.subheader("🔍 AI Diagnosis")
            st.write(analysis_result)

            # 👇 Add this block for doctor referral
            st.markdown("---")
            st.info("📢 Based on the analysis, we recommend consulting:")
            st.markdown("- 👩‍⚕️ **Dr. Lasya Priya** (General Medicine)")
            st.markdown("- 👨‍⚕️ **Dr. Vamsi Krishna** (Specialist Physician)")
