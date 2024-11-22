import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Utilitários")

image_url = "https://vstevam.com/images/building.gif"

# Display the image in Streamlit
st.image(image_url, caption="Under construction!!!!!!")

# df_1,df_2 = atualizar_base_de_clientes()

# st.write(df_1)
# st.write(df_2)
