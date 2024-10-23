import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *


st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Testar Billcharge")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

col_data_1, col_data_2, blank_3 = st.columns([1.5,1,2])

with col_data_1:
  data_seletor = st.date_input(
      "Select your vacation for next year",
      (three_days_ago, today),
      format="DD/MM/YYYY",
  )

  if len(data_seletor) == 2:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_final = data_seletor[1].strftime('%Y-%m-%d')
  else:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_final = data_inicial

with col_data_2:
  pegar_dados = st.button("Executar")

if pegar_dados:
  teste = paste_billcharges_with_json(data_inicial,data_final)
  st.write(teste)
