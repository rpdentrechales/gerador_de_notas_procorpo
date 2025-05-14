import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Clientes com erros", page_icon="💎",layout="wide")

st.title("Clientes com Erros")
st.caption("Lista de clientes com erros na integração com o Omie que precisam ser corrigidos manualmente.")

clientes_com_erros = pegar_dados_mongodb("clientes_com_erros")
st.dataframe(clientes_com_erros, hide_index=True, use_container_width=True)