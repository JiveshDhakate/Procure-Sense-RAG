import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="Query Offers", page_icon="🔍")
st.title("🔍 Query Supplier Offers")

# Use environment variable for backend 
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  
QUERY_URL = f"{BASE_URL}/spear-rag/evaluate-offers" 

with st.form("query_form"):
    query_text = st.text_input(
        "Enter your query:",
        placeholder="Find the best supplier for 10mm steel bolts under 1 dollar"
    )
    submitted = st.form_submit_button("Search")

if submitted:
    if query_text.strip():
        try:
            # Send the updated payload
            response = requests.post(QUERY_URL, json={"query": query_text})

            if response.status_code == 200:
                data = response.json()

                # Recommendation
                st.subheader("✅ Recommended Supplier")
                st.write(data.get("recommendation", "No recommendation returned."))

                # Reasoning
                st.subheader("📌 Reasoning")
                st.write(data.get("reasoning", "No reasoning provided."))

                # All evaluated offers
                st.subheader("📦 Offers Evaluated")
                offers = data.get("offers_evaluated", [])
                if offers:
                    for idx, offer in enumerate(offers, 1):
                        st.markdown(f"**Offer #{idx}**")
                        st.json(offer)
                else:
                    st.write("No offers evaluated.")

            else:
                st.error(f" Query failed: {response.text}")

        except Exception as e:
            st.error(f" Error connecting to backend: {e}")

    else:
        st.warning(" Please enter a query.")
