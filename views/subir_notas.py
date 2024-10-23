import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import load_main_dataframe

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Teste")

df = load_main_dataframe("CRM - Billcharges (Json)")
st.dataframe(df)
