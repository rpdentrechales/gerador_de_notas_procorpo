import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Teste")

today = datetime.datetime.now()


date = st.date_input(
    "Select your vacation for next year",
    (today, today),
    format="DD-MM-YYYY",
)
st.write(date)
