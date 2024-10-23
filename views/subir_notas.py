import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

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

teste("teste teste")

teste_1 = gerar_obj_api()
teste_2 = gerar_obj_aliquota()
teste_3 = gerar_obj_cc()
teste_4 = gerar_obj_tipo_pagamento()
teste_5 = gerar_obj_unidades()

st.write(teste_1)
st.write(teste_2)
st.write(teste_3)
st.write(teste_4)
st.write(teste_5)

