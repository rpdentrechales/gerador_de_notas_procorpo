import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Utilitários")

df_1,df_2 = atualizar_base_de_clientes()

st.dataframe(df_1,hide_index = True,use_container_width=True)
st.dataframe(df_2,hide_index = True,use_container_width=True)
