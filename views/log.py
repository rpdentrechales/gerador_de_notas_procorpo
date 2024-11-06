import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Logs", page_icon="💎",layout="wide")

st.title("Log Clientes:")
log_clientes_df = pegar_dados_mongodb("log_clientes")
st.dataframe(log_clientes_df)

st.title("Log Ordens de Serviço:")
log_os_df = pegar_dados_mongodb("log_os")
st.dataframe(log_os_df)
