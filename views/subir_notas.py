import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Selecionar datas")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

date = st.date_input(
    "Select your vacation for next year",
    (three_days_ago, today),
    format="DD/MM/YYYY",
)

st.write(date[0].strftime('%Y-%m-%d'))
st.write(date[1].strftime('%Y-%m-%d'))
