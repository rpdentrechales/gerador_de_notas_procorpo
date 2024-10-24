import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *


st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Testar Billcharge")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

col_data_1, col_data_2, blank_3 = st.columns([1,1,3])

with col_data_1:
  data_seletor = st.date_input(
      "Selecione a data",
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
  st.write("**Pegar dados do CRM**")
  pegar_dados = st.button("Executar",type="primary")

if (pegar_dados):
  dados_crm_df = paste_billcharges_with_json(data_inicial,data_final)
  st.session_state["dados_crm_df"] = dados_crm_df

if "dados_crm_df" in st.session_state:
  st.write("**Selecione notas para subir**")
  dados_crm_df = st.session_state["dados_crm_df"]
  filtro_pagamento = st.selectbox(
    "Selecionar tipo de pagamento",
    dados_crm_df["Tipo de Pagamento"].unique(),
    index=None
    )
  filtered_df = dados_crm_df.loc[dados_crm_df["Tipo de Pagamento"] == filtro_pagamento]
  if filtro_pagamento:
    st.write(filtered_df)
