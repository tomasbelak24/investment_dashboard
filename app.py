import streamlit as st
import os
import json
from dotenv import load_dotenv
from utils import fetch_account_cash, save_json, load_json

st.set_page_config(page_title="Trading212 Dashboard", layout="centered")
st.title("📊 Trading212 Account Overview")

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY_212")

if not api_key:
    st.error("API key not found. Please set API_KEY_212 in your .env file.")
    st.stop()

# Button to refresh data
if st.button("🔄 Refresh Account Cash"):
    data = fetch_account_cash(api_key)
    if data:
        save_json(data, "account_cash")
        st.success("Data refreshed and saved.")
    else:
        st.error("Failed to fetch data.")

# Load latest saved data
saved_data = load_json("account_cash")

if saved_data:
    st.subheader("💰 Account Cash Info")
    st.json(saved_data)
else:
    st.warning("No saved data found.")
