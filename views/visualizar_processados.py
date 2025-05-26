import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from datetime import datetime, timedelta,time

st.set_page_config(page_title="OS Processadas", page_icon="💎",layout="wide")

st.title("OS Processadas")

today = datetime.now()
trinta_dias = today - timedelta(days=30)

data_seletor = st.date_input(
    "Selecione a data do pagamento",
    (trinta_dias, today),
    format="DD/MM/YYYY",
)

if len(data_seletor) == 2:
    data_inicial = pd.to_datetime(data_seletor[0])
    data_final = pd.to_datetime(data_seletor[1])
else:
    data_inicial = pd.to_datetime(data_seletor[0])
    data_final = data_inicial

pegar_os_botao = st.button("Pegar OS Processadas", type="primary")

if pegar_os_botao:
    st.write(f"Buscando OS processadas entre {data_inicial} e {data_final}...")
    os_processados = pegar_todos_os(data_inicial, data_final)
    st.write(os_processados)