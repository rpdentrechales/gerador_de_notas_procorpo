import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Deletar Base MongoDB")
deletar_button = st.button("Deletar Base")

if deletar_button:
    with st.status("Deletandos Bases...", expanded=True) as status:

        deletar_todos_documentos("log_clientes", query=None)
        deletar_todos_documentos("log_os", query=None)
        deletar_todos_documentos("os_processados", query=None)
        st.balloons()

        status.update(
            label="Bases deletadas", state="complete", expanded=False
        )

st.title("Adicionar Conta Corrente")

contas_correntes = load_dataframe("Auxiliar - Contas Correntes")
dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")

