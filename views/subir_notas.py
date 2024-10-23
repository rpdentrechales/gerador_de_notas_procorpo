import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import load_main_dataframe

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Teste")

teste = query_BillCharges(1,"2024-10-23","2024-10-23")
st.dataframe(teste)
