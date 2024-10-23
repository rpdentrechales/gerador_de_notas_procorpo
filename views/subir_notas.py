import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
from auxiliar import *

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

df = load_main_dataframe("CRM - Billcharges (Json)")



# @st.cache_data
# def load_main_dataframe(worksheet):

#   conn = st.connection("gsheets", type=GSheetsConnection)
#   df = conn.read(worksheet=worksheet,dtype={"Ad ID": str})

#   return df

# @st.cache_data
# def load_aux_dataframe(worksheet,duplicates_subset):

#   conn = st.connection("gsheets", type=GSheetsConnection)
#   df = conn.read(worksheet=worksheet)
#   df = df.drop_duplicates(subset=duplicates_subset)

#   return df

st.title("Subir Notas")

st.dataframe(df)
