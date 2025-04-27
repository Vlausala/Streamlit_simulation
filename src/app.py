import streamlit as st
import requests
import pandas as pd
import datetime
from utils.utils import welcome_message
from config.api_config import BASE_API_URL, DEFAULT_TUNNIT, DEFAULT_TULOS, DEFAULT_DATE

# Git test

# Git test new branch fasdfafafafafafa

st.set_page_config(page_title="My Streamlit App", layout="wide")

st.title("🚀 Welcome to My Streamlit App") 
st.write(welcome_message())

# --- User Input Section ---
st.sidebar.header("🔧 Configure API Request")

# Select number of hours
tunnit = st.sidebar.slider("Hours to fetch (tunnit)", min_value=1, max_value=24, value=DEFAULT_TUNNIT)

# Select result type
tulos = st.sidebar.selectbox("Result type (tulos)", options=["haja", "sarja"], index=0)

# Select date
today = datetime.date.today()
date_input = st.sidebar.date_input("Select date", today)
aikaraja = date_input.strftime("%Y-%m-%d")

# --- Build API URL dynamically ---
params = {
    "tunnit": tunnit,
    "tulos": tulos,
    "aikaraja": aikaraja
}

response = requests.get(BASE_API_URL, params=params)

# --- Handle Response ---
if response.status_code == 200:
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df["hinta"] = df["hinta"].astype(float)
    
    # Convert to datetime and extract hour
    df["aikaleima_suomi"] = pd.to_datetime(df["aikaleima_suomi"])
    df['hour'] = df["aikaleima_suomi"].dt.hour  # Extract hour from timestamp

    # Sort data by hour
    df = df.sort_values("hour")

    # Set the index to the timestamp for plotting
    df.set_index("hour", inplace=True)

    # Show data
    st.subheader(f"📈 Electricity Prices on {aikaraja}")
    st.line_chart(df[['hinta']])

    with st.expander("Show raw data"):
        st.dataframe(df)
else:
    st.error("Failed to fetch data from the API.")
