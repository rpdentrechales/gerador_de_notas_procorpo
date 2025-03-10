import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Deletar Base MongoDB")
deletar_button = st.button("Deletar Base")

if deletar_button:
    deletar_todos_documentos("log_clientes", query=None)
    st.ballons()