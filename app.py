import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

st.set_page_config(page_title="EvokedMasterPrep", layout="centered")

# Replace with your sheet URL (make public "anyone with link can view")
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FwzTMzlevZXvXfBRtsVPNWuW0A8oUnaQGPARK2NLliI/edit?usp=sharing"

@st.cache_data(ttl=60)  # Reload every minute
def load_questions():
    df = pd.read_csv(SHEET_URL)
    return df.to_dict('records')

questions = load_questions()

# ... (same app code as before, with fetch replaced by load_questions())
