import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
import types

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - testar funções")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

data_seletor = st.date_input(
    "Select your vacation for next year",
    (three_days_ago, today),
    format="DD/MM/YYYY",
)

data_inicial = data_seletor[0].strftime('%Y-%m-%d')
data_final = data_seletor[1].strftime('%Y-%m-%d')

teste = paste_billcharges_with_json(data_inicial,data_final)

st.write(teste)
