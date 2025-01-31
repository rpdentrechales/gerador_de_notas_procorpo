import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Utilitários")

with st.status("Carregando Notas...", expanded=True) as status:

    st.write("Pegando dados")

    dados_os = atualizar_base_de_OS()

    resultados_df = pd.DataFrame(dados_os)

    status.update(
        label="Todos os dados Carregados!", state="complete", expanded=False
    )


st.dataframe(resultados_df)