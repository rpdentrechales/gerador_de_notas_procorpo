import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Utilitários")

dados_os = atualizar_base_de_OS()

resultados_df = pd.DataFrame(dados_os)

st.dataframe(resultados_df)