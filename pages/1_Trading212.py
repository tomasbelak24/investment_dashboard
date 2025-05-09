import streamlit as st
import os
from dotenv import load_dotenv
from utils import *
from db.database import insert_account_cash, fetch_data
import altair as alt

REFRESH_INTERVAL = timedelta(minutes=15)

st.set_page_config(page_title="Trading212 Dashboard", layout="centered")
st.title("📊 Trading212 Account Overview")

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY_212")

if not api_key:
    st.error("API key not found. Please set API_KEY_212 in your .env file.")
    st.stop()

# Button to refresh data
if st.button("🔄 Refresh"):
    last_refresh = get_last_refresh()
    now = datetime.now()

    if last_refresh and (now - last_refresh) < REFRESH_INTERVAL:
        remaining_time = REFRESH_INTERVAL - (now - last_refresh)
        st.warning(f"Please wait {remaining_time} before refreshing again.")
    else:

        data = fetch_account_cash(api_key)
        
        if data:
            save_json(data, "account_cash")
            insert_account_cash(data)
            set_last_refresh()
            st.success("Data refreshed and saved.")
        else:
            st.error("Failed to fetch data.")

 

# Load latest saved data
saved_data = load_json("account_cash")

if saved_data:
    st.subheader("💰 Account Cash Info", divider=True)
    cash_info = saved_data['data']
    st.header(f"{cash_info['total']} €")
    st.write(f"{cash_info['invested']} €")
    roi = cash_info['total'] / cash_info['invested'] * 100 - 100
    color = "green" if roi >= 0 else "red"
    st.header(f":{color}[{'+' if roi >= 0 else '-'}{roi:.2f}%]")

    #st.json(saved_data)
    
else:
    st.warning("No saved data found.")



### Plot
plot_df = fetch_data()
if plot_df is not None:

    st.subheader("📈 Account Cash History", divider=True)
    
    chart = alt.Chart(plot_df).transform_fold(
            ['invested', 'total'],
            as_=['Category', 'Value']
        ).mark_line().encode(
            x=alt.X('fetched_at:T', title='Date', axis=alt.Axis(format='%d-%m-%Y')),
            y=alt.Y('Value:Q', title='EUR'),
            color='Category:N'
        ).properties(
            width=800,
            height=400
    )

    st.altair_chart(chart) 
