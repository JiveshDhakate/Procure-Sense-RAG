import streamlit as st
import requests
import os

st.set_page_config(page_title="Upload Offers", page_icon="📤")
st.title("📤 Upload Supplier Offer")

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000") 
UPLOAD_URL = f"{BASE_URL}/spear-rag/ingest-offers"

with st.form("upload_form"):
    quotation_text = st.text_area(
        "Paste supplier quotation text:",
        height=200,
        placeholder="E.g. QuickFix offers 10mm bolts for $0.75/unit..."
    )
    submitted = st.form_submit_button("Upload")

if submitted:
    if quotation_text.strip():
        try:
            response = requests.post(UPLOAD_URL, json={"text": quotation_text})
            if response.status_code == 200:
                data = response.json()
                st.success(f"{data['offers_added']} offer(s) uploaded successfully!")
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.warning("Please enter some text before uploading.")
