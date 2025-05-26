import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def load_dataframe(worksheet):

  conn = st.connection("gsheets", type=GSheetsConnection)
  df = conn.read(worksheet=worksheet)

  return df

def update_sheet(worksheet, df):
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(data=df,worksheet=worksheet)
    return df